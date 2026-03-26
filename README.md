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
   
4. **Run the full pipeline**
    ```bash
    python3 src/main.py
    ```
   
5. **Run the tests**
    ```bash
    python3 -m pytest
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

## Pipeline Architecture
The project follows a modular **ETL (Extract, Transform, Load)** pattern:
1. **Extract:** `Extractor` downloads and unzips the latest DLTINS file from ESMA.
2. **Parse:** `Parser` uses `lxml.etree.iterparse` for memory-efficient XML processing.
3. **Transform:** `Transformer` uses `pandas` to calculate 'a' counts and apply the YES/NO flags.
4. **Load:** `Uploader` uses `fsspec` to push the final CSV to a destination (Local, S3, Azure).

## Branching Strategy & CI/CD

This project follows a structured branching and release model to ensure code stability, modular development, and automated delivery.

### Branch Hierarchy
* **`main`**: Production-ready code. Contains the latest stable release.
* **`develop`**: The primary integration branch where all new features are merged and tested together.
* **`feature/*`**: Short-lived branches created from `develop` for specific tasks, parsing logic, or refactoring.
* **`release/*`**: Dedicated branches created from `main` to prepare for a new production deployment. Cherry-Pick PR commits from development to bring new features to a release.

### Workflow & Release Logic
1.  **Feature Integration**: All work begins on `feature/` branches. Once development is complete and tests pass, a **Pull Request (PR)** is opened to merge into `develop`.
2.  **Release Preparation**: When a version is ready for production, a `release/` branch is branched off `main`. 
3.  **Selective Promotion (Cherry-picking)**: To maintain strict control over the release contents, specific commits and features are **cherry-picked** from `develop` into the `release/` branch. This prevents "release contamination" from unfinished features sitting in the develop branch.
4.  **Final Deployment**: Once the `release/` branch is validated, it is merged into `main`.

### Automation & Quality Gates
* **Automated Releases**: The project is configured for **Continuous Delivery**. Merging a Pull Request into the `main` branch triggers an automated release workflow (including version tagging).
* **Quality Checks**: Every PR to `develop` or `main` is subject to "Quality Gates." Merging is only permitted if the following pass:
    * **Ruff** (Linting & Formatting)
    * **Mypy** (Type Consistency)
    * **Pytest** (Unit & Functional Logic)