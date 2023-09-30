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
    
"""
Number of documents in 'known_faces' collection: 59422

{'_id': ObjectId('6517a1c2eb9f7c5d01bf3688'), 'file_name': '風間杜夫_0uGH.jpg.png_default.png_0.png_0_align_resize.png', 'vector': [[-2.002249002456665, 1.1896134614944458, -2.685077667236328, -0.35192739963531494, -4.17877721786499, 2.763749599456787, 0.7297924160957336, -1.7906469106674194, 0.9215985536575317, -0.9142802953720093, -1.0857841968536377,
（中略）
0.6890649795532227, -2.702629327774048, 1.0395612716674805, -1.9293512105941772, 1.8116620779037476,  -0.49356165528297424, -2.5102062225341797, -2.5021908283233643, 1.2771133184432983, 0.052276045083999634, 2.0962891578674316, 1.2408920526504517, -0.6889671683311462]]}

{'_id': ObjectId('6517a1c2eb9f7c5d01bf3689'), 'file_name': '風間杜夫_BNcF.jpg.png_default.png_0.png_0_align_resize.png', 'vector': [[-2.548264980316162, 2.27040433883667, 0.3865867555141449, -0.43443238735198975, -0.9933996796607971, 1.4334064722061157, -0.7523462772369385, 1.9946444034576416, 1.1201945543289185, 1.3821269273757935, 1.2295866012573242,
（中略）
0.8671872615814209, 0.6558080911636353, -0.8653426766395569, 1.4265012741088867, 3.138498306274414, 0.05671160668134689, -0.868281364440918, -1.763211965560913, -1.2924718856811523, 0.6372048854827881, -1.6095494031906128, 0.24598270654678345, 0.018475055694580078, 0.3127145767211914]]}
"""