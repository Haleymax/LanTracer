import threading
import time
import urllib

from common.KeyStore import KeyStore
from common.TCP_server import TCPServer
from common.aes_encryption import encrypt
from common.device_info import DeviceInfo
from urllib import request, parse
from config import init_api, check_api, tcp_port


def send_init_request_decorator(func):
    def wrapper(self, *args, **kwargs):
        # 调用被装饰的函数
        result = func(self, *args, **kwargs)
        # 发送初始化请求
        send_init_request()

        return result

    return wrapper


def send_init_request():
    max_retries = 5
    retries = 0
    init_api = "http://example.com/init"  # 替换为实际的初始化 API URL

    post_data = {
        "slave_address":DeviceInfo.get_local_ip(),
        "slave_port":tcp_port
    }
    while retries < max_retries:
        try:
            data = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request(url=init_api, data=data, method='POST')
            with urllib.request.urlopen(req) as response:
                if response.code == 200:
                    response_data = response.read().decode('utf-8')
                    print("请求发送成功")
        except Exception as e:
            print(f"请求发生错误: {e}")
            retries += 1


class SlaveNode:
    def __init__(self):
        self.check_thread = None
        self.tcp_thread = None
        self.shared_key = None
        self.host = DeviceInfo.get_local_ip()
        self.tcp_server = TCPServer()
        self.device = DeviceInfo()

    @send_init_request_decorator
    def start(self):
        """
        流程为先启动TCP服务器，然后再发送一个get请求进行初始化请求获取密钥
        :return:
        """
        self.get_shared_key()  # 初始化 shared_key
        # 启动TCP监测的线程
        self.tcp_thread = threading.Thread(target=self.tcp_server.start)
        self.tcp_thread.start()

        self.get_shared_key()

        # 启动发送内存信息的线程
        self.check_thread = threading.Thread(target=self.check)
        self.check_thread.start()

    def get_shared_key(self):
        path = r"/data/keystore.db"
        with KeyStore(path) as keystore:
            self.shared_key = keystore.get_key("api_key")

    def check(self):
        while True:
            try:
                localhost = self.device.get_local_ip()
                used_space, total_space = self.device.get_disk_usage()
                message_data = {
                    'host': encrypt(localhost, self.shared_key),
                    'used_space': encrypt(used_space, self.shared_key),
                    'total_space': encrypt(total_space, self.shared_key)
                }
                data = parse.urlencode(message_data).encode('utf-8')
                req = request.Request(check_api, data=data, method='POST')
                response = request.urlopen(req)

                result = response.read().decode('utf-8')
                print(result)
            except Exception as e:
                print(f"error:{e}")
            finally:
                time.sleep(60 * 30)


if __name__ == '__main__':
    slave_client = SlaveNode()
    slave_client.start()