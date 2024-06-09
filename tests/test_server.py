import unittest
import grpc
import api_pb2
import api_pb2_grpc
from grpc import ssl_channel_credentials

class TestServerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('/home/user/server/server.crt', 'rb') as f:
            trusted_certs = f.read()
        credentials = ssl_channel_credentials(root_certificates=trusted_certs)
        cls.channel = grpc.secure_channel('server:50051', credentials)
        cls.stub = api_pb2_grpc.DayTimeStub(cls.channel)

    def test_set_and_get(self):
        # 最初の値をセットし、前の値を確認（空のはず）
        response = self.stub.set(api_pb2.Value(data="Hello World"))
        self.assertEqual(response.data, "No data set")

        # 現在の値を取得
        response = self.stub.get(api_pb2.Empty())
        self.assertEqual(response.data, "Hello World")

        # 新たな値をセットし、前の値を確認
        response = self.stub.set(api_pb2.Value(data="New Data"))
        self.assertEqual(response.data, "Hello World")

        # 新たな値を取得
        response = self.stub.get(api_pb2.Empty())
        self.assertEqual(response.data, "New Data")

if __name__ == '__main__':
    unittest.main()
