import requests, json, time, random

# Main API URL
URL = 'http://ergast.com/api/f1/'


def getLastRound(season):
    # Get the total # of rounds in season
    last_round_json = requests.get(URL + str(season) + '/last.json').json()

    lr_dump = json.dumps(last_round_json)
    lr_load = json.loads(lr_dump)

    lastRound = int(lr_load['MRData']['RaceTable']['round'])

    return lastRound


def getRaceData(season, round):
    '''
        Gets all the races from a specific season.
        Season refers to the year of the race.
        Round refers to the race number within that season.
    '''
    race = requests.get(URL + str(season) + '/' + str(round) + '.json').json()

    r_dump = json.dumps(race)
    r_load = json.loads(r_dump)

    # Adds a PK to the JSON for the ksqlDB table to utilise.
    key = r_load['MRData']['RaceTable']['season'] + '-' + r_load['MRData']['RaceTable']['round'] 
    r_load['MRData']['RaceTable']['raceID'] = str(key)

    # Prevents message spam to console for prod/cons.
    #time.sleep(0.5)

    #print (r_load['MRData']['RaceTable'])
    return r_load['MRData']['RaceTable']


def getDriversPerSeason(season):
    '''
        Gets all the drivers from a specific season.
        Season refers to the year of the race.
        Round refers to the race number within that season.
    '''
    drivers = requests.get(URL + str(season) + '.json').json()

    d_dump = json.dumps(drivers)
    d_load = json.loads(d_dump)

    # ['MRData']['RaceTable']['Races'][0]['date'])

    # Prevents message spam to console for prod/cons.
    time.sleep(0.5)

    #print (r_load['MRData']['RaceTable'])
    return d_load['MRData']['DriverTable']['Drivers']


if __name__ == '__main__':
    while True:
        print(getRaceData(2020, 1))