import logging
import re
from pathlib import Path

import pandas as pd

from config import DB_TABLE
from database import get_db_connection

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger(__name__)


def configure_logging():
    """Configure logging to write to both file and console."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s - %(levelname)s - "
            "%(name)s - %(message)s"
        ),
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )


def fetch_data():
    """Fetch records from MySQL and return a pandas DataFrame."""
    query = f"SELECT * FROM `{DB_TABLE}`"

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            try:
                cursor.execute(query)

                rows = cursor.fetchall()
                columns = [
                    column[0] for column in cursor.description
                ]

            finally:
                cursor.close()

        dataframe = pd.DataFrame(rows, columns=columns)

        logger.info(
            "Fetched %d records from MySQL.",
            len(dataframe)
        )

        return dataframe

    except Exception:
        logger.exception("Failed to fetch records from MySQL.")
        raise


def transform_emails(dataframe):
    """Replace every email domain with gmail.com."""
    dataframe["email"] = dataframe["email"].str.replace(
        r"@.*$",
        "@gmail.com",
        regex=True
    )

    return dataframe


def transform_postal_codes(dataframe):
    """Remove non-digits and convert postal codes to integers."""
    dataframe["postalZip"] = dataframe["postalZip"].apply(
        lambda value: re.sub(r"\D", "", str(value))
    )

    dataframe["postalZip"] = pd.to_numeric(
        dataframe["postalZip"],
        errors="raise"
    ).astype("int64")

    return dataframe


def encode_phone_number(phone):
    """Encode phone digits in pairs using ASCII character conversion."""
    digits = "".join(
        character for character in str(phone)
        if character.isdigit()
    )

    encoded_phone = ""

    for index in range(0, len(digits) - 1, 2):
        pair = int(digits[index:index + 2])

        if 65 <= pair <= 99:
            encoded_phone += chr(pair)
        else:
            encoded_phone += "O"

    return encoded_phone


def transform_phone_numbers(dataframe):
    """Encode phone numbers and rename the output column."""
    dataframe["phone"] = dataframe["phone"].apply(
        encode_phone_number
    )

    dataframe = dataframe.rename(
        columns={"phone": "coded_phone_number"}
    )

    return dataframe


def transform_data(dataframe):
    """Apply all required transformations."""
    dataframe = dataframe.copy()

    dataframe = transform_emails(dataframe)
    dataframe = transform_postal_codes(dataframe)
    dataframe = transform_phone_numbers(dataframe)

    logger.info("All data transformations completed.")

    return dataframe


def main():
    configure_logging()

    original_data = fetch_data()

    print("\nOriginal data:")
    print(original_data.to_string(index=False))

    transformed_data = transform_data(original_data)

    print("\nTransformed data:")
    print(transformed_data.to_string(index=False))

    print("\nData types:")
    print(transformed_data.dtypes)


if __name__ == "__main__":
    main()
