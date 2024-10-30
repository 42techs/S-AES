import numpy as np
import random

# S-Box 和逆 S-Box
S_BOX = [
    [0x9, 0x4, 0xA, 0xB],
    [0xD, 0x1, 0x8, 0x5],
    [0x6, 0x2, 0x0, 0x3],
    [0xC, 0xE, 0xF, 0x7]
]

S_BOX_INV = [
    [0xA, 0x5, 0x9, 0xB],
    [0x1, 0x7, 0x8, 0xF],
    [0x6, 0x0, 0x2, 0x3],
    [0xC, 0x4, 0xD, 0xE]
]
 
rcon = [0b10000000, 0b00110000]

# 生成轮密钥的辅助函数
def g(w, i):
    N0 = (w >> 4) & 0xF
    N1 = w & 0xF
    N1_sub = S_BOX[N1 >> 2][N1 & 0x3]
    N0_sub = S_BOX[N0 >> 2][N0 & 0x3]
    return ((N1_sub << 4) | N0_sub) ^ rcon[i]

# 密钥函数
def key_expansion(key):
    w = [0] * 6
    w[0] = (key >> 8) & 0xFF
    w[1] = key & 0xFF
    w[2] = w[0] ^ g(w[1], 0)
    w[3] = w[2] ^ w[1]
    w[4] = w[2] ^ g(w[3], 1)
    w[5] = w[4] ^ w[3]
    return w
 
# 加密和解密核心函数
def NS(state, box):
    result = 0
    for i in range(4):
        nibble = (state >> (4 * (3 - i))) & 0xF
        row = (nibble >> 2) & 0x3
        col = nibble & 0x3
        substituted_nibble = box[row][col]
        result |= (substituted_nibble << (4 * (3 - i)))
    return result
 
def RS(state):
    high_byte = (state >> 8) & 0xFF
    low_byte = state & 0xFF
    shifted_low_byte = ((low_byte << 4) | (low_byte >> 4)) & 0xFF
    return (high_byte << 8) | shifted_low_byte

def GF_mult(a, b):
    p = 0
    for counter in range(4):
        if (b & 1) == 1:
            p ^= a
        hi_bit_set = (a & 0x8)
        a <<= 1
        if hi_bit_set == 0x8:
            a ^= 0x13
        b >>= 1
    return p

def MC(state, inv=False):
    if inv:
        mix_matrix = np.array([[9, 2], [2, 9]])  
    else:
        mix_matrix = np.array([[1, 4], [4, 1]])

    state_array = np.array([
        [(state >> 12) & 0xF, (state >> 8) & 0xF],
        [(state >> 4) & 0xF, state & 0xF]
    ])
    mixed_state = np.zeros_like(state_array)

    for j in range(2):
        mixed_state[0, j] = GF_mult(mix_matrix[0, 0], state_array[0, j]) ^ GF_mult(mix_matrix[0, 1], state_array[1, j])
        mixed_state[1, j] = GF_mult(mix_matrix[1, 0], state_array[0, j]) ^ GF_mult(mix_matrix[1, 1], state_array[1, j])

    mixed_state = (mixed_state[0, 0] << 12) | (mixed_state[0, 1] << 8) | (mixed_state[1, 0] << 4) | mixed_state[1, 1]
    return mixed_state

def encrypt(plain_text, key):
    key = int(key, 2)
    plain_text = int(plain_text, 2)
    
    w = key_expansion(key)
    state = plain_text

    state ^= (w[0] << 8) | w[1]
    state = NS(state, S_BOX)
    state = RS(state)
    state = MC(state)
    state ^= (w[2] << 8) | w[3]
    state = NS(state, S_BOX)
    state = RS(state)
    state ^= (w[4] << 8) | w[5]
    return f"{state:016b}"

def decrypt(cipher_text, key):
    cipher_text = int(cipher_text, 2)
    key = int(key, 2)

    w = key_expansion(key)
    state = cipher_text
    
    state ^= (w[4] << 8) | w[5]
    state = RS(state)
    state = NS(state, S_BOX_INV)
    state ^= (w[2] << 8) | w[3]
    state = MC(state, inv=True)
    state = RS(state)
    state = NS(state, S_BOX_INV)
    state ^= (w[0] << 8) | w[1]
    return f"{state:016b}"

# CBC加密函数
def cbc_encrypt(plaintext, key, iv):
    ciphertext = ""
    iv = int(iv, 2)  # 转换 IV 为整数
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]  # 每16位为一组
        if len(block) < 16:
            block = block.ljust(16, '0')  # 若不足16位，补0
        
        # 当前块与IV或前一个密文进行异或
        block = int(block, 2) ^ iv
        encrypted_block = encrypt(f"{block:016b}", key)  # 加密
        ciphertext += encrypted_block  # 连接到密文
        iv = encrypted_block  # 更新IV为当前密文块
    return ciphertext

# CBC解密函数
def cbc_decrypt(ciphertext, key, iv):
    plaintext = ""
    iv = int(iv, 2)  # 转换 IV 为整数
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]  # 每16位为一组
        decrypted_block = decrypt(block, key)  # 解密
        decrypted_block = int(decrypted_block, 2) ^ iv  # 与IV或前一个密文进行异或
        plaintext += f"{decrypted_block:016b}"  # 连接到明文
        iv = block  # 更新IV为当前密文块
    return plaintext

# 测试示例
if __name__ == "__main__":
    plaintext = "00000000000011110000000000000000"  # 示例明文
    key = "1111111111110000"  # 示例密钥
    iv = f"{random.randint(0, 0xFFFF):016b}"  # 随机生成 16 位 IV

    print(f"IV: {iv}")
    ciphertext = cbc_encrypt(plaintext, key, iv)
    print(f"密文: {ciphertext}")

    # 测试篡改
    modified_ciphertext = ciphertext[:16] + "1111000011110000" + ciphertext[32:]  # 修改第一个块
    print(f"篡改的密文: {modified_ciphertext}")

    # 解密前后的比较
    decrypted_text_before_modification = cbc_decrypt(ciphertext, key, iv)
    decrypted_text_after_modification = cbc_decrypt(modified_ciphertext, key, iv)
    print(f"解密前的明文: {decrypted_text_before_modification}")
    print(f"解密后的明文: {decrypted_text_after_modification}")

