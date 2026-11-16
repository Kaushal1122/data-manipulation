import logging
from contextlib import contextmanager

import mysql.connector

from config import DB_CONFIG

logger = logging.getLogger(__name__)


@contextmanager
def get_db_connection():
    connection = None

    try:
        connection = mysql.connector.connect(
            **DB_CONFIG,
            use_pure=True
        )

        logger.info("MySQL connection established.")

        yield connection

    except mysql.connector.Error:
        logger.exception("MySQL database operation failed.")
        raise

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            logger.info("MySQL connection closed.")
