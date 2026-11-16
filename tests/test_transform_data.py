import pandas as pd

from transform_data import (
    encode_phone_number,
    transform_data,
    transform_emails,
    transform_phone_numbers,
    transform_postal_codes,
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

    result = transform_data(dataframe)

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

    transform_data(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)
