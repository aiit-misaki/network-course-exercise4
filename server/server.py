import grpc
from concurrent import futures
import api_pb2
import api_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
import logging
from grpc import ssl_server_credentials
import os

# シークレットキーのパスを環境変数から取得
secret_key_path = os.getenv('SECRET_KEY_PATH', '/home/user/server.key')
crt_path = os.getenv('CRT_PATH', '/home/user/server.crt')

# シークレットキーを読み込み
with open(secret_key_path, 'rb') as f:
    secret_key = f.read()

with open(crt_path, 'rb') as f:
    certificate_chain = f.read()

server_credentials = grpc.ssl_server_credentials(
    ((secret_key, certificate_chain),)
)

# ロギングの設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DayTimeServicer(api_pb2_grpc.DayTimeServicer):
    def __init__(self):
        self.last_value = None  # 最後にsetされた値を保存
        logging.info("Server initialized, no previous value set.")

    def set(self, request, context):
        old_value = self.last_value if self.last_value is not None else "No data set"
        self.last_value = request.data
        logging.info(f"Set called: new value = {self.last_value}, previous value = {old_value or 'None'}")
        return api_pb2.PreviousValue(data=old_value)

    def get(self, request, context):
        logging.info(f"Get called: current value = {self.last_value or 'No data set'}")
        return api_pb2.Value(data=self.last_value or "No data set")

    def daytime(self, request, context):
        response = "Response from daytime"
        logging.info(f"Daytime called: response = {response}")
        return api_pb2.DayTimeResponse(daytime="Response from daytime")

    def timestamp(self, request, context):
        now = Timestamp()
        now.GetCurrentTime()
        logging.info(f"Timestamp called: current timestamp = {now}")
        return api_pb2.TimestampResponse(timestamp=now)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_DayTimeServicer_to_server(DayTimeServicer(), server)
    # TLS設定の追加
    # with open('server.crt', 'rb') as f:
    #     server_cert = f.read()
    # with open('server.key', 'rb') as f:
    #     server_key = f.read()
    # server_credentials = ssl_server_credentials([(server_key, server_cert)])
    server.add_secure_port('[::]:50051', server_credentials)

    logging.info("Server started at port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
