from pymongo import MongoClient

# MongoDBに接続
# client = MongoClient('172.17.0.0', 27019)  
client = MongoClient('mongodb://172.18.0.2:27017/')
print(client.list_database_names())
# データベースとコレクションを選択
db = client['face_recognition_db']
collection = db['known_faces']

# コレクションを消去
# collection.drop()

# コレクション内のドキュメント数をカウント
count = collection.count_documents({})
print(f"Number of documents in 'known_faces' collection: {count}")

# # コレクションから2件のドキュメントを取得して表示
# for doc in collection.find().limit(2):
#     print(doc)
    
"""
Number of documents in 'known_faces' collection: 59422

{'_id': ObjectId('6517a1c2eb9f7c5d01bf3688'), 'file_name': '風間杜夫_0uGH.jpg.png_default.png_0.png_0_align_resize.png', 'vector': [[-2.002249002456665, 1.1896134614944458, -2.685077667236328, -0.35192739963531494, -4.17877721786499, 2.763749599456787, 0.7297924160957336, -1.7906469106674194, 0.9215985536575317, -0.9142802953720093, -1.0857841968536377,
（中略）
0.6890649795532227, -2.702629327774048, 1.0395612716674805, -1.9293512105941772, 1.8116620779037476,  -0.49356165528297424, -2.5102062225341797, -2.5021908283233643, 1.2771133184432983, 0.052276045083999634, 2.0962891578674316, 1.2408920526504517, -0.6889671683311462]]}

{'_id': ObjectId('6517a1c2eb9f7c5d01bf3689'), 'file_name': '風間杜夫_BNcF.jpg.png_default.png_0.png_0_align_resize.png', 'vector': [[-2.548264980316162, 2.27040433883667, 0.3865867555141449, -0.43443238735198975, -0.9933996796607971, 1.4334064722061157, -0.7523462772369385, 1.9946444034576416, 1.1201945543289185, 1.3821269273757935, 1.2295866012573242,
（中略）
0.8671872615814209, 0.6558080911636353, -0.8653426766395569, 1.4265012741088867, 3.138498306274414, 0.05671160668134689, -0.868281364440918, -1.763211965560913, -1.2924718856811523, 0.6372048854827881, -1.6095494031906128, 0.24598270654678345, 0.018475055694580078, 0.3127145767211914]]}
"""
"""
(mongodb) 
 terms  terms  ~/bin/mongodb  python
Python 3.8.10 (default, May 26 2023, 14:05:08) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pymongo import MongoClient
>>> client = MongoClient('localhost', 27019)
>>> db = client['test_db']
>>> collection = db['test_collection']
>>> result = collection.insert_one({"key": "value"})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/collection.py", line 671, in insert_one
    self._insert_one(
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/collection.py", line 611, in _insert_one
    self.__database.client._retryable_write(acknowledged, _insert_command, session)
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/mongo_client.py", line 1567, in _retryable_write
    with self._tmp_session(session) as s:
  File "/usr/lib/python3.8/contextlib.py", line 113, in __enter__
    return next(self.gen)
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/mongo_client.py", line 1885, in _tmp_session
    s = self._ensure_session(session)
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/mongo_client.py", line 1868, in _ensure_session
    return self.__start_session(True, causal_consistency=False)
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/mongo_client.py", line 1811, in __start_session
    self._topology._check_implicit_session_support()
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/topology.py", line 583, in _check_implicit_session_support
    self._check_session_support()
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/topology.py", line 599, in _check_session_support
    self._select_servers_loop(
  File "/home/terms/bin/mongodb/lib/python3.8/site-packages/pymongo/topology.py", line 269, in _select_servers_loop
    raise ServerSelectionTimeoutError(
pymongo.errors.ServerSelectionTimeoutError: localhost:27019: timed out, Timeout: 30s, Topology Description: <TopologyDescription id: 6518e351d8266a5f9741a27c, topology_type: Unknown, servers: [<ServerDescription ('localhost', 27019) server_type: Unknown, rtt: None, error=NetworkTimeout('localhost:27019: timed out')>]>
>>> 
"""