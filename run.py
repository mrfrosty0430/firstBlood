import requests
import sys

class Participant(object):
    def __init__(self,name,champion,gold_earned,gold_2,gold_4,gold_6,pos_2,pos_4,pos_6,jungle_minions_2,jungle_minions_4,jungle_minions_6,minions_2,minions_4,minions_6,damage_dealt_2,damage_dealt_4,damage_dealt_6):
        self.name = name
        self.champion = champion
        self.gold_earned = gold_earned
        self.gold_2 = gold_2
        self.gold_4 = gold_4
        self.gold_6 = gold_6
        self.pos_2 = pos_2
        self.pos_4 = pos_4
        self.pos_6 = pos_6
        self.jungle_minions_2 = jungle_minions_2
        self.jungle_minions_4 = jungle_minions_4
        self.jungle_minions_6 = jungle_minions_6
        self.minions_2 = minions_2 - self.jungle_minions_2
        self.minions_4 = minions_4 - self.jungle_minions_4
        self.minions_6 = minions_6 - self.jungle_minions_6
        self.damage_dealt_2 = damage_dealt_2
        self.damage_dealt_4 = damage_dealt_4
        self.damage_dealt_6 = damage_dealt_6
        
        '''
        self.damage_dealt = damage_dealt
        self.vision_score = vision_score
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        if deaths == 0:
            self.kda = kills + assists
        else:
            self.kda = (kills + assists)/ deaths
        '''
    
    
    def __repr__(self):

        return "summoner name: \t%s\n \
                champion: \t%s\n \
                gold earned: \t%s\n \
                gold at 2: \t%s\n \
                gold at 4: \t%s\n \
                gold at 6: \t%s\n \
                pos at 2: \t%r\n \
                pos at 4: \t%r\n \
                pos at 6: \t%r\n \
                damage dealt at 2: \t%s\n \
                damage dealt at 4: \t%s\n \
                damage dealt at 6: \t%s\n \
                " % (self.name,self.champion,self.gold_earned,self.gold_2,self.gold_4,self.gold_6,
                     self.pos_2,self.pos_4,self.pos_6,self.damage_dealt_2,self.damage_dealt_4,self.damage_dealt_6)
    
        
        
        


key = "RGAPI-71749747-7eec-45c7-b4e8-d34f3bae967d"
key_param = ("api_key",key)
def build_url(url, *params):
    for param in params:
        print(param)
        field = param[0]
        value = param[1]
        url = url + "%s=%s&" % (field,value)
    url = url[:-1]
    return url
        

def analyze(match):
    url = "https://asia.api.riotgames.com/lol/match/v5/matches/%s?" % (match)
    match_url = build_url(url,key_param)
    info = requests.get(url=match_url).json()
    url = "https://asia.api.riotgames.com/lol/match/v5/matches/%s/timeline?" % (match)
    timeline_url = build_url(url,key_param)
    timeline_info = requests.get(url=timeline_url).json()
    for i in range(len(info["info"]["participants"])):
        participant = info["info"]["participants"][i]
        summonerName = participant["summonerName"]
        championName = participant["championName"]
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
        print(new)

def run():

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
    
    
    for match in getMatches:
        #analyze(match)
        print(match)
        analyze(match)
        break

    

if __name__ == "__main__":
    run()