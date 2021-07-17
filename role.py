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


key = "RGAPI-71749747-7eec-45c7-b4e8-d34f3bae967d"
key_param = ("api_key",key)

class Participant(object):
    def __init__(self,champion,gold_earned,gold_2,gold_4,gold_6,pos_2,pos_4,pos_6,jungle_minions_2,jungle_minions_4,jungle_minions_6,minions_2,minions_4,minions_6,damage_dealt_2,damage_dealt_4,damage_dealt_6):
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

        return "champion: \t%s\n \
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
                " % (self.champion,self.gold_earned,self.gold_2,self.gold_4,self.gold_6,
                     self.pos_2,self.pos_4,self.pos_6,self.damage_dealt_2,self.damage_dealt_4,self.damage_dealt_6)
    
        
def build_url(url, *params):
    for param in params:
        print(param)
        field = param[0]
        value = param[1]
        url = url + "%s=%s&" % (field,value)
    url = url[:-1]
    return url
        
        



def parse(games):
    for game in games:
        match = game[:-2]
        url = "https://euw1.api.riotgames.com/lol/match/v4/matches/%s?" % (match)
        match_url = build_url(url,key_param)
        info = requests.get(url=match_url).json()
        url = "https://euw1.api.riotgames.com//lol/match/v4/timelines/by-match/%s?" % (match)
        timeline_url = build_url(url,key_param)
        timeline_info = requests.get(url=timeline_url).json()

        for i in range(len(info["participants"])):
            participant = info["participants"][i]
            championName = participant["championName"]
            goldEarned = participant["goldEarned"]
            gold_2 = timeline_info["frames"][2]["participantFrames"][str(i+1)]["totalGold"]
            gold_4 = timeline_info["frames"][4]["participantFrames"][str(i+1)]["totalGold"]
            gold_6 = timeline_info["frames"][6]["participantFrames"][str(i+1)]["totalGold"]
            pos_2 = (timeline_info["frames"][2]["participantFrames"][str(i+1)]["position"]["x"],timeline_info["frames"][2]["participantFrames"][str(i+1)]["position"]["y"])
            pos_4 = (timeline_info["frames"][4]["participantFrames"][str(i+1)]["position"]["x"],timeline_info["frames"][4]["participantFrames"][str(i+1)]["position"]["y"])
            pos_6 = (timeline_info["frames"][6]["participantFrames"][str(i+1)]["position"]["x"],timeline_info["frames"][6]["participantFrames"][str(i+1)]["position"]["y"])
            jungle_minions_2 = timeline_info["frames"][2]["participantFrames"][str(i+1)]["jungleMinionsKilled"]
            jungle_minions_4 = timeline_info["frames"][4]["participantFrames"][str(i+1)]["jungleMinionsKilled"]
            jungle_minions_6 = timeline_info["frames"][6]["participantFrames"][str(i+1)]["jungleMinionsKilled"]
            minions_2 = timeline_info["frames"][2]["participantFrames"][str(i+1)]["minionsKilled"] - jungle_minions_2
            minions_4 = timeline_info["frames"][4]["participantFrames"][str(i+1)]["minionsKilled"] - jungle_minions_4
            minions_6 = timeline_info["frames"][6]["participantFrames"][str(i+1)]["minionsKilled"] - jungle_minions_6
            damage_dealt_2 = timeline_info["frames"][2]["participantFrames"][str(i+1)]["damageStats"]["totalDamageDoneToChampions"]
            damage_dealt_4= timeline_info["frames"][4]["participantFrames"][str(i+1)]["damageStats"]["totalDamageDoneToChampions"]
            damage_dealt_6 = timeline_info["frames"][6]["participantFrames"][str(i+1)]["damageStats"]["totalDamageDoneToChampions"]

            new = Participant(championName,goldEarned,gold_2,gold_4,gold_6,pos_2,pos_4,pos_6,jungle_minions_2,jungle_minions_4,jungle_minions_6,minions_2,minions_4,minions_6,damage_dealt_2,damage_dealt_4,damage_dealt_6)
            print(new)
            break


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