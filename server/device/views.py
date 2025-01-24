import json
import threading

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from common.aes_encryption import get_key
from common.logger import logger
from common.tcp_client import TCPClient
from core.tcp_send_key import send_shared_key
from device.models import SharedKey


# Create your views here.


@csrf_exempt
def init(request):
    """
    slave节点上线的初始化请求
    :param request:
    :return:
    """
    result = {}
    if request.method == "POST":
        slave_address = request.POST['slave_address']
        slave_port = request.POST['slave_port']
        table_is_null = False

        # 获取密钥，如果不存在就新创建一个并入库
        if not SharedKey.objects.all():
           table_is_null = True
        else:
            table_is_null = False

        if table_is_null:
            shared_key = get_key()
            key = SharedKey(
                key="shared_key",
                value=shared_key,
            )
            key.save()
        else:
            shared_key = SharedKey.objects.latest('updated_at')

        # 通过TCP通信的方式将密钥发送过去
        tcp_client = TCPClient(slave_host=slave_address, slave_port=slave_port)
        try:
            tcp_client.connect()

            ret = tcp_client.send_message(message=shared_key)
            logger.info(ret)
            result["success"] = True
        except Exception as e:
            logger.error(e)
            result["success"] = False
        finally:
            tcp_client.close()
        return HttpResponse(json.dumps(result), content_type="application/json", status=200)
    else:
        result["success"] = False
        return HttpResponse(json.dumps(result), content_type="application/json", status=201)


def check(request):
    result = {}
    if request.method == "POST":
        host = request.POST['host']
        used_space = request.POST['used_space']
        return HttpResponse(json.dumps(result), content_type="application/json", status=200)

@csrf_exempt
def get_share_key(request):
    result = {}
    if request.method == "POST":
        try:
            # 检查请求体是否为空
            if not request.body:
                return HttpResponse(json.dumps({"error": "Empty request body"}), content_type="application/json", status=400)

            # 解析 JSON 数据
            data = json.loads(request.body)
            host = data.get("slave_address")  # 注意字段名是否正确
            port = data.get("slave_port")

            # 检查必要字段是否存在
            if not host or not port:
                return HttpResponse(json.dumps({"error": "Missing required fields"}), content_type="application/json", status=400)

            # 启动线程
            tcp_client_thread = threading.Thread(target=send_shared_key, args=(host, int(port)))
            tcp_client_thread.start()

            return HttpResponse(json.dumps(result), content_type="application/json", status=200)
        except json.JSONDecodeError as e:
            return HttpResponse(json.dumps({"error": "Invalid JSON data"}), content_type="application/json", status=400)
        except Exception as e:
            return HttpResponse(json.dumps({"error": str(e)}), content_type="application/json", status=500)
    else:
        return HttpResponse(json.dumps({"error": "Invalid request method"}), content_type="application/json", status=405)