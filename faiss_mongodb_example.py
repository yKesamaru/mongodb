from pymongo import MongoClient
import numpy as np
import faiss

# MongoDBに接続
client = MongoClient('localhost', 27017)
db = client['my_database']
collection = db['my_collection']

# ダミーデータを作成（512次元のベクトル、10個）
dummy_data = np.random.rand(10, 512).astype('float32')

# MongoDBにダミーデータを挿入
for i, vec in enumerate(dummy_data):
    collection.insert_one({'index': i, 'vector': vec.tolist()})

# Faissのインデックスを作成
index = faiss.IndexFlatL2(512)
index.add(dummy_data)

# 検索用のクエリベクトルを作成（512次元）
query_vector = np.random.rand(1, 512).astype('float32')

# Faissで検索
k = 3  # 近傍点数
D, I = index.search(query_vector, k)

# 検索結果をMongoDBに保存
for i in I[0]:
    doc = collection.find_one({'index': int(i)})
    collection.update_one({'index': int(i)}, {'$set': {'is_similar': True}})

print("Faissでの検索とMongoDBへの結果保存が完了しました。")
