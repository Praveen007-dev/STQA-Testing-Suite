# 🚀 Automated REST API Testing Suite

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi)
![Playwright](https://img.shields.io/badge/Playwright-API_Testing-2EAD33?style=flat-square&logo=playwright)
![Pytest](https://img.shields.io/badge/Pytest-Testing_Framework-0A9EDC?style=flat-square&logo=pytest)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=flat-square)

This repository contains a complete, automated Software Testing and Quality Assurance (STQA) suite. It utilizes **Playwright's APIRequestContext** alongside **Pytest** to perform rigorous Black-Box and White-Box testing against a standalone Python FastAPI backend.

---

## 🎯 Assignment Rubric Fulfillment

This project is architected to strictly satisfy the STQA grading deliverables:

| Rubric Requirement | Implementation in this Project |
| :--- | :--- |
| **1. System Under Test (SUT)** | A non-trivial **E-commerce Cart REST API** (`main.py`) featuring dynamic calculations, floating-point math, strict inventory boundaries (max 50 items), and Pydantic data validation. |
| **2. Tool Setup** | Configured a completely automated Python CI pipeline (`pipeline.py`) that boots the server, attaches a coverage engine, executes tests, and safely shuts down. |
| **3. Test Design** | **15 distinct test cases** designed using Boundary Value Analysis, Equivalence Partitioning, and Error Guessing. |
| **4. Execution & Reporting** | Generates a custom `report.html` (Pass/Fail logs, assertion metrics, execution speed) and an `htmlcov` dashboard (100% line and branch coverage). |

---

## 📁 Repository Architecture

* `pipeline.py`: The CI/CD orchestrator. Runs the server, executes tests, and compiles reports in one command.
* `main.py`: The FastAPI backend (System Under Test) containing the target `/cart/add` endpoint.
* `test_api.py`: The Pytest suite containing all 15 Playwright API test cases.
* `conftest.py`: Pytest hooks that inject custom **Test Case ID** and **Description** columns into the HTML report.
* `pytest.ini`: Environment configuration for registering custom test markers.
* `.coveragerc`: Coverage engine configuration required to track asynchronous server threads.

---

## 🧪 Test Case Design & Scenarios

The test suite evaluates the SUT across four formal testing methodologies:

### 1. Functional Correctness (Happy Path)
* **TC-001:** Valid cart calculation (Subtotal + 10% Tax).
* **TC-002:** Floating-point precision accuracy.
* **TC-003:** Handling of zero-price promotional items.

### 2. Boundary Value Analysis (BVA)
* **TC-004:** Lower boundary accepted (Quantity = 1).
* **TC-005:** Absolute zero rejected (Quantity = 0).
* **TC-006:** Exact upper boundary accepted (Quantity = 50).
* **TC-007:** Just above upper boundary rejected (Quantity = 51).
* **TC-008:** Extreme high quantity rejected (Quantity = 99999).

### 3. Edge Cases & Error Guessing (Equivalence Partitioning)
* **TC-009:** Negative quantities rejected.
* **TC-010:** Missing required `price` field.
* **TC-011:** Missing required `item_id` field.
* **TC-012:** Missing required `quantity` field.
* **TC-013:** Invalid data type (String passed to Integer field).
* **TC-014:** Invalid data type (String passed to Float field).

### 4. Non-Functional Testing (Performance)
* **TC-015:** Load benchmarking (Executes 50 sequential POST requests; asserts average response time remains under 100ms).

---

## ⚙️ Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/Praveen007-dev/STQA-Testing-Suite.git
cd STQA-Testing-Suite
```

**2. Create and activate a virtual environment:**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
```

**3. Install the testing dependencies:**
```bash
pip install fastapi "uvicorn[standard]" pytest-playwright pytest-html pytest-cov coverage
```

**4. Initialize Playwright:**
```bash
playwright install chromium
```

---

## 🚀 One-Click Execution Pipeline

To run the entire testing suite, simply execute the orchestrator script from your terminal:

```bash
python pipeline.py
```

### What happens under the hood?
1. `pipeline.py` starts the FastAPI server in the background, attaching the `coverage` engine to track asynchronous threads.
2. It triggers `pytest`, which utilizes Playwright to fire HTTP requests at the live local server.
3. Upon test completion, it pings a hidden `/shutdown` endpoint, triggering a graceful `SIGINT` shutdown so the `.coverage` file is securely written to disk.
4. It compiles the raw data into visually readable HTML reports.

---

## 📊 Generated Deliverables

Upon a successful pipeline run, the script outputs two files directly into your root directory:

1. **`report.html`**: The Execution & Assertions Report. Open this in any browser to view a detailed table of executed tests, their pass/fail status, descriptions, and execution speed in milliseconds.
2. **`htmlcov/index.html`**: The White-Box Coverage Dashboard. Open this to verify that the test suite achieved 100% Line and Branch coverage across the SUT's backend logic.