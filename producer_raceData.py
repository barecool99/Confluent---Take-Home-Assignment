import json
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from token import EXACT_TOKEN_TYPES
from confluent_kafka import Producer
from datetime import datetime

from f1_python import getLastRound, getRaceData


if __name__ == '__main__':
    '''
        Config parser from:
        https://developer.confluent.io/get-started/python/#build-producer
    '''
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    # Create Producer instance
    producer = Producer(config)
    topic = "tpc-race-data"
    
    while True:
        season = 2020 # Default season

        for s in range(1955, 2021):
            season = s

            lastRound = getLastRound(season)

            #print (lastRound)

            for round in range(1, lastRound + 1):
                if round > lastRound:
                    print (f'All race data sent for the {season} season.')
                    break

                else:
                    #print (f'round = {round}')
                    #print (f'last round = {lastRound}')

                    raceData = getRaceData(season, round)
                    raceData_JSON = json.dumps(raceData).encode('utf-8')
                    
                    # Key consists of race year + round.
                    # Round 12 in the 2017 season ==> 2017-12

                    raceData_Key = raceData['raceID']

                    print (raceData_Key)

                    producer.produce(topic, value = raceData_JSON, key = raceData_Key)
                    print (f'\nMessage sent @ {datetime.now()} | Message: \n {str(raceData_JSON)}')

        producer.poll(10000)
        producer.flush()
        break # Ends loop rather than cycling through dataset infinitely