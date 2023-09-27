from pymongo import MongoClient
import numpy as np
import faiss

# MongoDBに接続
client = MongoClient('localhost', 27017)
db = client['my_database']
collection = db['my_collection']

# ダミーデータを作成
companies = ['yahoo', 'google', 'microsoft', 'apple', 'amazon']
dummy_data = []
for company in companies:
    vec = np.random.rand(512).astype('float32')  # 512次元のベクトル
    url = f"{company}.co.jp"
    dummy_data.append({'company': company, 'vector': vec.tolist(), 'url': url})

# MongoDBにダミーデータを挿入
collection.insert_many(dummy_data)

# Faissのインデックスを作成
vectors = np.array([d['vector'] for d in dummy_data]).astype('float32')
index = faiss.IndexFlatL2(512)
index.add(vectors)

# テキストファイルからクエリベクトルを読み込む（ここではランダムに生成）
query_vector = np.random.rand(1, 512).astype('float32')

# Faissで検索
k = 1  # 近傍点数
D, I = index.search(query_vector, k)

# 検索結果を出力
for i in I[0]:
    doc = collection.find_one({'company': companies[i]})
    print(f"検索に一致したURL: {doc['url']}")

print("Faissでの検索と結果の出力が完了しました。")
