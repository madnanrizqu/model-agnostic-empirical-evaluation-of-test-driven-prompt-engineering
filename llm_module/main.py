import time
from datetime import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import tempfile
import httpx

load_dotenv()
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_TOKEN")
SUMOPOD_API_KEY = os.getenv("SUMOPOD_TOKEN")
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_TOKEN")
CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

HUGGING_FACE_NAME_URL_MAP = {
    "Qwen/Qwen2.5-Coder-3B-Instruct": "https://lwnxgyx0ip0qy5db.us-east-1.aws.endpoints.huggingface.cloud/v1/",
    "Qwen/Qwen2.5-Coder-7B-Instruct": "https://fp6motvyt9hw0vcz.us-east-1.aws.endpoints.huggingface.cloud/v1/",
    "Qwen/Qwen2.5-Coder-14B-Instruct": "https://fur59g14ehnip28i.us-east-1.aws.endpoints.huggingface.cloud/v1/",
    "Qwen/Qwen2.5-Coder-32B-Instruct": "https://uz65gtkv52071x3n.us-east-1.aws.endpoints.huggingface.cloud/v1/",
}


class ModelSolutionGenerator:
    def __init__(self, configs, options):
        self.models = []
        self.generation_dir = None
        self.temp_results_dir_prefix = options["temp_results_dir_prefix"]
        self.dataset_prompt_template = options["dataset_prompt_template"]
        self.messages = []
        self.max_retries = options.get("max_retries", 1)

        for config in configs:
            model = config.copy()
            if config["type"] == "hugging_face":
                base_url = HUGGING_FACE_NAME_URL_MAP.get(config["name"])
                if base_url is None:
                    raise ValueError(
                        f"Model {config['name']} not found in HUGGING_FACE_NAME_URL_MAP"
                    )
                client = OpenAI(
                    base_url=base_url,
                    api_key=HUGGING_FACE_API_KEY,
                    max_retries=self.max_retries,
                )
            elif config["type"] == "open_router":
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=OPEN_ROUTER_API_KEY,
                    max_retries=self.max_retries,
                )
            elif config["type"] == "sumopod":
                client = OpenAI(
                    base_url="https://ai.sumopod.com/v1",
                    api_key=SUMOPOD_API_KEY,
                    max_retries=self.max_retries,
                )
            elif config["type"] == "groq":
                client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=GROQ_API_KEY,
                    max_retries=self.max_retries,
                )
            elif config["type"] == "cloudflare":
                client = OpenAI(
                    base_url=f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/v1",
                    api_key=CLOUDFLARE_API_KEY,
                    max_retries=self.max_retries,
                )
            model.update({"client": client})
            self.models.append(model)

    def __call_model(self, model, messages):
        print(f"Calling model {model['name']}...")
        start_time = time.time()

        # Set default parameters if not provided
        params = model.get("params", {})

        # Not too long to make run_all stuck
        # Not too short that harder problems cannot be solved
        timeout_seconds = 150

        # Build API call parameters from model configuration
        api_params = {
            "model": model["key"],
            "messages": messages,
            "timeout": timeout_seconds,
        }

        # Add all parameters from config, excluding None values
        for param_name, param_value in params.items():
            if param_value is not None:
                api_params[param_name] = param_value

        # Log the parameters being used
        param_list = [f"{k}: {v}" for k, v in params.items() if v is not None]
        print(f"Using parameters: {', '.join(param_list)}")
        print(f"Timeout: {timeout_seconds} seconds")

        try:
            response = model["client"].chat.completions.create(**api_params)
            end_time = time.time()
            elapsed_seconds = f"{(end_time - start_time):.2f}"
            response_msg = response.choices[0].message.content
            timestamp = datetime.now().isoformat()

            print(f"Success! API Response time: {elapsed_seconds} seconds")
            return response_msg, timestamp, elapsed_seconds

        except Exception as e:
            end_time = time.time()
            elapsed_seconds = f"{(end_time - start_time):.2f}"

            # Check if it's a timeout-related error
            error_msg = str(e).lower()
            error_type = type(e).__name__
            is_timeout = (
                # Direct timeout exception types
                isinstance(e, (TimeoutError, httpx.TimeoutException))
                # Check error type name
                or "timeout" in error_type.lower()
                # Check common timeout error types
                or error_type
                in ["TimeoutError", "ReadTimeoutError", "ConnectTimeoutError"]
                # Check error message
                or "timeout" in error_msg
                or "timed out" in error_msg
                # Check class hierarchy for timeout-related exceptions
                or any("timeout" in base.__name__.lower() for base in type(e).__mro__)
            )

            if is_timeout:
                print(
                    f"TIMEOUT ERROR after {elapsed_seconds} seconds (limit: {timeout_seconds}s)"
                )
                print(f"Error details: {str(e)}")
                # Re-raise as TimeoutError for consistent handling upstream
                raise TimeoutError(
                    f"API call timed out after {elapsed_seconds} seconds (limit: {timeout_seconds}s): {str(e)}"
                )
            else:
                print(f"API ERROR after {elapsed_seconds} seconds: {str(e)}")
                # Re-raise original exception for non-timeout errors
                raise

    def __init_generation_progress(self, dataset_name):
        dir_path = os.path.join(
            self.temp_results_dir_prefix,
            f"tmp_{dataset_name}_generation_start_at_{datetime.now().isoformat()}",
        )
        os.makedirs(dir_path, exist_ok=True)
        print(f"Progress will be saved to {dir_path}")

        self.generation_dir = dir_path

    def __save_generation_progress(self, results, errors):
        results_path = os.path.join(self.generation_dir, "generation_results.json")
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)

        errors_path = os.path.join(self.generation_dir, "generation_errors.json")
        with open(errors_path, "w") as f:
            json.dump(errors, f, indent=2)

    def store_messages(self, messages):
        """
        Stores messages to the instance's messages attribute.

        Args:
            messages: Array of messages in OpenAI format to store
        """
        self.messages = messages.copy() if messages else []

    def get_stored_messages(self):
        """
        Returns the currently stored messages.

        Returns:
            Array of stored messages
        """
        return self.messages.copy()

    def create_messages(self, prompt, assistant_answer=None):
        """
        Creates an array of messages for OpenAI API calls.
        Optionally includes an assistant's previous answer.
        """
        messages = [
            {"role": "system", "content": self.dataset_prompt_template},
            {"role": "user", "content": prompt},
        ]
        if assistant_answer is not None:
            messages.append({"role": "assistant", "content": assistant_answer})

        return messages

    def extend_messages(self, messages, new_content, role="user"):
        """
        Extends an existing message array with a new message.

        Args:
            messages: Existing array of messages for OpenAI API calls
            new_content: Content to add to the messages
            role: Role of the new message (default: "user")

        Returns:
            Extended message array
        """
        messages.append({"role": role, "content": new_content})
        return messages

    def get_solution_with_existing_messages(self, messages, row):
        """
        Process a single row using provided messages array and generate solutions using all models

        Args:
            messages: Existing OpenAI-formatted messages array to use for the API call
            row: The dataset row to process

        Returns:
            List of results from all models
        """
        results = []
        errors = []

        print(f"\nSolving row id {row['task_id']}...")

        for model in self.models:
            try:
                response_msg, timestamp, elapsed_seconds = self.__call_model(
                    model, messages
                )

                result = {
                    "dataset_name": "",
                    "dataset_row_id": row["task_id"],
                    "solution": response_msg,
                    "llm_name": model["name"],
                    "prompt": row["prompt"],
                    "timestamp": timestamp,
                    "response_time": elapsed_seconds,
                }
                if "context" in row:
                    result["context"] = row["context"]

                results.append(result)

            except Exception as e:
                print(f"Error with model {model['name']}: {str(e)}")

                error = {
                    "dataset_name": "",
                    "dataset_row_id": row["task_id"],
                    "error": str(e),
                    "llm_name": model["name"],
                    "prompt": row["prompt"],
                    "timestamp": datetime.now().isoformat(),
                }
                errors.append(error)

        return results, errors

    def _get_solution_for_row(
        self,
        row,
        dataset_name,
        absolute_start_time,
        index,
        total_rows,
        results=[],
        errors=[],
    ):
        """
        Process a single row from the dataset and generate solutions using all models

        Args:
            row: The dataset row to process
            dataset_name: Name of the dataset
            dataset_prompt_template: Template for the system prompt
            results: List to append successful results to
            errors: List to append errors to
            absolute_start_time: Start time for elapsed time calculation
            index: Current row index for progress tracking
            total_rows: Total number of rows for progress calculation
        """
        absolute_elapsed_seconds = f"{(time.time() - absolute_start_time):.2f}"
        messages = self.create_messages(row["prompt"])

        print("\n")
        progress = (index + 1) / total_rows * 100
        print(
            f"Solving row id {row['task_id']}... [{index + 1}/{total_rows}] ({progress:.1f}%)"
        )
        print(f"{absolute_elapsed_seconds} seconds has elapsed since start")

        for model in self.models:
            try:
                response_msg, timestamp, elapsed_seconds = self.__call_model(
                    model, messages
                )

                result = {
                    "dataset_name": dataset_name,
                    "dataset_row_id": row["task_id"],
                    "solution": response_msg,
                    "llm_name": model["name"],
                    "prompt": row["prompt"],
                    "timestamp": timestamp,
                    "response_time": elapsed_seconds,
                }
                if "context" in row:
                    result["context"] = row["context"]

                results.append(result)

            except Exception as e:
                print(f"Error with model {model['name']}")

                error = {
                    "dataset_name": dataset_name,
                    "dataset_row_id": row["task_id"],
                    "error": str(e),
                    "llm_name": model["name"],
                    "prompt": row["prompt"],
                    "timestamp": datetime.now().isoformat(),
                }
                errors.append(error)

        return results, errors

    def generate_solution_for_dataset(
        self,
        dataset_name,
        dataset_numpy_frame,
        start_index=None,
        end_index=None,
    ):
        results = []
        errors = []
        absolute_start_time = time.time()
        self.__init_generation_progress(dataset_name)
        print(f"Getting solution for {dataset_name}...")

        # Filter dataset based on start_index and/or end_index if provided
        filtered_dataset = dataset_numpy_frame
        if start_index is not None or end_index is not None:
            # Convert to indices using iloc
            start = start_index if start_index is not None else 0
            end = end_index if end_index is not None else len(dataset_numpy_frame) - 1
            filtered_dataset = dataset_numpy_frame.iloc[
                start : end + 1
            ]  # +1 because end is inclusive

        for index, row in filtered_dataset.iterrows():
            self._get_solution_for_row(
                row,
                dataset_name,
                absolute_start_time,
                index,
                len(dataset_numpy_frame),
                results,
                errors,
            )
            self.__save_generation_progress(results, errors)

        return results, errors

    def regenerate_failed_reported_rows(self, failed_rows_data, dataset):
        """
        Regenerates solutions for failed dataset rows

        Args:
            failed_rows_data: Array of objects containing information about failed generations
            dataset: The complete dataset containing all rows
        """
        results = []
        errors = []
        absolute_start_time = time.time()

        self.__init_generation_progress(failed_rows_data[0]["dataset_name"])

        for failed_row in failed_rows_data:
            absolute_elapsed_seconds = f"{(time.time() - absolute_start_time):.2f}"
            dataset_row = dataset[
                dataset["task_id"] == failed_row["dataset_row_id"]
            ].iloc[0]

            messages = self.create_messages(failed_row["prompt"])

            print(f"\nRetrying row id {failed_row['dataset_row_id']}...")
            print(f"{absolute_elapsed_seconds} seconds has elapsed since start")

            for model in self.models:
                if model["name"] == failed_row["llm_name"]:
                    try:
                        response_msg, timestamp, elapsed_seconds = self.__call_model(
                            model, messages
                        )

                        result = {
                            "dataset_name": failed_row["dataset_name"],
                            "dataset_row_id": failed_row["dataset_row_id"],
                            "solution": response_msg,
                            "llm_name": model["name"],
                            "prompt": failed_row["prompt"],
                            "timestamp": timestamp,
                            "response_time": elapsed_seconds,
                            "retry": True,
                        }
                        results.append(result)

                    except Exception as e:
                        print(f"Error with model {model['name']}")

                        error = failed_row.copy()
                        error.update(
                            {
                                "error": str(e),
                                "timestamp": datetime.now().isoformat(),
                                "retry": True,
                            }
                        )
                        errors.append(error)

                    self.__save_generation_progress(results, errors)

        return results, errors
