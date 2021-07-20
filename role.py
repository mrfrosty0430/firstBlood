##TODO


#first use data dragon to see what runes are used.

#then find the following features

#position(x,y) at 2 mins, 4 mins, 6 mins
#gold at 2 mins, 4 mins, 6 mins
#minions killed
#jungle minions killed
#damage dealt
#runes

#then compare with champion playrates

from sklearn import preprocessing
import csv, requests
from pymongo import MongoClient
from matches import match_list
from time import sleep
from classes import Participant
from decouple import config

key = config('KEY')
key_param = ("api_key",key)
client = MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.scjiy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.RiotData




def parse(games):
    collection = db.newData
    for j in range(len(match_list)):
        if j % 50 == 0 and j > 0:
            print("sleeping cuz too many requests")
            sleep(120)
            print("done sleeping")
        game = match_list[j]
        
        try:
            match = "KR_" + str(game)
            url = "https://asia.api.riotgames.com/lol/match/v5/matches/%s?" % (match)
            match_url = build_url(url,key_param)
            info = requests.get(url=match_url).json()
            url = "https://asia.api.riotgames.com/lol/match/v5/matches/%s/timeline?" % (match)
            timeline_url = build_url(url,key_param)
            timeline_info = requests.get(url=timeline_url).json()

            teams = dict()
            teams["A"] = []
            teams["B"] = []
            for i in range(len(info["info"]["participants"])):
                participant = info["info"]["participants"][i]
                summonerName = participant["summonerName"]
                championName = participant["championName"]
                teamPosition = participant["teamPosition"]
                goldEarned = participant["goldEarned"]
                gold_2 = timeline_info["info"]["frames"][2]["participantFrames"][str(i+1)]["totalGold"]
                gold_4 = timeline_info["info"]["frames"][4]["participantFrames"][str(i+1)]["totalGold"]
                gold_6 = timeline_info["info"]["frames"][6]["participantFrames"][str(i+1)]["totalGold"]
                pos_2 = (timeline_info["info"]["frames"][2]["participantFrames"][str(i+1)]["position"]["x"],timeline_info["info"]["frames"][2]["participantFrames"][str(i+1)]["position"]["y"])
                pos_4 = (timeline_info["info"]["frames"][4]["participantFrames"][str(i+1)]["position"]["x"],timeline_info["info"]["frames"][4]["participantFrames"][str(i+1)]["position"]["y"])
                pos_6 = (timeline_info["info"]["frames"][6]["participantFrames"][str(i+1)]["position"]["x"],timeline_info["info"]["frames"][6]["participantFrames"][str(i+1)]["position"]["y"])
                jungle_minions_2 = timeline_info["info"]["frames"][2]["participantFrames"][str(i+1)]["jungleMinionsKilled"]
                jungle_minions_4 = timeline_info["info"]["frames"][4]["participantFrames"][str(i+1)]["jungleMinionsKilled"]
                jungle_minions_6 = timeline_info["info"]["frames"][6]["participantFrames"][str(i+1)]["jungleMinionsKilled"]
                minions_2 = timeline_info["info"]["frames"][2]["participantFrames"][str(i+1)]["minionsKilled"] - jungle_minions_2
                minions_4 = timeline_info["info"]["frames"][4]["participantFrames"][str(i+1)]["minionsKilled"] - jungle_minions_4
                minions_6 = timeline_info["info"]["frames"][6]["participantFrames"][str(i+1)]["minionsKilled"] - jungle_minions_6
                damage_dealt_2 = timeline_info["info"]["frames"][2]["participantFrames"][str(i+1)]["damageStats"]["totalDamageDoneToChampions"]
                damage_dealt_4= timeline_info["info"]["frames"][4]["participantFrames"][str(i+1)]["damageStats"]["totalDamageDoneToChampions"]
                damage_dealt_6 = timeline_info["info"]["frames"][6]["participantFrames"][str(i+1)]["damageStats"]["totalDamageDoneToChampions"]

                new = Participant(summonerName,championName,goldEarned,gold_2,gold_4,gold_6,pos_2,pos_4,pos_6,jungle_minions_2,jungle_minions_4,jungle_minions_6,minions_2,minions_4,minions_6,damage_dealt_2,damage_dealt_4,damage_dealt_6)
                dictdata = {
                    "id": i+1,
                    "summonerName" : summonerName,
                    "championName" : championName,
                    "teamPosition" : teamPosition,
                    "goldEarned" : goldEarned,
                    "gold_2" : gold_2,
                    "gold_4" : gold_4,
                    "gold_6" : gold_6,
                    "pos_2" : pos_2,
                    "pos_4" : pos_4,
                    "pos_6" : pos_6,
                    "jungle_minions_2" : jungle_minions_2,
                    "jungle_minions_4" : jungle_minions_4,
                    "jungle_minions_6" : jungle_minions_6,
                    "minions_2" : minions_2,
                    "minions_4" : minions_4,
                    "minions_6" : minions_6,
                    "damage_dealt_2" : damage_dealt_2,
                    "damage_dealt_4" : damage_dealt_4,
                    "damage_dealt_6" : damage_dealt_6
                }
                if i < 5:
                    teams["A"].append(dictdata)
                else:
                    teams["B"].append(dictdata)
            collection.update_one(teams,{"$set":teams},upsert=True)

        except Exception as e: print(e)
        


def main():
    with open('verification_results.csv',newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        games = []
        team_A_roles = []
        team_B_roles = []
        for row in csvreader:
            games.append(row[11])
            team_A_roles.append([row[1],row[3],row[4],row[5],row[6]])
            team_B_roles.append([row[7],row[8],row[9],row[10],row[2]])
        
        games = games[1:]
        
        data = parse(games)





if __name__ == "__main__":
    main()