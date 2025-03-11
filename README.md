# Prompting Techniques for Legal LLMs

An interactive application showcasing advanced prompting techniques for legal professionals working with Large Language Models (LLMs).

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/arthrod/prompting)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
# Create a virtual environment
uv venv

# Install dependencies
uv pip install -e ".[dev]"

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

## Roadmap

- Complete Portuguese translations for all techniques
- Add advanced prompting templates specific to different legal practice areas
- Integrate with more LLM providers
- Add export functionality for generated prompts
- Create a companion CLI tool for quick prompt generation

## Author

- Arthur Souza Rodrigues (arthrod@umich.edu)

## License

MIT License
