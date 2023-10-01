# [Docker] プロジェクト専用のMongoDB環境を構築する

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/eye_catch.png)

- [\[Docker\] プロジェクト専用のMongoDB環境を構築する](#docker-プロジェクト専用のmongodb環境を構築する)
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
  - [Dockerとの接続がタイムアウトする場合](#dockerとの接続がタイムアウトする場合)
  - [FaissとMongoDBを組み合わせたダミーデータの検索](#faissとmongodbを組み合わせたダミーデータの検索)
    - [必要なパッケージのインストール](#必要なパッケージのインストール)
    - [コード例](#コード例)
      - [出力例](#出力例)
    - [保存されたデータをホストのディレクトリにエクスポートするには](#保存されたデータをホストのディレクトリにエクスポートするには)
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
## Dockerとの接続がタイムアウトする場合
コンテナを作ってから時間が経つと、MongoDBとの接続ができなくなる（タイムアウトする）ことがあります。その場合は、以下の記事をご参照下さい。

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

### 保存されたデータをホストのディレクトリにエクスポートするには
```bash
# MongoDBのコンテナ内でデータをエクスポート
docker exec -it my-mongodb mongoexport --db=my_database --collection=my_collection --out=/tmp/my_collection.json

# ファイルをホストにコピー
docker cp my-mongodb:/tmp/my_collection.json ./my_collection.json

```

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/2023-09-28-15-09-17.png)

```bash
{"_id":{"$oid":"6513ea6ce9c9037ca21862bb"},"index":0,"vector":[0.36408308148384094,0.8792225122451782,0.6153969168663025,0.2538047432899475,0.10696064680814743,0.9659271836280823,0.00801455695182085,0.7307615280151367,0.7949811816215515,0.33783167600631714,0.5843088626861572,0.4470159411430359,0.6317119598388672,0.7270761728286743,0.7257930040359497,0.9755019545555115,0.6576134562492371,0.3073962330818176,0.6146091818809509,0.8653984665870667,0.4204859137535095,0.0057876817882061005,0.7131060361862183,0.9305503368377686,0.4388488531112671,0.290812611579895,0.11452355235815048,0.3728684186935425,0.6782816052436829,0.5864309668540955,0.10036266595125198,0.4481697380542755,0.8349695801734924,0.515590250492096,0.7040157318115234,0.8889831900596619,0.7343042492866516,0.017087381333112717,0.9407217502593994,0.44759446382522583,0.8900551199913025,0.9805720448493958,0.

（中略）

9521809816360474,0.484465628862381,0.27780604362487793,0.7375951409339905,0.4279486835002899,0.24318945407867432,0.8132983446121216,0.18424507975578308,0.9579278230667114,0.6484475135803223,0.41953107714653015,0.3379378914833069,0.9985294342041016,0.3462742865085602,0.5037786960601807,0.23378881812095642],"is_similar":true}
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