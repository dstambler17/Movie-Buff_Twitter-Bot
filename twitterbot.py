import tweepy
import time
import requests
import json
import random

CONSUMER_KEY = 'Ln97L2Sye1w8qf5VJ8GY3x5S5'
CONSUMER_SECRET = 'AXIxtwf37tPlbgTmR5mq8aPBDUFoHwkRivA1ofAGmwf6I7YvGP'
ACCESS_KEY = '1128674142021193728-1fMFVrPwk7caHXC6CdSBOdhviC46XV'
ACCESS_SECRET = 'Q8SuxYJKlm6iCyyMC1M9Vag5dsOY3r5KCztYGGUfGlwmQ'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'savedInfo.json'
MOVIE_FILE_NAME = 'movie_List.txt'

#Read most recent and list of users
def read_info(file_name):
    with open(file_name, 'r') as f_read:
        info = json.load(f_read)
    f_read.close()
    return info

#Save info dict: most recent and list of users
def write_info(res_data, file_name):
    with open(file_name, 'w') as f_write:
        json.dump(res_data, f_write)
    f_write.close()
    return

def read_movie_quotes(file_name):
    with open(file_name, encoding="utf-8") as file:
        movie_quotes = file.readlines()
    movie_quotes = [item.strip() for item in movie_quotes]
    file.close()
    return movie_quotes


def getRandomQuote(movie_quotes):
    num = random.randint(1,101)
    location = str(num) + '___'
    res = movie_quotes[num - 1].split('___')[1]
    return res

def thankUser(data, mention):
    if mention.user.screen_name not in data["mention_count"]:
        data["mention_count"][mention.user.screen_name] = 1
    else:
        count = data["mention_count"][mention.user.screen_name] + 1
        if count == 5:
            api.create_friendship(mention.user.screen_name)
        if count == 10:
            api.update_status('@'+ mention.user.screen_name + " Hey bud, thanks so much for engaging with me! :)")
        data["mention_count"][mention.user.screen_name] = count
    return data

#Method for replying
def reply(mention, movie_quotes):
    if '#quoteplease' in mention.full_text.lower():
        print('found #quoteplease')
        print('responding back...')
        quote = getRandomQuote(movie_quotes)
        print(quote)
        api.update_status('@' + mention.user.screen_name + ' ' + quote, mention.id)
    if '#sources' in mention.full_text.lower():
        print('found #sources')
        print('responding back')
        sources = 'I am pulling from a list on the top 100 movie quotes. This list was compiled by the American Film Institute, and taken from infoplease: \
        https://www.infoplease.com/arts-entertainment/movies-and-videos/top-100-movie-quotes.'
        api.update_status('@' + mention.user.screen_name + ' ' + sources, mention.id)
    return

#Credit to YKDojo Twitter Tutorial Youtube Channel for outline of reply function
def engage(movie_quotes):
    print('And replying to tweets...')
    data = read_info(FILE_NAME)
    last_seen_id = int(data["last_used"])
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        data["last_used"]= str(mention.id)
        data = thankUser(data, mention)
        write_info(data, FILE_NAME)
        print(mention.full_text)
        reply(mention, movie_quotes)


QUOTE_LIST = read_movie_quotes(MOVIE_FILE_NAME)
for quote in QUOTE_LIST:
    print(quote)
while True:
    engage(QUOTE_LIST)
    time.sleep(15)

'''NEXT STEPS: 1) Add list to text file after scrapping. Have App (using code similar to vid) reply to a tweet with a random movie quote
from that list everytime someone tweets the app DONE
2) Have app follow anyone who asks that question 5 times
3) Binary search
4) Have the app reply to tweets asking where I got the movie quote from with "All Credit goes to American Enterprise Institute" DONE
You can save all info as a json and just read/write to/from file
5) If a person tweets 10 times have app thank person for engaging with app via message'''
