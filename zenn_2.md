# [Docker] MongoDBを操作する

![](assets/eye_catch_3.png)

## はじめに
プロジェクトごとにMongoDBを使い分けられる環境をDockerで作成してあります。
この記事では、Dockerを使ってMongoDBを操作します。

新しいコンテナを作成する
```bash
docker run --name new-mongodb-3 -p 27019:27017 -d mongo:latest
```
### コンテナの確認
```bash
docker ps
CONTAINER ID   IMAGE          COMMAND                   CREATED          STATUS          PORTS                                           NAMES
bc80d5f77ba2   mongo:latest   "docker-entrypoint.s…"   17 seconds ago   Up 16 seconds   0.0.0.0:27019->27017/tcp, :::27019->27017/tcp   new-mongodb-3
```
#### 追加解説：ポートマッピング
`-p`オプションで指定する値`27019:27017`は、「ホストマシンの27019ポートをコンテナ内部の27017ポートにマッピングする」という意味です。

- `27019`: ホストマシン（あなたのPCやサーバー）のポート
- `27017`: コンテナ内部でMongoDBが動作するポート

##### 0.0.0.0:27019->27017/tcp, :::27019->27017/tcpとは？

この表記は、Dockerがどのようにポートマッピングをしているかを示しています。

- `0.0.0.0:27019->27017/tcp`: IPv4アドレスでのアクセスを意味します。外部からはホストマシンの27019ポートにアクセスすると、コンテナ内の27017ポートに転送されます。
- `:::27019->27017/tcp`: IPv6アドレスでのアクセスを意味します。基本的にはIPv4と同様の動作をします。

#### MongoDBに接続するPythonコード

MongoDBに接続する際には、上記のポートマッピング設定に基づいてPythonコードを書きます。

```python
from pymongo import MongoClient

# MongoDBが動いているDockerコンテナに接続
client = MongoClient('localhost', 27019)

# 既存のデータベース名をリストで取得
database_names = client.list_database_names()

# データベース名を出力
print("Existing databases:")
for db_name in database_names:
    print(db_name)
```

このコードでは、`MongoClient('localhost', 27019)`として、ホストマシンの27019ポートに接続しています。この27019ポートは、Dockerコンテナ内の27017ポートにマッピングされているため、実際にはコンテナ内のMongoDBに接続することになります。

出力結果
```bash
Existing databases:
admin
config
local
```
これらはMongoDBにデフォルトで存在するシステムデータベースです。

- `admin`: 管理用のデータベースで、ユーザー認証やロールの情報が格納
- `config`: シャーディング（データの分散配置）に関する設定情報が格納
- `local`: 各MongoDBインスタンス固有のデータが格納

この状態であれば、ユーザーが作成したデータベースは存在していません。
新しいデータベースを作成する場合は、Pythonの`pymongo`ライブラリを使って簡単に作成できます。

## データベースを設計する

MongoDBはスキーマレスなデータベースであり、柔軟なデータモデリングが可能です。しかし、それでもアプリケーションの要件に応じて、どのようなコレクションとフィールドを持つかは事前に考慮する必要があります。

### コレクションの設計

今回のプロジェクトでは、`npKnown.npz`から取得したファイル名と512次元ベクトルデータを格納するコレクションを作成します。このコレクションを`known_vectors`と名付けましょう。

### フィールドの設計

`known_vectors`コレクションには以下のフィールドを持たせます。

- `file_name`: ファイル名を格納するフィールド（String型）
- `vector_data`: 512次元ベクトルデータを格納するフィールド（Array型）

### Pythonでコレクションを作成するテンプレート

Pythonの`pymongo`ライブラリを使って、新しいコレクションとフィールドを作成します。
大まかな流れは以下のコードの通りです。（このコードは実行しません）
```python
from pymongo import MongoClient

# MongoDBに接続
client = MongoClient('localhost', 27019)

# 新しいデータベースとコレクションを作成（データベース名：my_database, コレクション名：known_vectors）
db = client['my_database']
collection = db['known_vectors']

# サンプルデータを挿入（実際にはnpKnown.npzからデータを読み込む）
sample_data = {
    "file_name": "sample_file",
    "vector_data": [0.1, 0.2, 0.3, ..., 0.512]  # 512次元ベクトル
}
collection.insert_one(sample_data)

# 挿入したデータを確認
for doc in collection.find({}):
    print(doc)
```

このようにして、MongoDBに新しいデータベースとコレクションを作成し、データを格納できます。
