# 1. Start from a lightweight, stable Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install the 'uv' package manager
RUN pip install uv

# 4. Copy *only* the dependency files first
# This is a Docker trick to speed up builds.
# This layer is only rebuilt if your dependencies change.
COPY pyproject.toml uv.lock ./

# 5. Install all project dependencies using uv
# --system installs them globally inside the container
RUN uv pip install --system -r pyproject.toml

# 6. Copy all your application code and model files
# This copies train.py, predict.py, serve.py, schemas.py, dv.bin, model.bin
COPY *.py *.bin ./

# 7. Tell Docker the port your application runs on
EXPOSE 8000

# 8. The command to run your API server
# We use "--host 0.0.0.0" to make it reachable from outside the container
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]