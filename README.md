# Prompting Techniques for Legal LLMs

An interactive application showcasing advanced prompting techniques for legal professionals working with Large Language Models (LLMs).

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/arthrod/prompting)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/arthrod/prompting)

## About

This application provides a comprehensive guide to various legal-focused prompting techniques for LLMs, helping legal professionals get better responses for their work. The app includes:

- Interactive examples with bad and good prompts for legal contexts
- Detailed explanations of why each technique works
- Real-time LLM response testing through a direct API connection
- Multilingual support (English and Portuguese)

### The 10 Prompting Techniques

1. **Role-Based Prompting (Persona Priming)** - Assigning the AI a specific legal role or expertise
2. **Context-Rich Prompting** - Including detailed legal background and jurisdictional information
3. **Constraint-Based Prompting** - Setting conditional and focused instructions for legal analysis
4. **Example-Based Prompting (Few-Shot Learning)** - Providing examples of desired outputs for consistent formats
5. **Step-by-Step Prompting (Chain-of-Thought Legal Reasoning)** - Breaking down complex legal analysis
6. **Extracting Key Provisions and Data from Contracts** - Targeted extraction techniques
7. **Master Service Agreement Clause Drafting and Refinement** - Specialized contract drafting methods
8. **Handling Ambiguity and Multiple Interpretations** - Analyzing legal uncertainties
9. **Comparative Law Analysis Across Jurisdictions** - Cross-jurisdictional legal analysis methods
10. **Recency Bias (Le Gran Finale)** - Strategic placement of critical instructions at the end of prompts

## Running the Application

You can run the application in several ways:

### Local Installation

```bash
# Using make (recommended)
# will install uv and construct the virtual environment based on the pyproject.toml file
make run

# Or using uv directly (assuming it is installed)
uv venv
uv sync --install --all-packages
uv run marimo run app.py
```

### Using the DevContainer

This repository includes a DevContainer configuration for VS Code and GitHub Codespaces:

1. Open the repository in VS Code with the DevContainer extension or GitHub Codespaces
2. The environment will be automatically set up
3. Run the application with:
   ```bash
   make run
   ```

### Docker Deployment

This application uses Marimo's official Docker container, making deployment simple and reliable:

#### Using Docker Compose (Recommended)
```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f
```

#### Using Docker Directly
```bash
# Build the Docker image
docker build -t legal-prompting-app .

# Run the container
docker run -p 8080:8080 legal-prompting-app
```

#### Using GitHub Container Registry
After pushing to GitHub, the application is automatically built and published to GitHub Container Registry:

```bash
# Pull the latest image
docker pull ghcr.io/arthrod/prompting:main

# Run the container
docker run -p 8080:8080 ghcr.io/arthrod/prompting:main
```

Access the application at https://prompting.synthetic.lawyer after deployment.

> **Note:** The port exposure (`-p 8080:8080` or the `ports` section in docker-compose.yml) is necessary for browser access to the application. The container internally runs on port 8080, and this mapping makes it accessible at the same port on your host machine.

#### Development with Docker

For development with live code changes, use the volume mount in docker-compose.yml:

```bash
# Start the container with mounted volumes
docker-compose up -d

# Make changes to your local files and they'll be reflected in the running app
```

## Development

### Project Structure

- `app.py`: Main application file with all cells defining the interactive UI
- `layouts/app.slides.json`: Layout definition for the UI
- `custom.css`: Custom styling for the application
- `Dockerfile`: Uses Marimo's official container as a base
- `docker-compose.yml`: Multi-container Docker configuration with development support

### Dependencies

This project requires:
- Python 3.12+
- Marimo 0.11.17+
- HTTPX for API communication
- Various libraries for data visualization and manipulation

All dependencies are managed through `pyproject.toml` and installed using `uv sync --all-packages`.

## Roadmap

### English
- Complete Portuguese translations for all techniques
- Add advanced prompting templates specific to different legal practice areas
- Integrate with more LLM providers
- Add export functionality for generated prompts
- Create a companion CLI tool for quick prompt generation

### Português
- Completar traduções em português para todas as técnicas
- Adicionar modelos avançados de prompts específicos para diferentes áreas do direito
- Integrar com mais provedores de LLM
- Adicionar funcionalidade de exportação para prompts gerados
- Criar uma ferramenta CLI para geração rápida de prompts

## Special Thanks

A special thank you to [Thomas Schmelzer](https://github.com/tschm) for his invaluable contributions and for helping me fix some of my "noob" mistakes. His expertise and guidance have been instrumental in improving this project.

## Author

- Arthur Souza Rodrigues (arthrod@umich.edu)

## License

MIT License
