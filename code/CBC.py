import random

def triple_encrypt(block, key1, key2):
    # 这里是三重加密的伪代码，仅供示范，具体实现请参考您的三重加密算法
    return ''.join('1' if b == '0' else '0' for b in block)  # 示例：简单取反

def triple_decrypt(block, key1, key2):
    # 这里是三重解密的伪代码，仅供示范
    return ''.join('1' if b == '0' else '0' for b in block)  # 示例：简单取反

def generate_iv():
    return ''.join(random.choice('01') for _ in range(16))  # 生成16位随机二进制字符串作为初始向量

def encrypt(plaintext, key1, key2):
    iv = generate_iv()
    ciphertext = iv  # 初始向量作为密文的一部分

    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i + 16]
        block_xor = ''.join('1' if (b1 != b2) else '0' for b1, b2 in zip(block, iv))
        encrypted_block = triple_encrypt(block_xor, key1, key2)
        ciphertext += encrypted_block
        iv = encrypted_block  # 更新IV为上一个加密块

    return ciphertext

def decrypt(ciphertext, key1, key2):
    iv = ciphertext[:16]  # 提取IV
    plaintext = ''

    for i in range(16, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        decrypted_block = triple_decrypt(block, key1, key2)
        block_xor = ''.join('1' if (b1 != b2) else '0' for b1, b2 in zip(decrypted_block, iv))
        plaintext += block_xor
        iv = block  # 更新IV为上一个密文块

    return plaintext

# 测试案例
def test_saes_cbc():
    key1 = '1101010101010101'  # 16位密钥1
    key2 = '1010101010101010'  # 16位密钥2
    plaintext = '11001100110011001100110011001100'  # 示例明文（长度为32位）

    print("原始明文:", plaintext)

    # 加密
    ciphertext = encrypt(plaintext, key1, key2)
    print("生成的密文:", ciphertext)

    # 解密
    decrypted_text = decrypt(ciphertext, key1, key2)
    print("解密后的明文:", decrypted_text)

    # 篡改密文并尝试解密
    tampered_ciphertext = ciphertext[:20] + '1' + ciphertext[21:]  # 修改密文的某一部分
    print("篡改后的密文:", tampered_ciphertext)

    decrypted_tampered_text = decrypt(tampered_ciphertext, key1, key2)
    print("篡改后解密的明文:", decrypted_tampered_text)

if __name__ == "__main__":
    test_saes_cbc()
