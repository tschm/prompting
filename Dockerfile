FROM ghcr.io/marimo-team/marimo:latest

WORKDIR /app

# Copy project files
COPY . .

# Install project dependencies using uv
RUN pip install -e ".[dev]"

# Create necessary directories
RUN mkdir -p prompting/layouts data

# Expose the port the app runs on
EXPOSE 8080

# Command to run the app
CMD ["marimo", "run", "prompting/app.py", "--no-token", "--port", "8080", "--host", "0.0.0.0"] 