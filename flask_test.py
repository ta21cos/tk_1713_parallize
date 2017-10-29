# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for, jsonify
import numpy as np
import Parallize
import json

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# /post にアクセスしたときの処理
@app.route('/post', methods=['POST'])
def post():
    print("posted")
    if request.method == 'POST':
        print("POST!")
        # リクエストフォームから「名前」を取得して
        recipe_ids_json = request.data
        recipe_ids = json.loads(recipe_ids_json)["recipe_ids"]
        procedure_json = Parallize.main(recipe_ids)

        print(procedure_json)

        return jsonify(ResultSet=procedure_json)

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
