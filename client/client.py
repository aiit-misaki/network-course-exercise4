import grpc
import api_pb2
import api_pb2_grpc
from grpc import ssl_channel_credentials
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levellevel)s - %(message)s')

def run():
    # TLS設定の追加
    with open('server.crt', 'rb') as f:
        trusted_certs = f.read()
    credentials = ssl_channel_credentials(root_certificates=trusted_certs)

    with grpc.secure_channel('server:50051', credentials) as channel:
        stub = api_pb2_grpc.DayTimeStub(channel)
        # 最初の値をセットし、前の値を確認（空のはず）
        prev_value = stub.set(api_pb2.Value(data="Hello World"))
        print("First set - Previous Value:", prev_value.data)

        # 現在の値を取得
        current_value = stub.get(api_pb2.Empty())
        print("First get - Current Value:", current_value.data)

        # 新たな値をセットし、前の値を確認
        prev_value = stub.set(api_pb2.Value(data="New Data"))
        print("Second set - Previous Value:", prev_value.data)

        # 新たな値を取得
        current_value = stub.get(api_pb2.Empty())
        print("Second get - Current Value:", current_value.data)

if __name__ == '__main__':
    run()
