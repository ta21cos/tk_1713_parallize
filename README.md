# tk_1713_parallize
JPHACK2017

`python flask_test.py`でサーバーが起動
`{"recipe_ids": [x, x, ...]}`という形式のjsonをpostすると
`{"result": [{"index": xxx, "description": xxx, "duration": xxx, "mo_start": xxx, "mo_end": xxx, "recipe_id": xxx}, ...]}`という形式のjsonが返ってくる
