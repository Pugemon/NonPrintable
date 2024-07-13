# NonPrintableEncoder

NonPrintableEncoder is a utility class for encoding and decoding hidden byte data within a string using non-printable UTF-8 characters. 

## Features

- Encode and embed dictionary data within a string.
- Extract and decode hidden byte data from a string.
- Simple obfuscation method using non-printable UTF-8 characters.

## Important Note

This encoding method is not secure and should not be used for any cryptographic purposes. It can be easily reversed and is intended only for simple obfuscation.

## Installation

To use NonPrintableEncoder, you need to have Python installed along with the `cbor2` library. You can install `cbor2` using pip:

```sh
pip install cbor2
```

## Usage

```python
from NonPrintableEncoder import NonPrintableEncoder

original_text = "This is a test"
data_to_encode = {"key1": "value1", "key2": 2}

# Encoding
encoded_string = NonPrintableEncoder.encode_dict(original_text, data_to_encode)
print(f"Encoded string: {encoded_string}")

# Decoding
decoded_text, decoded_data = NonPrintableEncoder.decode_dict(encoded_string)
print(f"Decoded text: {decoded_text}")
print(f"Decoded data: {decoded_data}")

assert original_text == decoded_text, "The decoded text does not match the original text."
assert data_to_encode == decoded_data, "The decoded data does not match the original data."
```

