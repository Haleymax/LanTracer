import socket
import time

from django.core.cache import cache

from common.aes_encryption import get_key
from common.logger import logger
from device.models import SharedKey


def send_shared_key(host:str, port:int):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(3)
    try:
        client.connect((host, port))
        logger.info(f"已经连接到了 salve 节点的 tcp 服务器 {host}:{port}")

        message = get_key()

        logger.info(f"获取到密钥准备发送给slave节点{message}")

        try:
            shared_key = SharedKey.objects.get(key="shared_key")
            shared_key.value = message
            shared_key.save()
            logger.info(f"密钥已更新")
        except SharedKey.DoesNotExist:
            SharedKey.objects.create(key="shared_key", value=message)
            logger.info("创建新的密钥")

        client.sendall(message)

        response = client.recv(1024).decode('utf-8')
        logger.info(f"得到客户端的反馈:{response}")
    except Exception as e:
        logger.error(f"在传输过程中发生错误:{e}")
    finally:
        client.close()
        logger.info("关闭TCP服务端")