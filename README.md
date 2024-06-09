# network-course-exercise4

### リポジトリをクローン
git clone https://github.com/aiit-misaki/network-course-exercise4.git
cd network-course-exercise4

### Docker Composeを使用してサーバーとクライアントをビルドおよび起動
docker-compose up --build

### テスト用コンテナのビルドと実行
docker-compose -f docker-compose.test.yml up --build

### サーバーとクライアントのログを確認
docker-compose logs

docker-compose -f docker-compose.test.yml logs

