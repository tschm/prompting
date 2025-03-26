FROM ghcr.io/marimo-team/marimo:latest

WORKDIR /app

# Install uv for better dependency management
RUN pip install -U uv

# Copy project files (copies the prompting folder)
COPY . .

# Install project dependencies using uv sync
RUN uv sync --install --all-packages

# Create necessary directories
RUN mkdir -p data

# Expose the port the app runs on
EXPOSE 8080

# Command to run the app
CMD ["marimo", "run", "prompting/app.py", "--no-token", "--port", "8080", "--host", "0.0.0.0"]
