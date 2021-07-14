import requests

def run():

    key = "RGAPI-b9d3fc35-eb1b-4912-8096-18a0856a1539"
    print("hi")
    
    summoner = input("put summoner name\n")
    summonerData = (requests.get(url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s?api_key=%s" % (summoner,key))).json()
    
    #need to handle exceptions
    summ_id = summonerData['id']
    account_id = summonerData['accountId']
    puuid = summonerData['puuid']
    
    

    

if __name__ == "__main__":
    run()