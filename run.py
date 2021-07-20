import requests
from decouple import config
import sys
from analyze import analyze
from classes import Participant
from helper_functions import build_url
from normalize import normalize
import numpy as np
import joblib
from bson.objectid import ObjectId
from sklearn.preprocessing import StandardScaler


key = config('KEY')
key_param = ("api_key",key)


positionsDict = dict()
positionsDict[0] = "JGL"
positionsDict[1] = "TOP"
positionsDict[2] = "MID"
positionsDict[3] = "BOT"
positionsDict[4] = "SUP"

def addDataFromAPI(participant):
    if participant.team_position == "TOP":
        labels.append(1)
    elif participant.team_position == "MIDDLE":
        labels.append(2)
    elif participant.team_position == "JUNGLE":
        labels.append(0)
    elif participant.team_position == "BOTTOM":
        labels.append(3)
    elif participant.team_position == "UTILITY":
        labels.append(4)
    else:
        return
    gold_2.append(participant.gold_2)
    gold_4.append(participant.gold_4)
    gold_6.append(participant.gold_6)
    pos_2x.append(participant.pos_2[0])
    pos_6x.append(participant.pos_4[0])
    pos_4x.append(participant.pos_6[0])
    pos_2y.append(participant.pos_2[1])
    pos_4y.append(participant.pos_4[1])
    pos_6y.append(participant.pos_6[1])
    jgl_min_2.append(participant.jungle_minions_2)
    jgl_min_4.append(participant.jungle_minions_4)
    jgl_min_6.append(participant.jungle_minions_6)
    min_2.append(participant.minions_2)
    min_4.append(participant.minions_4)
    min_6.append(participant.minions_6)
    damage_2.append(participant.damage_dealt_2)
    damage_4.append(participant.damage_dealt_4)
    damage_6.append(participant.damage_dealt_6)
    
    
    
    

def reset():
    global total, labels, gold_2, gold_4, gold_6, pos_2x, pos_4x, pos_6x, pos_2y, pos_4y, pos_6y, jgl_min_2, jgl_min_4, jgl_min_6, min_2, min_4, min_6, damage_2, damage_4, damage_6
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

def prep_x():
    global total, labels, gold_2, gold_4, gold_6, pos_2x, pos_4x, pos_6x, pos_2y, pos_4y, pos_6y, jgl_min_2, jgl_min_4, jgl_min_6, min_2, min_4, min_6, damage_2, damage_4, damage_6
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

def init_vars():
    global total, labels, gold_2, gold_4, gold_6, pos_2x, pos_4x, pos_6x, pos_2y, pos_4y, pos_6y, jgl_min_2, jgl_min_4, jgl_min_6, min_2, min_4, min_6, damage_2, damage_4, damage_6
    
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

def run():
    init_vars()
    summoner = input("put summoner name\n")
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s?" % (summoner)
    summoner_url = build_url(url,key_param)
    summonerData = requests.get(url=summoner_url).json()
    print(summoner_url,summonerData)
    
    #need to handle exceptions
    summ_id = summonerData['id']
    account_id = summonerData['accountId']
    puuid = summonerData['puuid']
    
    #get recent 20 matches
    url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/%s/ids?" % (puuid)
    queue_param = ("queue","420")
    match_param = ("type","ranked")
    start_param = ("start","0")
    count_param = ("count","100")
    match_url = build_url(url,match_param,start_param,count_param,key_param)
    print(match_url)
    getMatches = requests.get(url = match_url).json()
    newclf = joblib.load('my_model.pkl')
    
    for match in getMatches:
        print("new match with number ",match)
        names = []
        participants = analyze(match)
        for participant in participants:
            addDataFromAPI(participant)
            names.append(participant)
        prep_x()

        normalized = np.transpose(np.array(normalize(total)))


        #X_train, X_test, y_train, y_test = train_test_split(normalized,labels,random_state=1, test_size=0.1)
        sc_X = StandardScaler()
        #X_trainscaled=sc_X.fit_transform(X_train)

        X_test = normalized
        y_test = labels


        X_testscaled=sc_X.fit_transform(X_test)

        y_pred=newclf.predict(X_testscaled)
        for i in range(len(y_pred)):
            print(i)
            print("predicted %s to play in lane %s(predict) instead of lane %s(true)" % (names[i].champion,positionsDict[y_pred[i]],positionsDict[y_test[i]]))

        
        reset()
        print(total)
        print(labels)


    

if __name__ == "__main__":
    run()