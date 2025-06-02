# Installation

## Requirements

- Python 3.10 or higher
- pip (Python package installer)
- Git (optional, for development)

## Installation Methods

### 1. Using pip (Recommended)

The easiest way to install Meine is through pip:

```bash
pip install meine
```

### 2. From Source

If you want the latest development version or plan to contribute:

```bash
# Clone the repository
git clone https://github.com/Balaji01-4D/meine
cd meine

# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Verifying Installation

After installation, verify that Meine is working correctly:

```bash
meine --version
```

You should see the version number of Meine displayed.

## Platform-Specific Notes

### Linux
- No additional requirements
- Full functionality available out of the box

### macOS
- Requires Python 3.10 or higher
- Terminal access required for full functionality

### Windows
- Requires Python 3.10 or higher
- Windows Terminal recommended for best experience
- Some system commands may have limited functionality

## Troubleshooting

If you encounter any issues during installation:

1. Ensure Python version is 3.10 or higher:
   ```bash
   python --version
   ```

2. Update pip to the latest version:
   ```bash
   pip install --upgrade pip
   ```

3. If you get permission errors:
   ```bash
   pip install --user meine
   ```

4. For virtual environment issues:
   ```bash
   python -m pip install virtualenv
   virtualenv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install meine
   ```

## Next Steps

- Read the [Getting Started](/guide/getting-started) guide
- Learn about [Basic Usage](/guide/basic-usage)
- Configure your [Settings](/guide/configuration)
