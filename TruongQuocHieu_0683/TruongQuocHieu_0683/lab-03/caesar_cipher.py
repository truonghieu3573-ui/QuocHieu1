import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"

        plain_text = self.ui.txt_vanban.toPlainText().strip()
        key = self.ui.txt_khoa.text().strip()

        if plain_text == "":
            QMessageBox.warning(
                self,
                "Thiếu dữ liệu",
                "Vui lòng nhập Plain Text cần mã hóa!"
            )
            return

        if key == "":
            QMessageBox.warning(
                self,
                "Thiếu dữ liệu",
                "Vui lòng nhập Key!"
            )
            return

        payload = {
            "plain_text": plain_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                encrypted_text = data.get("encrypted_text")

                if encrypted_text is None:
                    QMessageBox.warning(
                        self,
                        "Lỗi dữ liệu",
                        f"API không trả về encrypted_text.\nDữ liệu nhận được:\n{data}"
                    )
                    return

                self.ui.txt_mahoa.setText(encrypted_text)

                QMessageBox.information(
                    self,
                    "Thông báo",
                    "Mã hóa thành công!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Lỗi API",
                    f"Gọi API thất bại!\nStatus code: {response.status_code}\n{response.text}"
                )

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Lỗi kết nối",
                f"Không thể kết nối API.\nChi tiết lỗi: {e}"
            )

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"

        cipher_text = self.ui.txt_mahoa.toPlainText().strip()
        key = self.ui.txt_khoa.text().strip()

        if cipher_text == "":
            QMessageBox.warning(
                self,
                "Thiếu dữ liệu",
                "Vui lòng nhập CipherText cần giải mã!"
            )
            return

        if key == "":
            QMessageBox.warning(
                self,
                "Thiếu dữ liệu",
                "Vui lòng nhập Key!"
            )
            return

        payload = {
            "cipher_text": cipher_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                decrypted_text = data.get("decrypted_text")

                if decrypted_text is None:
                    QMessageBox.warning(
                        self,
                        "Lỗi dữ liệu",
                        f"API không trả về decrypted_text.\nDữ liệu nhận được:\n{data}"
                    )
                    return

                self.ui.txt_vanban.setText(decrypted_text)

                QMessageBox.information(
                    self,
                    "Thông báo",
                    "Giải mã thành công!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Lỗi API",
                    f"Gọi API thất bại!\nStatus code: {response.status_code}\n{response.text}"
                )

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Lỗi kết nối",
                f"Không thể kết nối API.\nChi tiết lỗi: {e}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())