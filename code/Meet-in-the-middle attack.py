
from code.s_aes import encrypt, decrypt 
# 中间相遇攻击函数
def generate_intermediate_states(plain_texts, keys):
    intermediate_states = {}
    
    for key in keys:
        for plain_text in plain_texts:
            # 加密明文以获取中间状态
            plain_text_bin = int(plain_text, 2)
            state = encrypt(plain_text, f"{key:08b}")  # 确保密钥是8位二进制字符串
            intermediate_states.setdefault(state, []).append(key)

    return intermediate_states

# 尝试所有密钥组合
def meet_in_the_middle_attack(plain_texts, cipher_texts):
    possible_keys = []
    keys = [i for i in range(256)]  # 假设密钥空间为0到255
    
    # 生成中间状态表
    forward_states = generate_intermediate_states(plain_texts, keys)

    # 反向查找
    for key in keys:
        for cipher_text in cipher_texts:
            cipher_text_bin = int(cipher_text, 2)
            state = decrypt(cipher_text, f"{key:08b}")  
            if state in forward_states:
                for k1 in forward_states[state]:
                    # k1 和 k2 组合成一个可能的密钥
                    possible_keys.append((k1, key))
    
    return possible_keys

plain_texts = ["1100110011001100", "1111111100000000"]  # 明文列表 
cipher_texts = ["0101000111010100", "0010111111010000"]  # 密文列表 

found_keys = meet_in_the_middle_attack(plain_texts, cipher_texts)

for k1, k2 in found_keys:
    print(f"密钥组合: K1 = {k1:08b}, K2 = {k2:08b}")
