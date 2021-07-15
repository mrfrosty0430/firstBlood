import requests


class Participant(object):
    def __init__(self,name,champion,gold_earned):
        self.name = name
        self.champion = champion
        self.gold_earned = gold_earned
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

        return "summoner name: \t%s\nchampion: \t%s\ngold earned: \t%s" % (self.name,self.champion,self.gold_earned)
    
        
        
        


key = "RGAPI-b9d3fc35-eb1b-4912-8096-18a0856a1539"
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
    for participant in info["info"]["participants"]:
        new = Participant(participant["summonerName"],participant["championName"],participant["goldEarned"])
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
        analyze(match)

    

if __name__ == "__main__":
    run()