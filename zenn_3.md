# [Docker] MongoDB接続がタイムアウトする場合の対処法

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/eye_catch_4.png)

- [\[Docker\] MongoDB接続がタイムアウトする場合の対処法](#docker-mongodb接続がタイムアウトする場合の対処法)
  - [はじめに](#はじめに)
  - [注意](#注意)
  - [環境](#環境)
  - [MongoDBと繋がらなくなった時、調べるべき手順のリスト](#mongodbと繋がらなくなった時調べるべき手順のリスト)
  - [解法](#解法)
    - [ホストのファイアーウォール設定](#ホストのファイアーウォール設定)
    - [`mongosh`コマンドの使用](#mongoshコマンドの使用)
      - [MongoDBの設定確認](#mongodbの設定確認)
    - [Dockerのネットワーク](#dockerのネットワーク)
  - [まとめ](#まとめ)
  - [参考文献](#参考文献)


## はじめに
Dockerを使用してMongoDBコンテナを構築しました。構築から時間が経つと、接続がタイムアウトする問題に直面しました。
具体的には
```python
client = MongoClient('mongodb://localhost:27019/')
```
のように、`localhost`文字列を使用した場合、接続ができませんでした。（当たり前のような気もしますし、自分でもあいまいです。）
最終的には、以下のように、MongoDBコンテナのIPアドレスを使用することで、接続できるようになりました。
```python
client = MongoClient('mongodb://172.18.0.2:27017/')
```
この記事では、そのような状況での対処法を詳しく解説します。

## 注意
Dockerのネットワークについて、本来適切な方法・手順があるかもしれません。この記事では、私が試行錯誤して解決した方法を紹介しています。

Dockerのネットワークについては、日本語のチュートリアルが存在します。以下のチュートリアルを参考にしてください。

- [Docker コンテナ・ネットワークの理解](https://docs.docker.jp/engine/userguide/networking/dockernetworks.html)

## 環境
pymongoのバージョンは4.5.0です。
```bash
>>> import pymongo
>>> print(pymongo.__version__)
4.5.0
```
dockerのバージョンは24.0.6です。
```bash
docker --version
Docker version 24.0.6, build ed223bc
```
MongoDBのバージョンは7.0.1です。
Mongoshのバージョンは1.10.6です。
> NOTE:
> `Mongosh`はMongoDBの公式シェルです。以前は`mongo`コマンドを使用されていましたので、ググると普通に`mongo`コマンドを使用した記事が出てきます。`mongo`コマンドは非推奨（というかDockerコンテナ内にない）ですので、`Mongosh`を使用してください。
```bash
$ docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED       STATUS       PORTS                                           NAMES
6cf444d25f06   mongo     "docker-entrypoint.s…"   5 hours ago   Up 5 hours   0.0.0.0:27017->27017/tcp, :::27017->27017/tcp   my-mongodb

$ docker exec -it my-mongodb mongosh
Current Mongosh Log ID:	651966a2a13f95aebb001e3d
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.6
Using MongoDB:		7.0.1
Using Mongosh:		1.10.6

For mongosh info see: https://docs.mongodb.com/mongodb-shell/

------
   The server generated these startup warnings when booting
   2023-10-01T07:57:57.556+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2023-10-01T07:57:58.534+00:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   2023-10-01T07:57:58.534+00:00: vm.max_map_count is too low
------

test> db.version()
7.0.1
```
Ubuntuのバージョンは20.04 LTSです。
```bash
$ uname -a
Linux terms 5.15.0-84-generic #93~20.04.1-Ubuntu SMP Wed Sep 6 16:15:40 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

## MongoDBと繋がらなくなった時、調べるべき手順のリスト

1. **ufw設定の確認**: `sudo ufw status` コマンドを使用して、ホストマシンのファイアウォール設定がMongoDBのポートを許可しているか確認します。
2. **`mongosh` コマンドの使用**: `mongosh` コマンドを使用して手動でMongoDBに接続し、動作を確認します。
3. **MongoDBの設定確認**: コンテナ内で `mongod.conf` ファイルを探し、`bindIp` オプションが適切に設定されているか確認します。
4. **ポートマッピングの確認**: `docker ps` コマンドで、ホストとコンテナのポートが正しくマッピングされているか確認します。
5. **Dockerのネットワークモード確認**: `docker inspect <コンテナIDまたはコンテナ名> | grep NetworkMode` コマンドで、Dockerコンテナのネットワークモードを確認します。

他に考慮すべき点は、以下の通りです。
6. **MongoDBのログ確認**: MongoDBのログを確認して、エラーメッセージや警告がないかチェックします。
7. **telnetまたはncでの接続テスト**: `telnet` や `nc` コマンドを使用して、MongoDBに接続できるかテストします。
8. **MongoDBのプロセス確認**: `ps aux | grep mongod` コマンドで、MongoDBのプロセスが正常に動作しているか確認します。
9. **Dockerコンテナのリスタート**: 問題が解決しない場合、Dockerコンテナをリスタートしてみます。


## 解法
### ホストのファイアーウォール設定
ufw（Uncomplicated Firewall）をファイアウォールとして使用している場合、Dockerはホストマシンのネットワークを使用するため、ufwの設定がDockerコンテナの通信を遮断する可能性があります。

```bash
sudo ufw allow from 127.0.0.1 to any port 27019 proto tcp  # ローカルホストからの通信だけを許可
```
この設定により、127.0.0.1（localhost）からの27019ポートへのTCP通信だけが許可されます。

設定が完了したら、ufwの設定を再読み込みして有効にしてください。
```bash
sudo ufw reload
```
そして、`sudo ufw status`で設定が反映されているか確認してください。
```bash
sudo ufw status
状態: アクティブ

To                         Action      From
--                         ------      ----
（省略）
27019/tcp                  ALLOW       127.0.0.1
```

### `mongosh`コマンドの使用
`mongosh`コマンドを使用して、手動でMongoDBに接続し、動作を確認します。
```bash
docker exec -it my-mongodb mongosh
Current Mongosh Log ID:	6519285a2cf91dd0da5bb580
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.6
Using MongoDB:		7.0.1
Using Mongosh:		1.10.6

For mongosh info see: https://docs.mongodb.com/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting
   2023-10-01T07:57:57.556+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2023-10-01T07:57:58.534+00:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   2023-10-01T07:57:58.534+00:00: vm.max_map_count is too low
------

test> exit
```

#### MongoDBの設定確認
**設定ファイルの確認**: MongoDBの設定ファイル（通常は`mongod.conf`）で、`bindIp` オプションが適切に設定されているか確認します。

   `mongod.conf`ファイルで、どのIPアドレスからの接続を許可するかが制限されていないか確認するのですが、Docker内には`mongod.conf.orig`ファイルはあるものの、`mongod.conf`ファイルはありませんでした。

   このように設定ファイルがない場合、`ps aux | grep mongod`で確認を行います。
   ```bash
   docker exec -it mongodb-1 /bin/bash
   root@b87f6a0ab623:/#  ps aux | grep mongod
   mongodb        1  0.3  0.9 2666480 149804 ?      Ssl  08:18   0:37 mongod --bind_ip_all
   root          80  0.0  0.0   3468  1640 pts/0    S+   11:00   0:00 grep mongod
   ```
   この出力から、MongoDBは`--bind_ip_all`オプションで起動していることがわかります。このオプションは、MongoDBがすべてのIPアドレスからの接続を許可するように設定されていることを意味します。この設定はセキュリティ上のリスクがありますが、今回のように、ローカルネットワーク内での使用やテスト環境であれば問題ない場合もあります。

### Dockerのネットワーク
Dockerにユーザー定義のネットワーク（my_network）を作成します。
> NOTE:
> 本来なら`bridge`から接続できるはずですが、この環境では`bridge`へ接続できませんでした。
```bash
docker network create my_network
```

ネットワークが作成されたら、新しいコンテナを作成する際や既存のコンテナを起動する際に、`--network`オプションを使用してこのネットワークに接続できます。

既存のコンテナに新しいネットワークを接続するには、以下のコマンドを使用します。

```bash
docker network connect my_network my-mongodb
```

このコマンドで、`my-mongodb`という名前のコンテナが`my_network`というネットワークに接続されます。

`docker network inspect my_network` コマンドを使用して、`my_network`という名前のネットワークの詳細情報を表示できます。このコマンドの出力には、そのネットワークに接続されているすべてのコンテナとそのIPアドレスが含まれます。

コマンドを実行すると、以下のような形式で情報が表示されるはずです。
```bash
$ docker network inspect my_network
[
    {
        "Name": "my_network",
        "Id": "8672d61a39617cd6388c42dad055528e1f1d049d90b9b59b0af98010db79806c",
        "Created": "2023-10-01T14:43:54.96084477+09:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "6cf444d25f06f338d16160cd143ff3437ea1a2447305d4a903a0a415b3b57c36": {
                "Name": "my-mongodb",
                "EndpointID": "189238e17c2cf137b7a325ccb9d917d0daa32f6f09fec178d120ca0bdd3aa0f9",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",  # この行が重要
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

Dockerネットワークの情報から、MongoDBコンテナ（`my-mongodb`）のIPv4アドレスが`172.18.0.2`であることがわかります。この情報を使用して、PythonからMongoDBに接続できます。

Pythonインタラクティブシェルで以下のコードを実行します。

```python
from pymongo import MongoClient
# MongoDBコンテナのIPアドレスとポートを使用して接続
client = MongoClient('mongodb://172.18.0.2:27017/')
print(client.list_database_names())
```

この設定でPythonがMongoDBに接続できました。

Pythonのインタラクティブシェルでは、以下のように接続を確認できます。
```python
>>> from pymongo import MongoClient
>>> client = MongoClient('mongodb://172.18.0.2:27017/')
>>> print(client.list_database_names())
['admin', 'config', 'local', 'my_database']
>>> 
```

## まとめ
この記事では、Dockerを使用して構築したMongoDBコンテナとの接続がタイムアウトする問題に対する対処法を詳細に解説しました。ufwの設定、`mongosh`の使用、MongoDBの設定確認、Dockerのネットワーク設定など、多角的な視点から問題を解決する方法を模索しました。

また、`docker network inspect`コマンドを使用して、コンテナの内部IPアドレスを確認することで、Pythonからの接続もスムーズに行えました。

Dockerのユーザー定義ネットワークを作成して、そのネットワークにMongoDBコンテナを接続する方法は、本来の運用（設定）方法とは違うかもしれません。その点はご留意下さい。

何らかの接続問題に直面した際には、この記事が皆さんの参考になれば幸いです。

以上です。ありがとうございました。

## 参考文献
- [Docker コンテナ・ネットワークの理解](https://docs.docker.jp/engine/userguide/networking/dockernetworks.html)
