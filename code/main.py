import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget,
    QComboBox, QTextEdit, QStackedWidget
)
from s_aes import encrypt, decrypt, encrypt_ascii, decrypt_ascii

class SAESApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("S-AES 加解密系统")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.stacked_widget = QStackedWidget()

        self.encrypt_widget = QWidget()
        self.create_encrypt_ui()

        self.decrypt_widget = QWidget()
        self.create_decrypt_ui()

        self.stacked_widget.addWidget(self.encrypt_widget)
        self.stacked_widget.addWidget(self.decrypt_widget)

        # 切换按钮
        self.switch_button_layout = QHBoxLayout()
        self.encrypt_button = QPushButton("加密")
        self.encrypt_button.clicked.connect(self.show_encrypt)
        self.decrypt_button = QPushButton("解密")
        self.decrypt_button.clicked.connect(self.show_decrypt)

        self.switch_button_layout.addWidget(self.encrypt_button)
        self.switch_button_layout.addWidget(self.decrypt_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.switch_button_layout)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def create_encrypt_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("S-AES加密工具", font=QtGui.QFont("Arial", 16)))

        self.plaintext_entry = QLineEdit()
        self.plaintext_entry.setPlaceholderText("明文")
        self.plaintext_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.plaintext_entry)

        self.key_entry = QLineEdit()
        self.key_entry.setPlaceholderText("密钥 (16位)")
        self.key_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.key_entry)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["ASCII", "二进制"])
        layout.addWidget(self.format_combo)

        self.encrypt_button = QPushButton("加密")
        self.encrypt_button.setFont(QtGui.QFont("Arial", 12))
        self.encrypt_button.clicked.connect(self.encrypt_text)
        layout.addWidget(self.encrypt_button)

        self.result_text = QTextEdit()
        self.result_text.setFixedHeight(100)
        self.result_text.setFont(QtGui.QFont("Arial", 12))
        self.result_text.setStyleSheet("background-color: #e0e0e0;")
        layout.addWidget(self.result_text)

        self.encrypt_widget.setLayout(layout)

    def create_decrypt_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("解密工具", font=QtGui.QFont("Arial", 16)))

        self.ciphertext_entry = QLineEdit()
        self.ciphertext_entry.setPlaceholderText("密文")
        self.ciphertext_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.ciphertext_entry)

        self.key_entry_decrypt = QLineEdit()
        self.key_entry_decrypt.setPlaceholderText("密钥 (16位)")
        self.key_entry_decrypt.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.key_entry_decrypt)

        self.format_combo_decrypt = QComboBox()
        self.format_combo_decrypt.addItems(["ASCII", "二进制"])
        layout.addWidget(self.format_combo_decrypt)

        self.decrypt_button = QPushButton("解密")
        self.decrypt_button.setFont(QtGui.QFont("Arial", 12))
        self.decrypt_button.clicked.connect(self.decrypt_text)
        layout.addWidget(self.decrypt_button)

        self.result_text_decrypt = QTextEdit()
        self.result_text_decrypt.setFixedHeight(100)
        self.result_text_decrypt.setFont(QtGui.QFont("Arial", 12))
        self.result_text_decrypt.setStyleSheet("background-color: #e0e0e0;")
        layout.addWidget(self.result_text_decrypt)

        self.decrypt_widget.setLayout(layout)

    def show_encrypt(self):
        self.stacked_widget.setCurrentWidget(self.encrypt_widget)

    def show_decrypt(self):
        self.stacked_widget.setCurrentWidget(self.decrypt_widget)

    def encrypt_text(self):
        plaintext = self.plaintext_entry.text()
        key = self.key_entry.text()

        if len(key) != 16 or not all(k in '01' for k in key):
            self.result_text.setPlainText("错误: 密钥必须是16位二进制字符串！")
            return

        if self.format_combo.currentText() == "二进制":
            if not all(bit in '01' for bit in plaintext) or len(plaintext) != 16:
                self.result_text.setPlainText("错误: 明文必须是16位二进制字符串！")
                return
            ciphertext = encrypt(plaintext, key)  
        else:
            ciphertext = encrypt_ascii(plaintext, key)  

        self.result_text.setPlainText("密文: " + ciphertext)

    def decrypt_text(self):
        ciphertext = self.ciphertext_entry.text()
        key = self.key_entry_decrypt.text()

        if len(key) != 16 or not all(k in '01' for k in key):
            self.result_text_decrypt.setPlainText("错误: 密钥必须是16位二进制字符串！")
            return

        if self.format_combo_decrypt.currentText() == "二进制":
            if not all(bit in '01' for bit in ciphertext) or len(ciphertext) != 16:
                self.result_text_decrypt.setPlainText("错误: 密文必须是16位二进制字符串！")
                return
            plaintext = decrypt(ciphertext, key)  
        else:
            plaintext = decrypt_ascii(ciphertext, key)  

        self.result_text_decrypt.setPlainText("明文: " + plaintext)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SAESApp()
    window.show()
    sys.exit(app.exec_())
