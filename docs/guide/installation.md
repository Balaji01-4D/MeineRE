# Installation

## Requirements

- Python 3.10 or higher
- pip (Python package installer)
- Git (optional, for development)

## Installation Methods

### 1. Using pip (Recommended)

The easiest way to install **Meine** is via pip:

```bash
pip install meine
````

### 2. From Source

To install the latest development version or contribute to the project:

```bash
# Clone the repository
git clone https://github.com/Balaji01-4D/meine
cd meine

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Verifying Installation

To confirm Meine is installed correctly:

```bash
meine --version
```

You should see the version number displayed in the output.

## Platform-Specific Notes

### Linux

* No additional dependencies
* Full functionality available out of the box

### macOS

* Python 3.10+ required
* Full functionality available via Terminal

### Windows

* Python 3.10+ required
* Use Windows Terminal for the best experience
* Some system commands may have limited support

## Troubleshooting

If you run into problems during installation:

1. **Check Python version**

   ```bash
   python --version
   ```

2. **Update pip**

   ```bash
   pip install --upgrade pip
   ```

3. **Fix permission errors**

   ```bash
   pip install --user meine
   ```

4. **Virtual environment issues**

   ```bash
   python -m pip install virtualenv
   virtualenv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install meine
   ```
   

