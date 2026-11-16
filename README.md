# Data Manipulation

A Python project that inserts JSON-style records into a MySQL database, retrieves them using Pandas, and applies transformations to email addresses, postal codes, and phone numbers.

## Prerequisites

- Python 3.13
- MySQL 8.0+
- Git

## Dataset

The project uses the following dataset:

```python
{
    "cols": ["id", "name", "email", "postalZip", "phone"],
    "data": [
        [1, "Alice Chen", "alice.chen@gmail.com", "94103", "(816) 530-4269"],
        [2, "Brian Osei", "brian.osei@yahoo.com", 60614, "1-811-920-9732"],
        [3, "Carla Nunez", "carla.nunez@outlook.com", "M5V-3A8", "(212) 555-0148"],
        [4, "David Kim", "david.kim@hotmail.com", "10001", "1-408-555-0199"],
        [5, "Elena Petrova", "elena.petrova@icloud.com", 33101, "(305) 555-0176"],
        [6, "Farid Hassan", "farid.hassan@gmail.com", "SW1A1AA", "1-702-555-0123"],
        [7, "Grace Liu", "grace.liu@yahoo.com", "77002", "(617) 555-0110"],
        [8, "Hank Meyer", "hank.meyer@outlook.com", 98101, "1-206-555-0142"],
        [9, "Isabel Rossi", "isabel.rossi@gmail.com", "K1A0B1", "(415) 555-0187"],
        [10, "Jamal Walker", "jamal.walker@hotmail.com", "30301", "1-404-555-0165"]
    ]
}
```

## Transformations

The project performs the following transformations:

1. **Email:** Replaces every email domain with `gmail.com`.
2. **Postal code:** Removes all non-digit characters and converts the result to an integer.
3. **Phone number:** Extracts digits, processes them in pairs, and converts each pair to its corresponding ASCII character if its value is between 65 and 99 (inclusive). Otherwise, it replaces the pair with `O`. Any remaining unpaired digit is ignored.
4. **Column rename:** Renames `phone` to `coded_phone_number`.

## Transformed Output

```text
 id          name                   email  postalZip coded_phone_number
  1    Alice Chen    alice.chen@gmail.com      94103              QAOOE
  2    Brian Osei    brian.osei@gmail.com      60614              OO\OI
  3   Carla Nunez   carla.nunez@gmail.com        538              OOOOO
  4     David Kim     david.kim@gmail.com      10001              OOOOO
  5 Elena Petrova elena.petrova@gmail.com      33101              OOOOL
  6  Farid Hassan  farid.hassan@gmail.com         11              OOOOO
  7     Grace Liu     grace.liu@gmail.com      77002              OKOOO
  8    Hank Meyer    hank.meyer@gmail.com      98101              OOOOO
  9  Isabel Rossi  isabel.rossi@gmail.com        101              OOOOW
 10  Jamal Walker  jamal.walker@gmail.com      30301              OOOOO
```

### Data Types

```text
id                    int64
name                    str
email                   str
postalZip             int64
coded_phone_number      str
dtype: object
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Kaushal1122/data-manipulation.git
   cd data-manipulation
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create the MySQL database and table:

   ```sql
   CREATE DATABASE assignment_db;

   USE assignment_db;

   CREATE TABLE json_to_sql_table (
       id INT PRIMARY KEY,
       name VARCHAR(100),
       email VARCHAR(255),
       postalZip VARCHAR(50),
       phone VARCHAR(50)
   );
   ```

5. Copy `.env.example` to `.env` and configure your MySQL credentials.

## Run

Insert records into MySQL:

```bash
python insert_data.py
```

Run data transformations:

```bash
python transform_data.py
```

## Tests

Run unit tests:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=transform_data --cov-report=term-missing
```

## Code Quality

Run Ruff:

```bash
ruff check .
```

## Continuous Integration

GitHub Actions automatically runs Ruff and unit tests on pushes and pull requests. It generates HTML and XML coverage reports and uploads them as GitHub artifacts retained for 7 days.
