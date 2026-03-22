# Teresa Ferreira - Data Engineer Assessment

## Overview
This project automates the end-to-end process of identifying, downloading, and parsing ESMA's 'DLTINS' financial data files into a structured format.

## Tech Stack & Standards
- **Language:** Python 3.9+ 
- **Dependency Management:** `pyproject.toml` 
- **Code Quality:**
  - **Ruff:** Fast linting and formatting (enforcing PEP 8).
  - **Mypy:** Strict static type checking for robust data handling.
- **Testing:** `pytest` for unit and functional testing.

## Installation and Environment Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:titf512/teresa-ferreira-data-engineer-assessment.git
   cd teresa-ferreira-data-engineer-assessment
   ```
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   #For macOS and Linux
   source .venv/bin/activate  
   #For Windows: 
   .venv\Scripts\activate
   ```

3. **Install the package and development tools**
   ```bash
    python3 -m pip install --upgrade pip setuptools wheel
    python3 -m pip install -e ".[dev]"
   ```


## Development Workflow

To maintain some standards required for this assessment, I've decided to use the following commands before committing code:

### Ruff:
Ensures code follows professional style guides and includes mandatory documentation. Enforces PEP 8:
   ```bash
    python3 -m ruff check .  
   ```

### Mypy:
Verifies that type hints are consistent throughout the pipeline:
   ```bash
   python3 -m mypy .  
   ```

### Running Tests
Executes the automated test suite:
   ```bash
   python3 -m pytest .  
   ```

## Project Structure
- src/firds/: Core package containing the ETL logic.
- tests/: Unit tests and sample XML data for mocking.
- pyproject.toml: The "Source of Truth" for project metadata and tool configuration.
