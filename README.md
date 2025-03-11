# Prompting Techniques for LLMs

An interactive application to learn and practice effective prompting techniques for Large Language Models.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/marimo_dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

This application provides a comprehensive guide to various prompting techniques for LLMs, including:

- Role-Based Prompting (Persona Priming)
- Multiple techniques for improving LLM responses
- Interactive examples with good and bad prompts
- Multilingual support (English and Portuguese)

## Running the Application

You can run the application in several ways:

### Local Installation

```bash
# Create a virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt

# Run the application
uv run marimo run app.py
```

### Using the DevContainer

This repository includes a DevContainer configuration for VS Code and GitHub Codespaces:

1. Open the repository in VS Code with the DevContainer extension or GitHub Codespaces
2. The environment will be automatically set up
3. Run the application with:
   ```bash
   uv run marimo run app.py
   ```

## Development

### Project Structure

- `app.py`: Main application file with all cells defining the interactive UI
- `layouts/app.slides.json`: Layout definition for the UI
- `custom.css`: Custom styling for the application

### Dependencies

This project requires:
- Python 3.12+
- Marimo 0.11.17+
- HTTPX for API communication
- Various libraries for data visualization and manipulation

## License

MIT License
