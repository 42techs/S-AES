import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QTextEdit
)
from code.s_aes import encrypt, decrypt  # 确保此处正确引入加密解密函数

# 中间相遇攻击函数
def meet_in_the_middle_attack(plaintext, ciphertext):
    plaintext_int = int(plaintext, 2)
    ciphertext_int = int(ciphertext, 2)
    
    possible_keys = []

    for k1 in range(0, 0x10000):  # 遍历所有 16 位密钥 K1
        for k2 in range(0, 0x10000):  # 遍历所有 16 位密钥 K2
            key = (k1 << 16) | k2  # 组合成 32 位的密钥

            encrypted = encrypt(plaintext, f"{key:032b}")

            if encrypted == ciphertext:
                possible_keys.append((k1, k2))
    
    return possible_keys

class AttackUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("S-AES 中间相遇攻击")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            background-color: #f7f7f9;
            color: #333;
            font-family: Arial;
        """)

        layout = QVBoxLayout()
        
        # 明文输入
        self.plaintext_entry = QLineEdit()
        self.plaintext_entry.setPlaceholderText("输入明文 (16位二进制)")
        layout.addWidget(self.plaintext_entry)

        # 密文输入
        self.ciphertext_entry = QLineEdit()
        self.ciphertext_entry.setPlaceholderText("输入密文 (16位二进制)")
        layout.addWidget(self.ciphertext_entry)

        # 执行攻击按钮
        self.attack_button = QPushButton("执行中间相遇攻击")
        self.attack_button.clicked.connect(self.perform_attack)
        layout.addWidget(self.attack_button)

        # 结果显示
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def perform_attack(self):
        plaintext = self.plaintext_entry.text()
        ciphertext = self.ciphertext_entry.text()

        if len(plaintext) != 16 or not all(bit in '01' for bit in plaintext):
            self.result_text.setPlainText("错误: 明文必须是16位二进制字符串！")
            return

        if len(ciphertext) != 16 or not all(bit in '01' for bit in ciphertext):
            self.result_text.setPlainText("错误: 密文必须是16位二进制字符串！")
            return

        found_keys = meet_in_the_middle_attack(plaintext, ciphertext)

        if found_keys:
            results = "\n".join([f"K1: {k1:016b}, K2: {k2:016b}" for k1, k2 in found_keys])
            self.result_text.setPlainText("找到可能的密钥组合:\n" + results)
        else:
            self.result_text.setPlainText("未找到匹配的密钥组合。")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AttackUI()
    window.show()
    sys.exit(app.exec_())
