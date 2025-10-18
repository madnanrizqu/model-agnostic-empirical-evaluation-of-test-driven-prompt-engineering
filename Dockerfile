# Dockerfile for LLM Evaluation System
# Supports Python 3.11.x as required by the project

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Configure Poetry to create virtualenv in project directory
RUN poetry config virtualenvs.in-project true

# Copy dependency files first (for better layer caching)
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

# Copy .env.example to .env if .env doesn't exist (will be overridden by mount)
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Set environment variables for non-interactive execution
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Declare volumes for experiment results persistence and configuration
# Mount these to save results and use custom configs:
#   -v $(pwd)/config:/app/config  (use your local config files)
#   -v $(pwd)/rq1:/app/rq1        (save results to host)
#   -v $(pwd)/rq2:/app/rq2        (save results to host)
VOLUME ["/app/config", "/app/rq1", "/app/rq2"]

# Default command shows help
CMD ["poetry", "run", "python", "-c", "print('LLM Evaluation System Docker Container\\n\\n⚠️  IMPORTANT: Mount volumes to persist results and use custom configs!\\n\\nUsage:\\n  docker run -v $(pwd)/.env:/app/.env -v $(pwd)/config:/app/config -v $(pwd)/rq1:/app/rq1 -v $(pwd)/rq2:/app/rq2 <image> <command>\\n\\nCommands:\\n  • poetry run python rq1/run_all.py\\n  • poetry run python rq2/run_all.py\\n  • poetry run python rq1/<experiment>/get_solution.py\\n\\nResults saved to: /app/rq1/<experiment>/results_*/ (must mount to persist!)\\nConfig from: /app/config/rq1.py, /app/config/rq2.py (mount to customize!)\\n\\nSee DOCKER.md for detailed usage.')"]
