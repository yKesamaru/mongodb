"""
このスクリプトは、指定されたディレクトリとそのサブディレクトリ内に存在するnpKnown.npzファイルを探し、
その内容をMongoDBに保存します。

npKnown.npzファイルの構造:
- name.npy: ファイル名の配列が格納されています。
- efficientnetv2_arcface.npy: 512次元ベクトルの配列が格納されています。
  name.npyとefficientnetv2_arcface.npyの各要素は順番に対応しています。

MongoDBのドキュメント構造:
- file_name: npKnown.npz内のname.npyから取得したファイル名
- vector: npKnown.npz内のefficientnetv2_arcface.npyから取得した512次元ベクトル
- directory: npKnown.npzファイルが存在するディレクトリのパス

処理の流れ:
1. MongoDBサーバーに接続します。
2. 指定したディレクトリを走査して、npKnown.npzファイルを見つけます。
3. npKnown.npzファイルの内容を読み込み、MongoDBに保存します。
"""

import os

import numpy as np
from pymongo import MongoClient


def save_npz_to_mongodb(npz_data, collection):
    """
    npzファイルから読み込んだデータをMongoDBに保存する。

    Parameters:
    - npz_data: np.lib.npyio.NpzFile, npzファイルから読み込んだデータ
    - collection: pymongo.collection.Collection, MongoDBのコレクション
    """
    file_names = npz_data['name']
    vectors = npz_data['efficientnetv2_arcface']

    for file_name, vector in zip(file_names, vectors):
        file_name_str = str(file_name)  # NumPyの文字列型をPythonの文字列型に変換
        vector_list = vector.tolist()  # NumPyのndarray型をPythonのリスト型に変換
        face_data = {
            "file_name": file_name_str,
            "vector": vector_list
        }
        result = collection.insert_one(face_data)  # 挿入操作の結果を取得
        # debug
        # if result.inserted_id is not None:  # 挿入が成功したか確認
        #     print(f"Successfully inserted with ID: {result.inserted_id}")
        #     print(f"Saving: {file_name_str}, {vector_list}")
        # else:
        #     print("Insert failed.")

def load_npz_from_directory(directory_path, collection):
    """
    指定されたディレクトリとそのサブディレクトリからnpKnown.npzを探し、
    見つかった場合はMongoDBに保存する。

    Parameters:
    - directory_path: str, 走査するディレクトリのパス
    - collection: pymongo.collection.Collection, MongoDBのコレクション
    """
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file == "npKnown.npz":
                file_path = os.path.join(root, file)
                npz_data = np.load(file_path)
                save_npz_to_mongodb(npz_data, collection)

# MongoDBに接続
client = MongoClient('localhost', 27019)

# データベースを選択（データベースが存在しなければ、後から自動生成される）
db = client['face_recognition_db']

# コレクションを選択
collection = db['known_faces']

# 起点となるディレクトリのパス
directory_path = "/media/terms/2TB_Movie/face_data_backup/data"

# npKnown.npzファイルを読み込み、MongoDBに保存
load_npz_from_directory(directory_path, collection)
