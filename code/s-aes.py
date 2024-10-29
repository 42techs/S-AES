import numpy as np
 

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
 
# 半字节替代
def NS(state, box):
    result = 0
    for i in range(4):
        nibble = (state >> (4 * (3 - i))) & 0xF
        row = (nibble >> 2) & 0x3
        col = nibble & 0x3
        substituted_nibble = box[row][col]
        result |= (substituted_nibble << (4 * (3 - i)))
    return result
 
# 行移位
def RS(state):
    high_byte = (state >> 8) & 0xFF
    low_byte = state & 0xFF
    shifted_low_byte = ((low_byte << 4) | (low_byte >> 4)) & 0xFF
    return (high_byte << 8) | shifted_low_byte
 
# 乘法
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
 
# 列混淆
def MC(state, inv=False):
    if inv:
        mix_matrix = np.array([[9, 2], [2, 9]])  
    else:
        mix_matrix = np.array([[1, 4], [4, 1]])
     
    state = np.array([
        [(state >> 12) & 0xF, (state >> 8) & 0xF],
        [(state >> 4) & 0xF, state & 0xF]
    ])
    mixed_state = np.zeros_like(state)
 
    for j in range(2):
        mixed_state[0, j] = GF_mult(mix_matrix[0, 0], state[0, j]) ^ GF_mult(mix_matrix[0, 1], state[1, j])
        mixed_state[1, j] = GF_mult(mix_matrix[1, 0], state[0, j]) ^ GF_mult(mix_matrix[1, 1], state[1, j])
 
    mixed_state = (mixed_state[0, 0] << 12) | (mixed_state[0, 1] << 8) | (mixed_state[1, 0] << 4) | mixed_state[1, 1]
    return mixed_state
 
# 加密函数
def encrypt(plain_text, key):
    plain_text = int(plain_text, 2)
    key = int(key, 2)

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
 
# 解密函数
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
 
# 加密为ASCII
def encrypt_ascii(text, key):
    encrypted_text = ""
    # 每2字节分组
    for i in range(0, len(text), 2):
        # 获取2字节字符并转换为16位二进制
        block = text[i:i+2]
        if len(block) == 1:
            # 如果不足2字节则补0
            block += '\x00'
        # 将字符转换为16位二进制字符串
        plain_text_bin = f"{ord(block[0]):08b}{ord(block[1]):08b}"
        # 加密当前块，返回的是二进制
        encrypted_block_bin = encrypt(plain_text_bin, key)
        # 将16位二进制加密结果转换为两个ASCII字符并追加到密文
        encrypted_text += chr(int(encrypted_block_bin[:8], 2)) + chr(int(encrypted_block_bin[8:], 2))
    return encrypted_text

# 解密为ASCII
def decrypt_ascii(cipher_text, key):
    decrypted_text = ""
    # 每2个ASCII字符分组
    for i in range(0, len(cipher_text), 2):
        # 取出2个ASCII字符，转换为16位二进制字符串
        encrypted_block = cipher_text[i:i+2]
        encrypted_block_bin = f"{ord(encrypted_block[0]):08b}{ord(encrypted_block[1]):08b}"
        # 解密当前块
        decrypted_block_bin = decrypt(encrypted_block_bin, key)
        # 将解密后的16位二进制转换为ASCII字符
        char1 = chr(int(decrypted_block_bin[:8], 2))
        char2 = chr(int(decrypted_block_bin[8:], 2))
        decrypted_text += char1 + char2
    return decrypted_text.rstrip('\x00')  # 去除填充的'\x00'
