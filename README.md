![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/eye_catch.png)

- [背景](#背景)
- [解決策](#解決策)
- [手順](#手順)
  - [1. Dockerのインストール](#1-dockerのインストール)
    - [Dockerがインストールされているか確認](#dockerがインストールされているか確認)
  - [2. MongoDBのDockerコンテナを起動](#2-mongodbのdockerコンテナを起動)
    - [一度停止したコンテナを再起動するには](#一度停止したコンテナを再起動するには)
  - [3. Python仮想環境の作成](#3-python仮想環境の作成)
  - [4. 仮想環境をアクティブにする](#4-仮想環境をアクティブにする)
  - [5. MongoDBのPythonドライバーをインストール](#5-mongodbのpythonドライバーをインストール)
- [FaissとMongoDBを組み合わせたダミーデータの検索](#faissとmongodbを組み合わせたダミーデータの検索)
  - [必要なパッケージのインストール](#必要なパッケージのインストール)
  - [コード例](#コード例)
    - [出力例](#出力例)
- [起動しているMongoDBコンテナを停止する](#起動しているmongodbコンテナを停止する)
  - [例](#例)
- [まとめ](#まとめ)


## 背景
- 顔認識システムで、URL、512次元の数値配列、検索結果などを効率よく保存・検索したい。
- MongoDBの高度なインデックス作成機能がこの用途に適している。
- Ubuntu 20.04を使用しており、システム全体に影響を与えずにMongoDBを導入したい。

## 解決策
Dockerを使用して、プロジェクト専用のMongoDB環境を構築する。

## 手順
### 1. Dockerのインストール
Ubuntu 20.04にDockerをインストールする。

#### Dockerがインストールされているか確認
```bash
docker --version
sudo systemctl status docker
```
インストールされていなければ、以下のURLを参照してインストールする。

[Install Docker Desktop on Ubuntu](https://docs.docker.com/desktop/install/ubuntu/)

### 2. MongoDBのDockerコンテナを起動
専用のディレクトリ（例：`/home/user/bin/mongodb`）でMongoDBのDockerコンテナを起動する。
```bash
docker run --name my-mongodb -v /home/user/bin/mongodb/data:/data/db -p 27017:27017 -d mongo
```

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/2023-09-27-17-36-39.png)

#### 一度停止したコンテナを再起動するには
Dockerコンテナを一度停止した後、再び起動するには以下の手順を実行します。

1. **停止したコンテナのIDまたは名前を確認する**: `docker ps -a` コマンドを使用して、すべてのコンテナ（実行中、停止中を含む）の一覧を表示します。
    ```bash
    docker ps -a
    ```
    このコマンドの出力から、再起動したいMongoDBコンテナのIDまたは名前（この場合は`my-mongodb`）を確認できます。

2. **コンテナを再起動する**: `docker start` コマンドに、再起動したいコンテナのIDまたは名前を指定します。
    ```bash
    docker start [CONTAINER_ID_OR_NAME]
    ```
    例えば、コンテナの名前が `my-mongodb` の場合、以下のように実行します。
    ```bash
    docker start my-mongodb
    ```

これで、`my-mongodb` コンテナが再起動します。

### 3. Python仮想環境の作成
同じディレクトリ内でPythonの仮想環境を作成する。
```bash
python3 -m venv .
```

### 4. 仮想環境をアクティブにする
```bash
source ./bin/activate
```

### 5. MongoDBのPythonドライバーをインストール
```bash
pip install pymongo
```
---

## FaissとMongoDBを組み合わせたダミーデータの検索

### 必要なパッケージのインストール
```bash
pip install pymongo
pip install faiss-cpu  # CPU版
```

### コード例
1. MongoDBに接続し、ダミーデータを挿入。
2. Faissのインデックスを作成し、ダミーデータを追加。
3. テキストファイル（ここではランダムに生成）からクエリベクトルを読み込み、Faissで検索。
4. 検索結果に一致したURLを標準出力。

https://github.com/yKesamaru/mongodb/blob/a0f6e3f40cff33fb6fb0febf1445aa2ab6b8889f/faiss_mongodb_example.py#L1-L38

#### 出力例
```bash
検索に一致したURL: amazon.co.jp
Faissでの検索と結果の出力が完了しました。
```

## 起動しているMongoDBコンテナを停止する

1. **コンテナのIDまたは名前を確認する**: `docker ps` コマンドを使用して、現在実行中のコンテナの一覧を表示します。
    ```bash
    docker ps
    ```
    このコマンドの出力から、MongoDBコンテナのIDまたは名前を確認できます。

2. **コンテナを停止する**: `docker stop` コマンドに、停止したいコンテナのIDまたは名前を指定します。
    ```bash
    docker stop [CONTAINER_ID_OR_NAME]
    ```
    例えば、コンテナのIDが `1234567890ab` の場合、以下のように実行します。
    ```bash
    docker stop 1234567890ab
    ```

### 例
```bash
$ docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED             STATUS             PORTS                                           NAMES
d4d93372ebcb   mongo     "docker-entrypoint.s…"   About an hour ago   Up About an hour   0.0.0.0:27017->27017/tcp, :::27017->27017/tcp   my-mongodb

$ docker stop my-mongodb
my-mongodb

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

```

これで、MongoDBのDockerコンテナが停止します。

---

## まとめ
- Dockerを使用することで、システム全体に影響を与えずにMongoDBを導入できる。
- Pythonの仮想環境内でMongoDBのPythonドライバー（PyMongo）をインストールすることで、プロジェクト専用の環境を構築できる。
- FaissとMongoDBを組み合わせることで、高次元のベクトルデータに対する効率的な検索と保存が可能。

以上です。ありがとうございました。