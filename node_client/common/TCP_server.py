import logging
import socket

from node_client.common.KeyStore import KeyStore
from node_client.common.device_info import DeviceInfo
from node_client.config.config import tcp_port


class TCPServer:
    def __init__(self):
        """
        初始化TCP服务器
        """
        self.host = DeviceInfo.get_local_ip()
        self.port = tcp_port
        self.socket = None

    def start(self):
        """
        启动TCP服务器
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f"TCP服务已经启动，正在监听:{self.host}:{self.port}")
            client_socket, client_address = self.socket.accept()
            print(f"与master节点建立TCP通信:{client_address[0], client_address[1]}")
            self.handle_client(client_socket)
        except Exception as e:
            print(f"TCP服务器运行出错: {e}")
        finally:
            if self.socket:
                self.socket.close()
                print("释放套接字")

    def handle_client(self, client_socket):
        """
        处理客户端信息
        :param client_socket: 客户端套接字
        """
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print("客户端已断开连接")
                    break
                print(f"收到来自客户端的数据: {data}")
                with KeyStore() as store:
                    store.update_key("secret", data)
                response = "success"
                client_socket.sendall(response.encode('utf-8'))
                print("已发送确认消息")
        except ConnectionResetError:
            print("客户端强制关闭连接")
        except Exception as e:
            print(f"处理客户端数据时出错: {e}")
        finally:
            client_socket.close()
            print("断开与客户端的连接")
