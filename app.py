from flask import Flask, jsonify, request,session
from elasticsearch import Elasticsearch
from flask_sqlalchemy import SQLAlchemy
import os
import json
from datetime import timedelta
from base64 import b64encode
import jwt
from flask_cors import CORS

es = Elasticsearch(['localhost:9200'])
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(seconds=24 * 60 * 60)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:wysxht12@47.100.138.195/kitchen"


app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#获取SQLAlchemy实例对象，接下来就可以使用对象调用数据

db = SQLAlchemy(app)
from user_controller import login, register, getUserInfo, save_user_search_record


@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/search',  methods=['POST','GET'])
def search():
    username=session.get('username')

    print ("request ",request.args)
    keyword = request.args['keyword']
    if username:
        state = save_user_search_record(username,keyword)
    from_set = request.args['from']
    from_set=int(from_set)
    print(" keyword",keyword)
    body = {
  "query":{
    "multi_match":{
      "query":keyword,
      "fields":["name","materials.material_name","tags_dist.tag_name","description"],

    },

  },
        "size": 10,
        "from": from_set,

}
    # 查询name="python"的所有数据
    res = es.search(index="recipe*", body=body)
    data={
        "code":200,
        "msg":"搜索成功",
        "data":res['hits']
    }
    return jsonify(data)
@app.route('/recommend',methods=['POST','GET'])
def recmmend_():
    from_set = request.args['from']
    body = {
        "query": {"match_all": {}},
        "size": 10,
        "from": from_set,
        "sort": [
            {
                "cooked": {
                    "order": "desc"
                },

            }
        ]
    }
    res = es.search(index="recipe*", body=body)
    data = {
        "code": 200,
        "msg": "搜索成功",
        "data": res['hits']
    }
    return data;

@app.route('/login', methods=['POST'])
def login_():
    username = request.form.get("username")
    password = request.form.get('password')
    state=login(username,password)
    if state==-1:
        res = {"code": 400,
               "msg": "登录失败"}
    else:
        session.permanent = True
        session['username'] = username
        res = {"code": 200,
               "msg": "登录成功"}
    return jsonify(res)
@app.route('/register', methods=['POST'])
def register_():
    username = request.form.get("username")
    password = request.form.get('password')
    state=register(username,password)
    if state==-1:
        res={"code":400,
             "msg":"注册失败"}
    else :
        res = {"code":200,
               "msg": "注册成功"}
    return jsonify(res)
@app.route('/logout',methods=['POST','GET'])
def loginout_():
    session.clear()
    res = {"code": 200,
           "msg": "退出成功"}
    return jsonify(res)

@app.route('/getUserInfo', methods=['POST','GET'])
def get_user_info():

    username=session.get("username")
    res=getUserInfo(username)

    return  jsonify(res)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8081)
