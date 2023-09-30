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

