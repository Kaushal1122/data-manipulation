import logging

from config import DB_TABLE
from database import get_db_connection

logger = logging.getLogger(__name__)


DATA = {
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


def insert_data():
    columns = DATA["cols"]
    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join(f"`{column}`" for column in columns)

    query = (
        f"INSERT INTO `{DB_TABLE}` "
        f"({column_names}) VALUES ({placeholders})"
    )

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            try:
                cursor.executemany(query, DATA["data"])
                connection.commit()

                logger.info(
                    "Successfully inserted %d records.",
                    cursor.rowcount
                )

            finally:
                cursor.close()

    except Exception:
        logger.exception("Failed to insert records.")
        raise


def main():
    insert_data()


if __name__ == "__main__":
    main()
