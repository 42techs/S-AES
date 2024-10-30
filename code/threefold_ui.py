import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget,
    QTextEdit, QStackedWidget
)
from code.threefold import triple_encrypt, triple_decrypt  # 确保这里可以找到三重加密解密函数

class SAESApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("S-AES 三重加密系统")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            background-color: #f7f7f9;
            color: #333;
            font-family: Arial;
        """)

        self.stacked_widget = QStackedWidget()

        self.encrypt_widget = QWidget()
        self.create_encrypt_ui()

        self.decrypt_widget = QWidget()
        self.create_decrypt_ui()

        self.stacked_widget.addWidget(self.encrypt_widget)
        self.stacked_widget.addWidget(self.decrypt_widget)

        self.switch_button_layout = QHBoxLayout()
        self.encrypt_button = QPushButton("加密")
        self.decrypt_button = QPushButton("解密")

        for button in [self.encrypt_button, self.decrypt_button]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 14px;
                    padding: 10px 20px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        self.encrypt_button.clicked.connect(self.show_encrypt)
        self.decrypt_button.clicked.connect(self.show_decrypt)
        
        self.switch_button_layout.addWidget(self.encrypt_button)
        self.switch_button_layout.addWidget(self.decrypt_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.switch_button_layout)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def create_encrypt_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("三重加密工具", font=QtGui.QFont("Arial", 16)))

        self.plaintext_entry = QLineEdit()
        self.plaintext_entry.setPlaceholderText("明文 (16位二进制)")
        self.plaintext_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.plaintext_entry)

        self.key1_entry = QLineEdit()
        self.key1_entry.setPlaceholderText("密钥1 (16位二进制)")
        self.key1_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.key1_entry)

        self.key2_entry = QLineEdit()
        self.key2_entry.setPlaceholderText("密钥2 (16位二进制)")
        self.key2_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.key2_entry)

        self.encrypt_button = QPushButton("三重加密")
        self.encrypt_button.setFont(QtGui.QFont("Arial", 12))
        self.encrypt_button.clicked.connect(self.encrypt_text)
        layout.addWidget(self.encrypt_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFixedHeight(100)
        self.result_text.setFont(QtGui.QFont("Arial", 12))
        self.result_text.setStyleSheet("""
            background-color: #e8e8e8;
            color: #333;
            padding: 10px;
            border-radius: 8px;
        """)
        layout.addWidget(self.result_text)

        self.encrypt_widget.setLayout(layout)

    def create_decrypt_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("三重解密工具", font=QtGui.QFont("Arial", 16)))

        self.ciphertext_entry = QLineEdit()
        self.ciphertext_entry.setPlaceholderText("密文 (16位二进制)")
        self.ciphertext_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.ciphertext_entry)

        self.key1_entry_decrypt = QLineEdit()
        self.key1_entry_decrypt.setPlaceholderText("密钥1 (16位二进制)")
        self.key1_entry_decrypt.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.key1_entry_decrypt)

        self.key2_entry_decrypt = QLineEdit()
        self.key2_entry_decrypt.setPlaceholderText("密钥2 (16位二进制)")
        self.key2_entry_decrypt.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.key2_entry_decrypt)

        self.decrypt_button = QPushButton("三重解密")
        self.decrypt_button.setFont(QtGui.QFont("Arial", 12))
        self.decrypt_button.clicked.connect(self.decrypt_text)
        layout.addWidget(self.decrypt_button)

        self.result_text_decrypt = QTextEdit()
        self.result_text_decrypt.setReadOnly(True)
        self.result_text_decrypt.setFixedHeight(100)
        self.result_text_decrypt.setFont(QtGui.QFont("Arial", 12))
        self.result_text_decrypt.setStyleSheet("""
            background-color: #e8e8e8;
            color: #333;
            padding: 10px;
            border-radius: 8px;
        """)
        layout.addWidget(self.result_text_decrypt)

        self.decrypt_widget.setLayout(layout)

    def show_encrypt(self):
        self.stacked_widget.setCurrentWidget(self.encrypt_widget)

    def show_decrypt(self):
        self.stacked_widget.setCurrentWidget(self.decrypt_widget)

    def encrypt_text(self):
        plaintext = self.plaintext_entry.text()
        key1 = self.key1_entry.text()
        key2 = self.key2_entry.text()

        if len(key1) != 16 or not all(k in '01' for k in key1):
            self.result_text.setPlainText("错误: 密钥1必须是16位二进制字符串！")
            return

        if len(key2) != 16 or not all(k in '01' for k in key2):
            self.result_text.setPlainText("错误: 密钥2必须是16位二进制字符串！")
            return

        if len(plaintext) != 16 or not all(bit in '01' for bit in plaintext):
            self.result_text.setPlainText("错误: 明文必须是16位二进制字符串！")
            return

        ciphertext = triple_encrypt(plaintext, key1, key2)
        self.result_text.setPlainText("密文: " + ciphertext)

    def decrypt_text(self):
        ciphertext = self.ciphertext_entry.text()
        key1 = self.key1_entry_decrypt.text()
        key2 = self.key2_entry_decrypt.text()

        if len(key1) != 16 or not all(k in '01' for k in key1):
            self.result_text_decrypt.setPlainText("错误: 密钥1必须是16位二进制字符串！")
            return

        if len(key2) != 16 or not all(k in '01' for k in key2):
            self.result_text_decrypt.setPlainText("错误: 密钥2必须是16位二进制字符串！")
            return

        if len(ciphertext) != 16 or not all(bit in '01' for bit in ciphertext):
            self.result_text_decrypt.setPlainText("错误: 密文必须是16位二进制字符串！")
            return

        plaintext = triple_decrypt(ciphertext, key1, key2)
        self.result_text_decrypt.setPlainText("明文: " + plaintext)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SAESApp()
    window.show()
    sys.exit(app.exec_())
