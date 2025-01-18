from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# 加密函数
def encrypt(plain_text, key):
    # 生成随机的初始化向量 (IV)
    iv = get_random_bytes(AES.block_size)
    # 创建 AES 加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 对明文进行填充并加密
    ciphertext = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    # 返回 IV 和密文（Base64 编码）
    return base64.b64encode(iv + ciphertext).decode()

# 解密函数
def decrypt(ciphertext, key):
    # Base64 解码
    ciphertext = base64.b64decode(ciphertext)
    # 提取 IV
    iv = ciphertext[:AES.block_size]
    # 提取密文
    ciphertext = ciphertext[AES.block_size:]
    # 创建 AES 解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并去除填充
    plain_text = unpad(cipher.decrypt(ciphertext), AES.block_size)
    # 返回明文
    return plain_text.decode()

def get_key():
    return get_random_bytes(16)

if __name__ == '__main__':
    # 示例
    shared_key = get_key()
    plain_text = "Hello, AES encryption with shared key!"

    # 加密
    ciphertext = encrypt(plain_text, shared_key)
    print("加密后的数据:", ciphertext)

    # 解密
    decrypted_text = decrypt(ciphertext, shared_key)
    print("解密后的数据:", decrypted_text)