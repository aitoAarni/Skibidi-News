# Development Workflow

This document outlines the development workflow for this Python 3.13 project.

## Prerequisites

-   **Python 3.13+** installed on your system
-   **Git** for version control

## Initial Setup

### 1. Create Virtual Environment

**Linux/macOS:**

```bash
python3 -m venv venv
```

**Windows:**

```cmd
python -m venv venv
```

> **Note:** Use `python3` on Linux/macOS and `python` on Windows (assuming Python 3.13 is your default Python).

### 2. Activate Virtual Environment

**Linux/macOS:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

> **Success indicator:** You should see `(venv)` at the beginning of your command prompt.

### 3. Install Dependencies

```bash
# Install development dependencies (includes production dependencies)
pip install -r requirements-dev.txt
```

## Daily Development Workflow

### Starting Work Session

**Linux/macOS:**

```bash
cd <to this root dir>
source venv/bin/activate
```

**Windows:**

```cmd
cd <to this root dir>
venv\Scripts\activate
```

### Running the Application

```bash
python3 main.py
```

### Ending Work Session

```bash
deactivate
```

## Managing Dependencies

### Adding New Dependencies

#### 1. Activate Virtual Environment First

**Linux/macOS:**

```bash
source venv/bin/activate  # if not active
```

**Windows:**

```cmd
venv\Scripts\activate  # if not active
```

#### 2. Install the Package

```bash
pip install package-name
```

#### 3. Add to Requirements File

**For production dependencies (needed to run the app):**

```bash
# Linux/macOS
echo "package-name>=version" >> requirements.txt

# Windows (Command Prompt)
echo package-name>=version >> requirements.txt

# Windows (PowerShell)
Add-Content requirements.txt "package-name>=version"
```

#### 4. Example: Adding Requests Library

**Complete workflow:**

```bash
# Activate environment
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install requests
pip install requests

# Check installed version
pip show requests

# Add to requirements (replace X.X.X with actual version)
echo "requests>=2.31.0" >> requirements.txt

# Verify it's added
cat requirements.txt  # Linux/macOS
# or type requirements.txt  # Windows
```

### Installing Dependencies from Requirements

When you pull changes that include new dependencies:

```bash
# Activate environment if not active
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Update all dependencies
pip install -r requirements-dev.txt
```

### Viewing Installed Packages

```bash
pip list
```

### Removing a Package

```bash
pip uninstall package-name

# Don't forget to remove it from requirements.txt or requirements-dev.txt
```

## Quick Reference Commands

### Virtual Environment Management

| Action          | Linux/macOS                 | Windows                     |
| --------------- | --------------------------- | --------------------------- |
| Create venv     | `python3 -m venv venv`      | `python -m venv venv`       |
| Activate        | `source venv/bin/activate`  | `venv\Scripts\activate`     |
| Deactivate      | `deactivate`                | `deactivate`                |
| Check if active | Look for `(venv)` in prompt | Look for `(venv)` in prompt |

### Package Management

| Action                    | Command                               |
| ------------------------- | ------------------------------------- |
| Install package           | `pip install package-name`            |
| Install from requirements | `pip install -r requirements-dev.txt` |
| List packages             | `pip list`                            |
| Show package info         | `pip show package-name`               |
| Uninstall package         | `pip uninstall package-name`          |
| Upgrade package           | `pip install --upgrade package-name`  |

## Best Practices

1. **Always activate your virtual environment** before working on the project
2. **Update requirements files** immediately after installing new packages
3. **Use version pinning** (`package>=1.2.0`) in requirements files
4. **Never commit the `venv/` directory** to Git (it's in `.gitignore`)
5. **Deactivate** when switching to other projects
6. **Regular updates:** Periodically update your dependencies

## Quick Start Reminder

```bash
# Setup (once)
python3 -m venv venv                    # Linux/macOS
# or python -m venv venv                # Windows

# Daily workflow
source venv/bin/activate                # Linux/macOS
# or venv\Scripts\activate              # Windows
python -m src.main                      # Run app
deactivate                              # When done
```
