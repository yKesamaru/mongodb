# [Docker] MongoDBとFaissを使って類似画像を検索する

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/eye_catch_3.png)

- [\[Docker\] MongoDBとFaissを使って類似画像を検索する](#docker-mongodbとfaissを使って類似画像を検索する)
  - [はじめに](#はじめに)
    - [新しいコンテナを作成する](#新しいコンテナを作成する)
    - [コンテナの確認](#コンテナの確認)
      - [追加解説：ポートマッピング](#追加解説ポートマッピング)
        - [0.0.0.0:27019-\>27017/tcp, :::27019-\>27017/tcpとは？](#000027019-27017tcp-27019-27017tcpとは)
    - [MongoDBに接続するPythonコード](#mongodbに接続するpythonコード)
      - [出力結果](#出力結果)
  - [データベースを設計する](#データベースを設計する)
    - [コレクションの設計](#コレクションの設計)
    - [フィールドの設計](#フィールドの設計)
    - [Pythonでコレクションを作成するテンプレート](#pythonでコレクションを作成するテンプレート)
  - [MongoDBにデータを格納する](#mongodbにデータを格納する)
  - [格納されたデータの確認](#格納されたデータの確認)
    - [出力結果](#出力結果-1)
  - [faissを使って検索する](#faissを使って検索する)
    - [検索対象顔画像](#検索対象顔画像)
    - [実装](#実装)
    - [出力結果](#出力結果-2)
  - [まとめ](#まとめ)


## はじめに
プロジェクトごとにMongoDBを使い分けられる環境をDockerで作成してあります。
この記事では、Docker上に構築されたデータベースから、Faissを使って類似画像を検索していこうと思います。

### 新しいコンテナを作成する
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

- `0.0.0.0:27019->27017/tcp`: IPv4アドレスでのアクセスを意味します。外部からはホストマシンの27019ポートにアクセスすると、コンテナ内の27017ポートに転送されます。
- `:::27019->27017/tcp`: IPv6アドレスでのアクセスを意味します。基本的にはIPv4と同様の動作をします。

### MongoDBに接続するPythonコード

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

#### 出力結果
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
### コレクションの設計

今回のプロジェクトでは、`npKnown.npz`から取得したファイル名と512次元ベクトルデータを格納するコレクションを作成します。このコレクションを`known_vectors`と名付けます。

### フィールドの設計

`known_vectors`コレクションには以下のフィールドを持たせます。

- `file_name`: ファイル名を格納するフィールド（String型）
- `vector`: 512次元ベクトルデータを格納するフィールド（Array型）

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
    "vector": [0.1, 0.2, 0.3, ..., 0.512]  # 512次元ベクトル
}
collection.insert_one(sample_data)

# 挿入したデータを確認
for doc in collection.find({}):
    print(doc)
```

このようにして、MongoDBに新しいデータベースとコレクションを作成し、データを格納できます。

## MongoDBにデータを格納する

https://github.com/yKesamaru/mongodb/blob/038389f84ab499ec8d3171ffe73d397f8a92a982/load_npKnown_npz.py#L1-L81

## 格納されたデータの確認
```python
from pymongo import MongoClient

# MongoDBに接続
client = MongoClient('localhost', 27019)

# データベースとコレクションを選択
db = client['face_recognition_db']
collection = db['known_faces']

# コレクションを消去
# collection.drop()

# コレクション内のドキュメント数をカウント
count = collection.count_documents({})
print(f"Number of documents in 'known_faces' collection: {count}")

# コレクションから2件のドキュメントを取得して表示
for doc in collection.find().limit(2):
    print(doc)
```
### 出力結果
```bash
Number of documents in 'known_faces' collection: 59422

{'_id': ObjectId('6517a1c2eb9f7c5d01bf3688'), 'file_name': '風間杜夫_0uGH.jpg.png_default.png_0.png_0_align_resize.png', 'vector': [[-2.002249002456665, 1.1896134614944458, -2.685077667236328, -0.35192739963531494, -4.17877721786499, 2.763749599456787, 0.7297924160957336, -1.7906469106674194, 0.9215985536575317, -0.9142802953720093, -1.0857841968536377,
（中略）
0.6890649795532227, -2.702629327774048, 1.0395612716674805, -1.9293512105941772, 1.8116620779037476,  -0.49356165528297424, -2.5102062225341797, -2.5021908283233643, 1.2771133184432983, 0.052276045083999634, 2.0962891578674316, 1.2408920526504517, -0.6889671683311462]]}

{'_id': ObjectId('6517a1c2eb9f7c5d01bf3689'), 'file_name': '風間杜夫_BNcF.jpg.png_default.png_0.png_0_align_resize.png', 'vector': [[-2.548264980316162, 2.27040433883667, 0.3865867555141449, -0.43443238735198975, -0.9933996796607971, 1.4334064722061157, -0.7523462772369385, 1.9946444034576416, 1.1201945543289185, 1.3821269273757935, 1.2295866012573242,
（中略）
0.8671872615814209, 0.6558080911636353, -0.8653426766395569, 1.4265012741088867, 3.138498306274414, 0.05671160668134689, -0.868281364440918, -1.763211965560913, -1.2924718856811523, 0.6372048854827881, -1.6095494031906128, 0.24598270654678345, 0.018475055694580078, 0.3127145767211914]]}
```

約6万件のデータがMongoDBに格納されました。

## faissを使って検索する
### 検索対象顔画像

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/woman.png)

生成AIで作成された顔画像を検索対象とします。

### 実装

[load_npKnown_npz.py](https://github.com/yKesamaru/mongodb/blob/038389f84ab499ec8d3171ffe73d397f8a92a982/find_similarrity_from_mongodb.py#L1-L80)

### 出力結果
```bash
Similar document ID: 6517a1fbeb9f7c5d01c01952
Similarity Score (Cosine Similarity): 0.4709591567516327
Similar file name: 阿川泰子_vn5Z..png.png.png_0_align_resize_default.png
Similar document ID: 6517a1f3eb9f7c5d01bff6ee
Similarity Score (Cosine Similarity): 0.42845162749290466
Similar file name: 大谷直子_vixw.jpg.png_align_resize_default.png
Similar document ID: 6517a1d0eb9f7c5d01bf6eb5
Similarity Score (Cosine Similarity): 0.41680583357810974
Similar file name: 後藤晴菜_kCOc.webp.png_default..png.png_0.png_0_align_resize.png
Similar document ID: 6517a1fbeb9f7c5d01c01957
Similarity Score (Cosine Similarity): 0.40054333209991455
Similar file name: 阿川泰子_tDgX..png_0_align_resize_default.png
Similar document ID: 6517a1ebeb9f7c5d01bfd61b
Similarity Score (Cosine Similarity): 0.38524919748306274
Similar file name: 岸本加世子_QIp1.jpg_default.png.png_0.png_0_align_resize.png
処理時間: 0分 6.07秒
```
![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/image913.png)

## まとめ
わずか6秒で、約6万件のデータから類似画像を検索できました。

検索結果は、最大の類似度が0.4709だったこともあり、やはりリアルの人物にはそっくりな方はおられませんでした。
しかし、どこかで見たお顔なんですよね。誰だろう。

今回の記事では、Docker上に構築されたデータベースから、Faissを使って類似画像を検索する方法を紹介しました。

以上です。
ありがとうございました。