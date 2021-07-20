class Participant(object):
    def __init__(self,name,champion,team_position,gold_earned,gold_2,gold_4,gold_6,pos_2,pos_4,pos_6,jungle_minions_2,jungle_minions_4,jungle_minions_6,minions_2,minions_4,minions_6,damage_dealt_2,damage_dealt_4,damage_dealt_6):
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
        self.team_position = team_position
        
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
                lane: \t%s\n \
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
                " % (self.name,self.champion,self.team_position, self.gold_earned,self.gold_2,self.gold_4,self.gold_6,
                     self.pos_2,self.pos_4,self.pos_6,self.damage_dealt_2,self.damage_dealt_4,self.damage_dealt_6)
    
        
        
        