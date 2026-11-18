import pandas as pd
import pytest

import database
import insert_data
import transform_data
from transform_data import (
    encode_phone_number,
    transform_emails,
    transform_phone_numbers,
    transform_postal_codes,
)
from transform_data import (
    transform_data as apply_transformations,
)


def test_transform_emails():
    dataframe = pd.DataFrame({
        "email": [
            "alice@gmail.com",
            "brian@yahoo.com",
            "carla@outlook.com"
        ]
    })

    result = transform_emails(dataframe)

    assert result["email"].tolist() == [
        "alice@gmail.com",
        "brian@gmail.com",
        "carla@gmail.com"
    ]


def test_transform_postal_codes():
    dataframe = pd.DataFrame({
        "postalZip": [
            "94103",
            60614,
            "M5V-3A8",
            "SW1A1AA"
        ]
    })

    result = transform_postal_codes(dataframe)

    assert result["postalZip"].tolist() == [
        94103,
        60614,
        538,
        11
    ]

    assert str(result["postalZip"].dtype) == "int64"


def test_encode_phone_number():
    assert encode_phone_number("(816) 530-4269") == "QAOOE"
    assert encode_phone_number("1-811-920-9732") == "OO\\OI"
    assert encode_phone_number("123") == "O"
    assert encode_phone_number("99") == "c"
    assert encode_phone_number("64") == "O"


def test_transform_phone_numbers():
    dataframe = pd.DataFrame({
        "phone": [
            "(816) 530-4269",
            "1-811-920-9732"
        ]
    })

    result = transform_phone_numbers(dataframe)

    assert "coded_phone_number" in result.columns
    assert "phone" not in result.columns

    assert result["coded_phone_number"].tolist() == [
        "QAOOE",
        "OO\\OI"
    ]


def test_transform_data():
    dataframe = pd.DataFrame({
        "id": [1, 2],
        "name": ["Alice Chen", "Brian Osei"],
        "email": [
            "alice@yahoo.com",
            "brian@hotmail.com"
        ],
        "postalZip": ["94103", "M5V-3A8"],
        "phone": [
            "(816) 530-4269",
            "1-811-920-9732"
        ]
    })

    result = apply_transformations(dataframe)

    assert result["email"].tolist() == [
        "alice@gmail.com",
        "brian@gmail.com"
    ]

    assert result["postalZip"].tolist() == [
        94103,
        538
    ]

    assert result["coded_phone_number"].tolist() == [
        "QAOOE",
        "OO\\OI"
    ]

    assert "phone" not in result.columns


def test_transform_data_does_not_modify_original():
    dataframe = pd.DataFrame({
        "id": [1],
        "name": ["Alice Chen"],
        "email": ["alice@yahoo.com"],
        "postalZip": ["M5V-3A8"],
        "phone": ["(816) 530-4269"]
    })

    original = dataframe.copy(deep=True)

    apply_transformations(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)


class FakeCursor:
    def __init__(self):
        self.rowcount = 10
        self.description = [
            ("id",),
            ("name",),
            ("email",),
            ("postalZip",),
            ("phone",)
        ]
        self.executed_query = None
        self.executed_data = None
        self.closed = False

    def executemany(self, query, data):
        self.executed_query = query
        self.executed_data = data

    def execute(self, query):
        self.executed_query = query

    def fetchall(self):
        return [
            (1, "Alice Chen", "alice@gmail.com", "94103", "1234567890"),
            (2, "Brian Osei", "brian@gmail.com", "60614", "1234567891")
        ]

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, cursor):
        self.fake_cursor = cursor
        self.committed = False
        self.closed = False

    def cursor(self):
        return self.fake_cursor

    def commit(self):
        self.committed = True

    def is_connected(self):
        return not self.closed

    def close(self):
        self.closed = True


def test_insert_data(monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        database.mysql.connector,
        "connect",
        lambda **kwargs: connection
    )

    insert_data.insert_data()

    assert cursor.executed_query is not None
    assert "INSERT INTO" in cursor.executed_query
    assert len(cursor.executed_data) == 10
    assert connection.committed is True
    assert cursor.closed is True
    assert connection.closed is True


def test_fetch_data(monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        database.mysql.connector,
        "connect",
        lambda **kwargs: connection
    )

    result = transform_data.fetch_data()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == [
        "id",
        "name",
        "email",
        "postalZip",
        "phone"
    ]
    assert cursor.closed is True
    assert connection.closed is True


def test_database_connection_closes(monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        database.mysql.connector,
        "connect",
        lambda **kwargs: connection
    )

    with database.get_db_connection() as db_connection:
        assert db_connection is connection
        assert connection.closed is False

    assert connection.closed is True


def test_database_connection_closes_on_exception(monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        database.mysql.connector,
        "connect",
        lambda **kwargs: connection
    )

    with pytest.raises(RuntimeError), database.get_db_connection():
        raise RuntimeError("Simulated operation failure")

    assert connection.closed is True
