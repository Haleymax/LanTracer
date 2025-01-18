import platform
import socket
import shutil


class DeviceInfo:
    def __init__(self):
        pass

    @staticmethod
    def get_local_ip(self) -> str:
        """
        获取本机ip地址
        :return: 返回本机的ip地址
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f"获取本机ip地址发送了错误:{e}")
            return "Unknown"

    def get_disk_usage(self):
        """
        获取磁盘使用信息
        :return: 磁盘信息
        """
        system = platform.system()
        if system == "Darwin" or system == "Linux":
            try:
                # 从根目录开始获取整个系统的磁盘使用情况
                usage = shutil.disk_usage("/")
                return usage.used, usage.total
            except Exception as e:
                print(f"获取磁盘信息时出错:{e}")
                return 0, 0
        elif system == "Windows":
            try:
                # window系统下磁盘分得比较散，所以目前只支持查看C盘的内存使用情况
                usage = shutil.disk_usage("C:\\")
                return usage.used, usage.total
            except Exception as e:
                print(f"获取磁盘信息时出错:{e}")
                return 0, 0
        else:
            print(f"不支持该操作系统:{system}")
            return 0, 0

    def print_device_info(self):
        """
        打印Node节点的信息
        :return:
        """
        local_ip = self.get_local_ip()
        usage, total = self.get_disk_usage()
        print(f"本机的ip地址为:{local_ip}")
        print(f"本机的磁盘总量为:{total}")
        print(f"本机的磁盘使用情况为:{usage}")

def get():
    return DeviceInfo()

if __name__ == "__main__":
    device_info = DeviceInfo()
    device_info.print_device_info()