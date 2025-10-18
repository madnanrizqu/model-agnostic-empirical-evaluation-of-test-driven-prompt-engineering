# Docker Usage

## Quick Start

```bash
# 1. Pull the pre-built image from Docker Hub
docker pull madnanrizqu/td-python-prompt-eval:latest

# 2. Run experiments (results and config are persisted to host)
# RQ1
docker run \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/rq1:/app/rq1 \
  -v $(pwd)/rq2:/app/rq2 \
  madnanrizqu/td-python-prompt-eval \
  poetry run python rq1/run_all.py

# RQ2
docker run \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/rq1:/app/rq1 \
  -v $(pwd)/rq2:/app/rq2 \
  madnanrizqu/td-python-prompt-eval \
  poetry run python rq2/run_all.py
```

## Building Locally (Optional)

If you want to build the image yourself instead of pulling from Docker Hub:

```bash
docker build -t madnanrizqu/td-python-prompt-eval .
```

## Essential Commands

**Run all RQ1 experiments:**

```bash
docker run -v $(pwd)/.env:/app/.env -v $(pwd)/config:/app/config -v $(pwd)/rq1:/app/rq1 \
  madnanrizqu/td-python-prompt-eval poetry run python rq1/run_all.py
```

**Run specific experiments:**

```bash
docker run -v $(pwd)/.env:/app/.env -v $(pwd)/config:/app/config -v $(pwd)/rq1:/app/rq1 \
  madnanrizqu/td-python-prompt-eval poetry run python rq1/run_all.py --folders human_eval_chatgpt4o
```

**Interactive shell:**

```bash
docker run -it -v $(pwd)/.env:/app/.env -v $(pwd)/config:/app/config -v $(pwd)/rq1:/app/rq1 -v $(pwd)/rq2:/app/rq2 \
  madnanrizqu/td-python-prompt-eval /bin/bash
```

## Volume Mounts (Required)

| Mount | Purpose | Required |
|-------|---------|----------|
| `-v $(pwd)/.env:/app/.env` | API keys | ✅ Always |
| `-v $(pwd)/config:/app/config` | Use your config changes | ✅ Recommended |
| `-v $(pwd)/rq1:/app/rq1` | Save RQ1 results | ✅ To persist results |
| `-v $(pwd)/rq2:/app/rq2` | Save RQ2 results | ✅ To persist results |

**⚠️ Without mounting `rq1/` or `rq2/`, results are lost when container stops!**

## Configuration

Edit config files on your host machine and they're immediately used by the container:

```bash
# 1. Edit config
nano config/rq1.py  # Change LLM_TO_USE, RATIO_OF_ROWS_TO_RUN, etc.

# 2. Run (your changes are automatically used)
docker run -v $(pwd)/.env:/app/.env -v $(pwd)/config:/app/config -v $(pwd)/rq1:/app/rq1 \
  madnanrizqu/td-python-prompt-eval poetry run python rq1/run_all.py
```

## Troubleshooting

**Permission issues:**

```bash
docker run --user $(id -u):$(id -g) -v $(pwd)/.env:/app/.env -v $(pwd)/rq1:/app/rq1 \
  madnanrizqu/td-python-prompt-eval poetry run python rq1/run_all.py
```

**Rebuild after code changes:**

```bash
docker build --no-cache -t madnanrizqu/td-python-prompt-eval .
```
