
# プロジェクト専用のMongoDB環境をUbuntu 20.04で構築する

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/eye_catch.png)

- [プロジェクト専用のMongoDB環境をUbuntu 20.04で構築する](#プロジェクト専用のmongodb環境をubuntu-2004で構築する)
  - [背景](#背景)
  - [解決策](#解決策)
  - [手順](#手順)
    - [1. Dockerのインストール](#1-dockerのインストール)
      - [Dockerがインストールされているか確認](#dockerがインストールされているか確認)
    - [2. MongoDBのDockerコンテナーを起動](#2-mongodbのdockerコンテナーを起動)
    - [3. Python仮想環境の作成](#3-python仮想環境の作成)
    - [4. 仮想環境をアクティブにする](#4-仮想環境をアクティブにする)
    - [5. MongoDBのPythonドライバーをインストール](#5-mongodbのpythonドライバーをインストール)
  - [FaissとMongoDBを組み合わせたダミーデータの検索](#faissとmongodbを組み合わせたダミーデータの検索)
    - [必要なパッケージのインストール](#必要なパッケージのインストール)
    - [コード例](#コード例)
      - [出力例](#出力例)
  - [起動しているMongoDBコンテナーを停止する](#起動しているmongodbコンテナーを停止する)
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

### 2. MongoDBのDockerコンテナーを起動
専用のディレクトリ（例：`/home/user/bin/mongodb`）でMongoDBのDockerコンテナーを起動する。
```bash
docker run --name my-mongodb -v /home/user/bin/mongodb/data:/data/db -p 27017:27017 -d mongo
```

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/2023-09-27-17-36-39.png)

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

## 起動しているMongoDBコンテナーを停止する

1. **コンテナーのIDまたは名前を確認する**: `docker ps` コマンドを使用して、現在実行中のコンテナーの一覧を表示します。
    ```bash
    docker ps
    ```
    このコマンドの出力から、MongoDBコンテナーのIDまたは名前を確認できます。

2. **コンテナーを停止する**: `docker stop` コマンドに、停止したいコンテナーのIDまたは名前を指定します。
    ```bash
    docker stop [CONTAINER_ID_OR_NAME]
    ```
    例えば、コンテナーのIDが `1234567890ab` の場合、以下のように実行します。
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

これで、MongoDBのDockerコンテナーが停止します。

---

## まとめ
- Dockerを使用することで、システム全体に影響を与えずにMongoDBを導入できる。
- Pythonの仮想環境内でMongoDBのPythonドライバー（PyMongo）をインストールすることで、プロジェクト専用の環境を構築できる。
- FaissとMongoDBを組み合わせることで、高次元のベクトルデータに対する効率的な検索と保存が可能。

以上です。ありがとうございました。