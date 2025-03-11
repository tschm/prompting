#!/bin/bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv pip install --no-cache-dir -e ".[dev]"

# Create MIT License file if it doesn't exist
if [ ! -f "LICENSE" ]; then
    cat > LICENSE << 'EOL'
MIT License

Copyright (c) 2024 Arthur Souza Rodrigues

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOL
    echo "Created MIT LICENSE file"
fi

# Make sure layouts directory exists
mkdir -p prompting/layouts

# Create a .cursorrules file if it doesn't exist
if [ ! -f ".cursorrules" ]; then
    cat > .cursorrules << 'EOL'
# Cursor rules for Prompting Techniques App
# Maintained by Arthur Souza Rodrigues (arthrod@umich.edu)

# Python rules
glob:**/*.py
command:uv run ruff check --fix $FILE
command:uv run ruff format $FILE

# Marimo specific rules
glob:prompting/app.py
command:uv run marimo run $FILE

# TOML rules
glob:**/*.toml
format:true
EOL
    echo "Created .cursorrules file"
fi

# Setup git config if needed
if [ -z "$(git config --global user.email)" ]; then
    git config --global user.email "arthrod@umich.edu"
    git config --global user.name "Arthur Souza Rodrigues"
fi

# Setup pre-commit if applicable
if [ -f ".pre-commit-config.yaml" ]; then
    uv run pre-commit install
fi

echo "Setup complete! You can now run the app with: uv run marimo run app.py"
