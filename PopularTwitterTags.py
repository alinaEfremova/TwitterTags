import twitter
import csv
from datetime import datetime
import logging
import requests

"""
Retrieve 50 trends for chosen countries 
Append results in corresponded csv file
"""

# logging settings
logging.basicConfig(level=logging.INFO,
                    filename='PopularTwitterTags.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

# creating session (send message if something wrong)
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
try:
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    logging.info('Successful authentication')
except Exception as e:
    # Send error message via Telegram
    requests.get("https://api.telegram.org/bot")
    logging.exception("Exception during authentication occurred")


countries = {'USA': 23424977,
             'UK': 23424975,
             'Canada': 23424775,
             'Netherlands': 23424909,
             'Russia': 23424936,
             'World': 1}

for country in countries.items():
    # take trends of the country
    try:
        trends = twitter_api.trends.place(_id=country[1])[0]['trends']
        logging.info(f'Trends for {country[0]} were retrieved')
    except Exception as e:
        # Send error message via Telegram
        requests.get("https://api.telegram.org/bot")
        logging.exception(f"Exception during retrieving trends for {country[0]} occurred")

    # timestamp as unique id
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    # saving results to csv file
    try:
        with open(f'{country[0]}.csv', 'a', encoding="utf-8") as fp:
            writer = csv.writer(fp, delimiter=',')
            for trend in trends:
                print(trend)
                row = [timestamp, trend['name'], trend['tweet_volume']]
                writer.writerow(row)
        logging.info(f'Trends for {country[0]} were added to {country[0]}.csv')
    except Exception as e:
        # Send error message via Telegram
        requests.get("https://api.telegram.org/bot")
        logging.exception(f"Exception during adding trends for {country[0]} to the {country[0]}.csv occurred")
