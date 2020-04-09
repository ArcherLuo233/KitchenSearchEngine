from SearchHistory import SearchHistory
from User import User
from app import db
import datetime
def register(username,password):
    if username=="" or password=="":
        return -1
    s = User.query.filter_by(username=username).first()
    if (s):
        return -1

    user=User(username=username,password=password)
    db.session.add(user)
    db.session.commit()
    return 1
def login(username,password):
    if username=="" or password=="":
        return -1
    user = User.query.filter_by(username=username).first()
    if password==user.password:
        return 1
    else:
        return -1

def getUserInfo(username):

    if username=="":

        return {
            "code":400,
            "msg":"用户名为空",
            "data":None
        }
    user = User.query.filter_by(username=username).first()
    if user==None:
        return {
            "code": 400,
            "msg": "用户不存在",
            "data": None
        }
    return {
        "code": 200,
        "msg": "获取成功",
        "data": {
            "username":user.username
        }
    }

def save_user_search_record(username,keyword):
    s = User.query.filter_by(username=username).first()
    sh=SearchHistory(user_id=s.id,keyword=keyword,time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(sh)
    db.session.commit()
    return 1