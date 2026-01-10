#!/bin/bash

# UV environment setup and Jupyter kernel registration script (pyproject.toml based)
# Usage: ./create-uv-env.sh <env_name> [python_version]

set -e  # Stop script on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions: Output messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print usage
usage() {
    echo "Usage: $0 <env_name> [python_version]"
    echo ""
    echo "Examples:"
    echo "  $0 interactive-analysis"
    echo "  $0 interactive-analysis 3.12"
    echo ""
    echo "Options:"
    echo "  env_name       : Name of the environment to create (required)"
    echo "  python_version : Python version to use (optional, default: 3.12)"
    exit 1
}

# Validate arguments
if [ $# -lt 1 ]; then
    print_error "Environment name is required."
    usage
fi

ENV_NAME=$1
PYTHON_VERSION=${2:-3.12}
VENV_PATH=".venv"

print_info "Starting environment setup..."
print_info "Environment name: $ENV_NAME"
print_info "Python version: $PYTHON_VERSION"
print_info "Virtual environment path: $VENV_PATH"

# Clean up existing virtual environment
if [ -d "$VENV_PATH" ]; then
    print_warning "Removing existing virtual environment: $VENV_PATH"
    rm -rf .venv
    print_success "Existing virtual environment removed."
fi

# Check and auto-install UV
install_uv() {
    print_info "Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

    if [ -f "$HOME/.local/bin/env" ]; then
        source "$HOME/.local/bin/env"
    fi

    if command -v uv &> /dev/null; then
        print_success "UV installed successfully!"
        uv --version
    else
        print_error "UV installation failed."
        exit 1
    fi
}

if ! command -v uv &> /dev/null; then
    print_warning "UV is not installed."
    read -p "Would you like to install UV automatically? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_uv
    else
        print_error "UV is required. Please install it manually."
        exit 1
    fi
fi

# 1. Set Python version
print_info "Setting up Python $PYTHON_VERSION..."
uv python pin $PYTHON_VERSION
print_success "Python $PYTHON_VERSION has been set."

# 2. Initialize project
print_info "Initializing project..."
if [ ! -f "pyproject.toml" ]; then
    uv init --name "$ENV_NAME"
    print_success "Project initialized as '$ENV_NAME'."
else
    print_warning "pyproject.toml already exists. Using existing project."
fi

# 3. Add required packages
print_info "Adding Jupyter-related packages..."
uv add ipykernel jupyter

# 4. Check pyproject.toml and install dependencies
if [ -f "pyproject.toml" ]; then
    print_info "pyproject.toml found. Syncing dependencies..."
    uv sync
    print_success "Dependencies installed based on pyproject.toml."
else
    print_error "pyproject.toml not found."
    exit 1
fi

# 5. Register Jupyter kernel
print_info "Registering Jupyter kernel..."
DISPLAY_NAME="$ENV_NAME (UV)"

if jupyter kernelspec list 2>/dev/null | grep -q "$ENV_NAME"; then
    print_warning "Removing existing '$ENV_NAME' kernel..."
    jupyter kernelspec remove -f "$ENV_NAME" || {
        print_warning "Kernel removal failed, continuing..."
    }
fi

uv run python -m ipykernel install --user --name "$ENV_NAME" --display-name "$DISPLAY_NAME" || {
    print_error "Failed to register Jupyter kernel."
    exit 1
}
print_success "Jupyter kernel registered as '$DISPLAY_NAME'."

# 6. Verify installation
print_info "Verifying installation..."
echo ""
echo "=== Installed Python version ==="
uv run python --version

echo ""
echo "=== Installed packages ==="
uv pip list

echo ""
echo "=== Registered Jupyter kernels ==="
jupyter kernelspec list 2>/dev/null | grep -E "(Available|$ENV_NAME)" || echo "Could not retrieve kernel list."

# 7. Create symlinks in root directory
print_info "Linking UV environment files to root directory..."
cd ..

for file in pyproject.toml .venv uv.lock; do
    if [ -e "$file" ] && [ ! -L "$file" ]; then
        print_warning "Backing up existing $file to ${file}.backup"
        mv "$file" "${file}.backup"
    elif [ -L "$file" ]; then
        print_info "Removing existing symlink $file"
        rm "$file"
    fi
done

ln -s setup/pyproject.toml . || { print_error "Failed to create pyproject.toml symlink"; exit 1; }
ln -s setup/.venv . || { print_error "Failed to create .venv symlink"; exit 1; }
if [ -f "setup/uv.lock" ]; then
    ln -s setup/uv.lock . || { print_warning "Failed to create uv.lock symlink"; }
fi

print_success "UV environment files linked to root directory!"

echo ""
print_success "Environment setup completed!"
echo ""
echo "=== Usage ==="
echo "1. Add package: uv add <package_name>"
echo "2. Remove package: uv remove <package_name>"
echo "3. Sync dependencies: uv sync"
echo "4. Run script: uv run python <script.py>"
echo "5. Launch Jupyter Lab: uv run jupyter lab"
echo "6. Select '$DISPLAY_NAME' kernel when creating new notebooks"
echo ""
print_info "You can now run 'uv run python' from the root directory!"
