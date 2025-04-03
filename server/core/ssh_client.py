import paramiko
from paramiko import SSHClient

from common.logger import logger


class RemoteClient:
    def __init__(self, host, port, username, password):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host = host
        self.port = port
        self._username = username
        self._password = password

    def connect(self, timeout=5):
        try:
            self.client.connect(hostname=self.host, port=self.port, username=self._username, password=self._password, timeout=timeout)
            logger.info(f"establish a connection with {self.host}:{self.port}")
            return True, ""
        except Exception as e:
            logger.error(f"failed to establish a connection with {self.host}:{self.port} as : {e}")
            return False, str(e)

    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info(f"disconnected from {self.host}:{self.port}")