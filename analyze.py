from helper_functions import build_url
import requests
from decouple import config
from classes import Participant

key = config('KEY')
key_param = ("api_key",key)

def analyze(match):
    url = "https://asia.api.riotgames.com/lol/match/v5/matches/%s?" % (match)
    match_url = build_url(url,key_param)
    info = requests.get(url=match_url).json()
    url = "https://asia.api.riotgames.com/lol/match/v5/matches/%s/timeline?" % (match)
    timeline_url = build_url(url,key_param)
    timeline_info = requests.get(url=timeline_url).json()
    participants = []
    for i in range(len(info["info"]["participants"])):
        participant = info["info"]["participants"][i]
        summonerName = participant["summonerName"]
        championName = participant["championName"]
        goldEarned = participant["goldEarned"]
        teamPosition = participant["teamPosition"]
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
        
        new = Participant(summonerName,championName,teamPosition,goldEarned,gold_2,gold_4,gold_6,pos_2,pos_4,pos_6,jungle_minions_2,jungle_minions_4,jungle_minions_6,minions_2,minions_4,minions_6,damage_dealt_2,damage_dealt_4,damage_dealt_6)
        participants.append(new)
    return participants