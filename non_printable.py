from typing import Optional, Tuple

import cbor2

UTF8_MASK = 0xE0000
HEADER = "\U000e0042\U000e0042\U000e0011\U000e0011"
"""
Unique header consisting of 4 non-printable UTF-8 characters.
"""
HEADER_LENGTH = len(HEADER)
"""
Cached header byte length for optimization and minimizing repeated computations.
"""


class NonPrintableEncoder:
    """
    Utility class to encode and decode hidden byte data within a string using non-printable UTF-8 characters.

    Note:
        This encoding method is not secure and should not be used for any cryptographic purposes.
        It can be easily reversed and is intended only for simple obfuscation.
    """

    @staticmethod
    def encode_dict(text: str, data: dict) -> str:
        """
        Encodes dict data and embeds it within a string, preserving the original text.

        Args:
            text (str): The text to embed the encoded data into.
            data (dict): The dict data to encode.

        Returns:
            str: The string with the encoded data embedded.
        """
        encoded_data = cbor2.dumps(data)
        return NonPrintableEncoder.encode(text, encoded_data)

    @staticmethod
    def decode_dict(encoded_string: str) -> Tuple[str, Optional[dict]]:
        """
        Extracts and decodes the hidden byte data from a string.

        Args:
            encoded_string (str): The string containing the hidden encoded data.

        Returns:
            Tuple[str, Optional[dict]]: A tuple containing the original text and the decoded dict data,
            or None if decoding fails.
        """
        try:
            text, dict_bytes = NonPrintableEncoder.decode(encoded_string)
            dict_data = cbor2.loads(dict_bytes)
        except (ValueError, cbor2.CBORDecodeError):
            text, dict_data = encoded_string, None
        return text, dict_data

    @staticmethod
    def encode(text: str, data: bytes) -> str:
        """
        Encodes byte data and embeds it within a string, preserving the original text.

        Args:
            data (bytes): The byte data to encode.
            text (str): The text to embed the encoded data into.

        Returns:
            str: The string with the encoded data embedded.
        """
        encoded_data = "".join(chr(UTF8_MASK + byte) for byte in data)
        return f"{text}{HEADER}{encoded_data}"

    @staticmethod
    def decode(encoded_string: str) -> Tuple[str, bytes]:
        """
        Extracts and decodes the hidden byte data from a string.

        Args:
            encoded_string (str): The string containing the hidden encoded data.

        Returns:
            Tuple[str, bytes]: A tuple containing the original text and the decoded byte data.

        Raises:
            ValueError: If the encoded string is in an incorrect format.
        """
        encoded_body_start = encoded_string.find(HEADER)
        if encoded_body_start == -1:
            raise ValueError(
                "Encoded string does not contain the expected header. Data may be corrupted or not encoded."
            )

        encoded_body_start += HEADER_LENGTH
        encoded_body = encoded_string[encoded_body_start:]
        byte_data = bytes((ord(char) - UTF8_MASK) for char in encoded_body)
        return encoded_string[: encoded_body_start - HEADER_LENGTH], byte_data


# Unit tests
if __name__ == "__main__":
    original_text = "This is a test"
    data_to_encode = {"key1": "value1", "key2": 2}

    # Encoding
    encoded_string = NonPrintableEncoder.encode_dict(original_text, data_to_encode)
    print(f"Encoded string: {encoded_string}")

    # Decoding
    decoded_text, decoded_data = NonPrintableEncoder.decode_dict(encoded_string)
    print(f"Decoded text: {decoded_text}")
    print(f"Decoded data: {decoded_data}")

    assert (
        original_text == decoded_text
    ), "The decoded text does not match the original text."
    assert (
        data_to_encode == decoded_data
    ), "The decoded data does not match the original data."
