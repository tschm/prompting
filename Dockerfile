FROM python:3.13-slim

WORKDIR /app

# Install curl and other dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
COPY . .

# Create virtual environment and install dependencies
RUN /root/.cargo/bin/uv venv /app/.venv && \
    /root/.cargo/bin/uv pip install --no-cache-dir -e ".[dev]"

# Expose the port the app runs on
EXPOSE 8080

# Command to run the app
CMD ["/app/.venv/bin/python", "-m", "marimo", "run", "prompting/app.py", "--host=0.0.0.0", "--port=8080"] 