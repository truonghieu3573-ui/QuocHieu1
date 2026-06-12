import math


class TranspositionCipher:
    def __init__(self):
        pass

    def _validate_key(self, key):
        try:
            key = int(key)
        except (TypeError, ValueError):
            raise ValueError("Key phải là số nguyên")

        if key <= 0:
            raise ValueError("Key phải lớn hơn 0")

        return key

    def encrypt(self, text, key):
        key = self._validate_key(key)

        if text is None:
            text = ""

        encrypted_text = ""

        # Ghi bản rõ theo từng hàng có độ dài = key,
        # sau đó đọc theo từng cột từ trái sang phải.
        for col in range(key):
            pointer = col

            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key

        return encrypted_text

    def decrypt(self, text, key):
        key = self._validate_key(key)

        if text is None:
            text = ""

        if text == "":
            return ""

        num_cols = key
        num_rows = math.ceil(len(text) / key)
        shaded_boxes = (num_cols * num_rows) - len(text)

        plain_text = [""] * num_rows

        col = 0
        row = 0

        # Bản mã được đọc theo cột, nên khi giải mã ta đổ ký tự
        # ngược lại vào ma trận theo cột rồi đọc từng hàng.
        for symbol in text:
            plain_text[row] += symbol
            row += 1

            if (row == num_rows) or (
                row == num_rows - 1 and col >= num_cols - shaded_boxes
            ):
                row = 0
                col += 1

        return "".join(plain_text)