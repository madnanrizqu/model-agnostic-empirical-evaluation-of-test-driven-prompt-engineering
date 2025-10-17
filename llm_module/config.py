from enum import Enum
from typing import List, Dict, Any


class LLMConfigManager:
    """
    Manages LLM configurations for different model types
    """

    def __init__(self):
        # Deprecated config, used in rq1
        self.closed_llm_config = {
            "name": "openai/gpt-4o-2024-11-20",
            "key": "openai/gpt-4o-2024-11-20",
            "type": "open_router",
            "params": {"temperature": 0, "seed": 1000},
        }

        self.open_llm_config = {
            "name": "Qwen/Qwen2.5-Coder-32B-Instruct",
            "key": "Qwen/Qwen2.5-Coder-32B-Instruct",
            "type": "hugging_face",
            "params": {"temperature": 0, "seed": 1000},
        }

        # More flexible config
        self.llm_configurations = {
            # OpenRouter API - OpenAI Models
            "CHATGPT_4O": {
                "name": "openai/gpt-4o-2024-11-20",
                "key": "openai/gpt-4o-2024-11-20",
                "type": "open_router",
                "params": {"temperature": 0, "seed": 1000},
            },
            "CHATGPT_4O_MINI": {
                "name": "openai/gpt-4o-mini-2024-07-18",
                "key": "openai/gpt-4o-mini-2024-07-18",
                "type": "open_router",
                "params": {"temperature": 0, "seed": 1000},
            },
            "CLAUDE_35_SONNET": {
                "name": "anthropic/claude-3.5-sonnet",
                "key": "anthropic/claude-3.5-sonnet",
                "type": "open_router",
                "params": {"temperature": 0, "seed": 1000},
            },
            "CLAUDE_35_HAIKU": {
                "name": "anthropic/claude-3.5-haiku",
                "key": "anthropic/claude-3.5-haiku",
                "type": "open_router",
                "params": {"temperature": 0, "seed": 1000},
            },
            "QWEN_2_5_CODER_32B_OR": {
                "name": "qwen/qwen-2.5-coder-32b-instruct",
                "key": "qwen/qwen-2.5-coder-32b-instruct",
                "type": "open_router",
                "params": {
                    "temperature": 0,
                    "seed": 1000,
                    "extra_body": {
                        "provider": {
                            "only": ["cloudflare"]  # restrict to cloudflare only
                        }
                    },
                },
            },
            # HuggingFace Endpoints
            "QWEN_2_5_CODER_32B": {
                "name": "Qwen/Qwen2.5-Coder-32B-Instruct",
                "key": "Qwen/Qwen2.5-Coder-32B-Instruct",
                "type": "hugging_face",
                "params": {"temperature": 0, "seed": 1000},
            },
            "QWEN_14B_CODER": {
                "name": "Qwen/Qwen2.5-Coder-14B-Instruct",
                "key": "Qwen/Qwen2.5-Coder-14B-Instruct",
                "type": "hugging_face",
                "params": {"temperature": 0, "seed": 1000},
            },
            "QWEN_7B_CODER": {
                "name": "Qwen/Qwen2.5-Coder-7B-Instruct",
                "key": "Qwen/Qwen2.5-Coder-7B-Instruct",
                "type": "hugging_face",
                "params": {"temperature": 0, "seed": 1000},
            },
            "QWEN_3B_CODER": {
                "name": "Qwen/Qwen2.5-Coder-3B-Instruct",
                "key": "Qwen/Qwen2.5-Coder-3B-Instruct",
                "type": "hugging_face",
                "params": {"temperature": 0, "seed": 1000},
            },
            # GROQ ENDPOINTS
            "QWEN_32B_CODER_GROQ": {
                "name": "qwen/qwen3-32b",
                "key": "qwen/qwen3-32b",
                "type": "groq",
                "params": {"temperature": 0, "seed": 1000, "reasoning_effort": "none"},
            },
            # CLOUDFLARE ENDPOINTS
            "QWEN_32B_CODER_CF": {
                "name": "@cf/qwen/qwen2.5-coder-32b-instruct",
                "key": "@cf/qwen/qwen2.5-coder-32b-instruct",
                "type": "cloudflare",
                "params": {"temperature": 0, "seed": 1000},
            },
        }

    def get_llm_config(self, llm_key: str) -> List[Dict[str, Any]]:
        """Get configuration for a specific LLM by its key.

        Args:
            llm_key: One of the 12 supported LLM configuration keys

        Returns:
            List containing single LLM configuration dictionary

        Raises:
            ValueError: If llm_key is not supported
        """
        if llm_key not in self.llm_configurations:
            supported_keys = list(self.llm_configurations.keys())
            raise ValueError(
                f"Unsupported LLM key: {llm_key}. Supported keys: {supported_keys}"
            )

        return [self.llm_configurations[llm_key]]

    def get_llm_config_by_type(self, llm_to_use: str) -> List[Dict[str, Any]]:
        """
        Legacy method for backward compatibility.
        Get configuration based on the specified type

        Args:
          llm_to_use: Type of LLM to use ('CLOSED_LLM', 'OPEN_LLM', or 'BOTH_LLM')

        Returns:
          List of configuration dictionaries

        Raises:
          ValueError: If llm_to_use is not a valid option
        """
        if llm_to_use == "CLOSED_LLM":
            return [self.closed_llm_config]
        elif llm_to_use == "OPEN_LLM":
            return [self.open_llm_config]
        elif llm_to_use == "BOTH_LLM":
            return [self.closed_llm_config, self.open_llm_config]
        else:
            raise ValueError("configs must be one of: CLOSED_LLM, OPEN_LLM, BOTH_LLM")
