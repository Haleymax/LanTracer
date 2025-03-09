import json
import threading

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from common.aes_encryption import get_key, decrypt
from common.tcp_client import TCPClient

from common.logger import logger
from core.tcp_send_key import send_shared_key
from device.models import SharedKey, Node, Device
from device.response_model import DeviceResponse


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

@csrf_exempt
def check(request):
    result = {}
    if request.method == "POST":
        try:
            if not request.body:
                return HttpResponse(json.dumps({"error":"Empty request body"}), content_type="application/json", status=400)

            key = SharedKey.objects.get(key="shared_key")


            data = json.loads(request.body)
            host = decrypt(ciphertext=data.get('host'), key=key.value)
            used_space = int(decrypt(ciphertext=data.get('used_space'), key=key.value))/1024/1024
            total_space = int(decrypt(ciphertext=data.get('total_space'), key=key.value))/1024/1024
            remaining_menory = total_space - used_space

            # 判断节点信息是否存在
            try:
                node_info, created = Node.objects.get_or_create(
                    ip_address=host,
                    defaults={
                        'node_name': host,
                        'total_menory': total_space,
                        'remaining_menory': remaining_menory,
                        'state': "online"
                    }
                )
                if not created:
                    # 如果对象已经存在，更新信息
                    node_info.node_name = host
                    node_info.total_menory = total_space
                    node_info.remaining_menory = remaining_menory
                    node_info.state = "online"
                    node_info.save()  # 保存更新后的信息
            except Exception as e:
                # 处理可能出现的异常，例如数据库连接错误等
                print(f"处理节点信息时出现错误: {e}")
            result["success"] = True
            return HttpResponse(json.dumps(result), content_type="application/json", status=200)
        except json.JSONDecodeError as e:
            return HttpResponse(json.dumps({"error":"Invalid JSON data"}), content_type="application/json", status=400)
        except Exception as e:
            logger.error(f"获取节点信息发生错误:{e}")
            return HttpResponse(json.dumps({"error":str(e)}), content_type="application/json", status=500)
    else:
        return HttpResponse(json.dumps({"error":"Invalid request method"}), content_type="application/json", status=405)


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

@csrf_exempt  # 如果需要禁用 CSRF 验证，可以保留这个装饰器
@require_http_methods(["GET"])
def get_device(request):
    device_response = DeviceResponse(status=False, message="no message")

    try:
        device_list =  []
        devices = Device.objects.all()
        for device in devices:
            one_record = {
                "host": device.ip_address,
                "name": device.node_name,
            }
            device_list.append(one_record)
        device_response.status = True
        device_response.message = device_list
    except Exception as e:
        logger.error(e)
        device_response.message = f"an error occurred during the query:{e}"
        return JsonResponse(device_response.dict(), status=500)
    return JsonResponse(device_response.dict(), status=200 )


