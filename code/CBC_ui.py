import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget,
    QTextEdit, QStackedWidget
)
from CBC import encrypt, decrypt, cbc_encrypt, cbc_decrypt  # 确保这里可以找到 CBC 相关函数

class CBCApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("S-AES CBC 加解密系统")
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
        layout.addWidget(QLabel("CBC 加密工具", font=QtGui.QFont("Arial", 16)))

        self.plaintext_entry = QLineEdit()
        self.plaintext_entry.setPlaceholderText("明文 (32位二进制)")
        self.plaintext_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.plaintext_entry)

        self.key_entry = QLineEdit()
        self.key_entry.setPlaceholderText("密钥 (16位二进制)")
        self.key_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.key_entry)

        self.iv_entry = QLineEdit()
        self.iv_entry.setPlaceholderText("初始向量 (16位二进制，随机生成将被忽略)")
        self.iv_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.iv_entry)

        self.encrypt_button = QPushButton("执行加密")
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
        layout.addWidget(QLabel("CBC 解密工具", font=QtGui.QFont("Arial", 16)))

        self.ciphertext_entry = QLineEdit()
        self.ciphertext_entry.setPlaceholderText("密文 (长度可变)")
        self.ciphertext_entry.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.ciphertext_entry)

        self.key_entry_decrypt = QLineEdit()
        self.key_entry_decrypt.setPlaceholderText("密钥 (16位二进制)")
        self.key_entry_decrypt.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.key_entry_decrypt)

        self.iv_entry_decrypt = QLineEdit()
        self.iv_entry_decrypt.setPlaceholderText("初始向量 (16位二进制)")
        self.iv_entry_decrypt.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.iv_entry_decrypt)

        self.decrypt_button = QPushButton("执行解密")
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
        key = self.key_entry.text()
        iv = self.iv_entry.text() or f"{random.randint(0, 0xFFFF):016b}"  # 随机 IV，如果未输入

        if len(key) != 16 or not all(k in '01' for k in key):
            self.result_text.setPlainText("错误: 密钥必须是16位二进制字符串！")
            return

        if len(plaintext) % 16 != 0 or not all(bit in '01' for bit in plaintext):
            self.result_text.setPlainText("错误: 明文必须是32位或16位的二进制字符串！")
            return

        ciphertext = cbc_encrypt(plaintext, key, iv)
        self.result_text.setPlainText("密文: " + ciphertext)

    def decrypt_text(self):
        ciphertext = self.ciphertext_entry.text()
        key = self.key_entry_decrypt.text()
        iv = self.iv_entry_decrypt.text()

        if len(key) != 16 or not all(k in '01' for k in key):
            self.result_text_decrypt.setPlainText("错误: 密钥必须是16位二进制字符串！")
            return

        if len(ciphertext) % 16 != 0 or not all(bit in '01' for bit in ciphertext):
            self.result_text_decrypt.setPlainText("错误: 密文必须是16位有效的二进制字符串！")
            return

        plaintext = cbc_decrypt(ciphertext, key, iv)
        self.result_text_decrypt.setPlainText("明文: " + plaintext)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CBCApp()
    window.show()
    sys.exit(app.exec_())
