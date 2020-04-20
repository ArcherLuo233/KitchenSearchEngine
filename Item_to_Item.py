import math
import pandas as pd
import jieba
import pymysql
from pymysql.cursors import DictCursor
from tqdm import tqdm
import json
from SearchHistory import SearchHistory
from User import User
from app import db
import datetime
from R_T import R_T
from Recipe import Recipe
from Tags import  Tags
conn = pymysql.Connect(
    host = "47.100.138.195",
    port = 3306,
    user = "root",
    passwd = "wysxht12",
    db = "kitchen",
)

def getorgindata():
    #取所有数据
    # sql = "select id,pv from recipe "
    # cursor.execute(sql)
    # result = cursor.fetchall()
    result = Recipe.query.all()
    return result
def getalltag():
    # 取所有tag_id-tag
    alltag = {}
    # sql = 'select * from tags'
    # cursor.execute(sql)
    # tag = cursor.fetchall()
    tag=Tags.query.all()
    for i in tag:
        alltag.update({i.id: i.tag})
    return alltag
def getrelationship():
    # 取recipe_id-tag_id
    # sql = 'select * from r_t'
    # cursor.execute(sql)
    # re = cursor.fetchall()
    re=R_T.query.all()
    relationship = {}
    for i in re:
        if i.recipe_id in relationship:
            relationship[i.recipe_id ].append(i.tag_id)
        else:
            relationship.update({i.recipe_id: [i.tag_id]})
    return relationship
def getrecommendItem(targetId):

    data=getorgindata()
    searchrecipe=''
    alldatagrades=[]
    alltag={}

    #取所有tag_id-tag

    alltag=getalltag()
    # 取recipe_id-tag_id

    relationship=getrelationship()

    remberid={}
    similar={}

    #targetId='104437056'
    #取当前个id，pv
    # sql='select id,pv from recipe where id={}'.format(targetId)
    # cursor.execute(sql)
    # i = cursor.fetchone()
    i=Recipe.query.filter_by(id=targetId).first()
    id1=i.id
    s1num = i.pv
    # 找当前个的标签
    if (id1 in remberid):
        ftag=remberid[id1]
    else:
        try:
            tagid1=relationship[id1]
        except:
            tagid1=[]
        ftag=[]
        for tt in tagid1:
            ftag=list(set(ftag+jieba.lcut_for_search(alltag[tt])))
        remberid.update({id1:ftag})

    rg = tqdm(data, desc='进行中')
    for j in rg:
        if (i==j): continue
        s2num = j.pv
        id2 = j.id
        # 找对应的另一个的标签
        stag = []
        if (id2 in remberid):
            stag=remberid[id2]
        else:
            try:
                tagid2=relationship[id2]
            except:
                tagid2=[]
            for tt in tagid2:
                stag=list(set(stag+jieba.lcut_for_search(alltag[tt])))
            remberid.update({id2:stag})
        #寻找相同项

        same=0
        for k1 in ftag:
            for k2 in stag:
                if k1==k2:
                    same+=1
                    break
        if (s1num==0): s1num=1
        if (s2num==0): s2num=1
        if(same==0):
            same=min(s1num,s2num)/20
        else :
            allsize=len(list(set(stag+ftag)))
            same=min(s1num,s2num)*same//allsize
        similar.update({str((id2)):same/math.sqrt(s1num*s2num)})
    similar = sorted(similar.items(), key=lambda x: x[1], reverse=True)
    ans=[]
    for index,i in enumerate(similar):
        if (index>=10):break;
        s = Recipe.query.filter_by(id=i[0]).first()
        tmp={
            "id":s.id,
            "name":s.name,
            "pv":s.pv,
            "img":s.img,
            "deccription":s.description
        }
        ans.append(tmp)

    return {
        "code": 200,
        "msg": "获取成功",
        "data": {
            "username":ans
        }
    }











