from enum import Enum
import csv, requests
from pymongo import MongoClient
from normalize import normalize
import numpy as np
import joblib
from bson.objectid import ObjectId

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_california_housing
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.datasets import load_iris
class positions(Enum):
    TOP=1
    MID=2
    BOT=3
    SUP=4
    JGL=0

client = MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.scjiy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.RiotData

positionsDict = dict()
positionsDict[0] = "JGL"
positionsDict[1] = "TOP"
positionsDict[2] = "MID"
positionsDict[3] = "BOT"
positionsDict[4] = "SUP"


total = []
labels = []
gold_2 = []
gold_4 = []
gold_6 = []
pos_2x = []
pos_4x = []
pos_6x = []
pos_2y = []
pos_4y = []
pos_6y = []
jgl_min_2 = []
jgl_min_4 = []
jgl_min_6 = []
min_2 = []
min_4 = []
min_6 = []
damage_2 = []
damage_4 = []
damage_6 = []


def addData(participant):
    if participant["teamPosition"] == "TOP":
        labels.append(1)
    elif participant["teamPosition"] == "MIDDLE":
        labels.append(2)
    elif participant["teamPosition"] == "JUNGLE":
        labels.append(0)
    elif participant["teamPosition"] == "BOTTOM":
        labels.append(3)
    elif participant["teamPosition"] == "UTILITY":
        labels.append(4)
    else:
        return
    gold_2.append(participant["gold_2"])
    gold_4.append(participant["gold_4"])
    gold_6.append(participant["gold_6"])
    pos_2x.append(participant["pos_2"][0])
    pos_6x.append(participant["pos_4"][0])
    pos_4x.append(participant["pos_6"][0])
    pos_2y.append(participant["pos_2"][1])
    pos_4y.append(participant["pos_4"][1])
    pos_6y.append(participant["pos_6"][1])
    jgl_min_2.append(participant["jungle_minions_2"])
    jgl_min_4.append(participant["jungle_minions_4"])
    jgl_min_6.append(participant["jungle_minions_6"])
    min_2.append(participant["minions_2"])
    min_4.append(participant["minions_4"])
    min_6.append(participant["minions_6"])
    damage_2.append(participant["damage_dealt_2"])
    damage_4.append(participant["damage_dealt_4"])
    damage_6.append(participant["damage_dealt_6"])
def readData():

    #assuming we already have db

    collection = db.newData
    cursor = collection.find({})
    #cursor = collection.find({"_id":ObjectId("60f3d5185b92c5b595de2d72")})
    names = []
    for document in cursor:
        damn = []
        for participant in document["A"]:
            addData(participant)
            damn.append((participant["championName"],participant["teamPosition"]))
            #print(participant["championName"],participant["teamPosition"])
        for participant in document["B"]:
            addData(participant)
            damn.append((participant["championName"],participant["teamPosition"]))
            #print(participant["championName"],participant["teamPosition"])
        names.append(damn)
    total.append(gold_2)
    total.append(gold_4)
    total.append(gold_6)
    total.append(pos_2x)
    total.append(pos_4x)
    total.append(pos_6x)
    total.append(pos_2y)
    total.append(pos_4y)
    total.append(pos_6y)
    total.append(jgl_min_2)
    total.append(jgl_min_4)
    total.append(jgl_min_6)
    total.append(min_2)
    total.append(min_4)
    total.append(min_6)
    total.append(damage_2)
    total.append(damage_4)
    total.append(damage_6)
    
    normalized = np.transpose(np.array(normalize(total)))
    print(normalized.shape)
    print(len(labels))

    #X_train, X_test, y_train, y_test = train_test_split(normalized,labels,random_state=1, test_size=0.1)
    sc_X = StandardScaler()
    #X_trainscaled=sc_X.fit_transform(X_train)
    
    X_test = normalized
    y_test = labels
    
    
    X_testscaled=sc_X.fit_transform(X_test)
    newclf = joblib.load('my_model.pkl')
    #clf = MLPClassifier(hidden_layer_sizes=(256,128,64,32),activation="relu",random_state=1,verbose=True,max_iter=20).fit(X_trainscaled, y_train)
    y_pred=newclf.predict(X_testscaled)
    for i in range(len(y_pred)):
        if y_pred[i] != y_test[i]:
            print(names[i // 10])
            print("predicted %s to play in lane %s(predict) instead of lane %s(true)" % (names[i//10][i%10],positionsDict[y_pred[i]],positionsDict[y_test[i]]))
            print((i%10,y_pred[i],y_test[i]))
        #print("prediction is %r, true label is %r" % (y_pred[i],y_test[i]))
    print(newclf.score(X_testscaled, y_test))
    #joblib.dump(clf, 'my_model.pkl', compress=9)



if __name__ == "__main__":
    readData()

                
    