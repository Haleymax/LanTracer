import socket

from common.logger import logger


class TCPClient:
    def __init__(self, slave_host, slave_port):
       self.slave_host = slave_host
       self.slave_port = slave_port
       self.socket = None


    def connect(self)->bool:
        """
        与slave节点建立连接
        :return:
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.slave_host, self.slave_port))
            logger.info(f"和{self.slave_host}:{self.slave_port}建立TCP通信")
            return True
        except Exception as e:
            logger.info(f"和{self.slave_host}:{self.slave_port}建立TCP通信失败:{e}")
            return False

    def send_message(self, message:str)->str:
        """
        向 slave节点发送信息
        :param message:
        :return: 是否发送成功
        """
        if self.socket is None:
            logger.info("未连接到服务器")
            return "disconnect"
        try:
            self.socket.sendall(message.encode("utf-8"))
            logger.info(f"已发送消息:{message}")
            response = self.socket.recv(1024).decode("utf-8")
            logger.info(f"已成功接收到:{response}")
            return response
        except Exception as e:
            logger.info(f"发送消息发生错误:{e}")
            return "senderror"

    def close(self):
        if self.socket :
            self.socket.close()
            logger.info("关闭TCP连接")
        else:
            logger.info("未建立tcp连接无需关闭")


if __name__ == "__main__":
    # 服务器地址和端口
    server_ip = "127.0.0.1"  # 替换为服务器的 IP 地址
    server_port = 12345  # 替换为服务器的端口

    # 要发送的消息
    message = "Hello, Server!"

    # 创建 TCP 客户端实例
    client = TCPClient(server_ip, server_port)

    try:
        # 连接到服务器
        client.connect()

        # 发送消息
        if client.send_message(message):
            print("消息发送成功！")
        else:
            print("消息发送失败。")
    finally:
        # 关闭连接
        client.close()