# Import dependencies and init
import tweepy
import os
import time
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# init twitter api
auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"),
                           os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_KEY"), os.getenv("ACCESS_SECRET"))
twtapi = tweepy.API(auth)

# init weather api
wapi_url = 'http://api.openweathermap.org/data/2.5/weather?q='
wapi_url_end = '&appid=' + os.getenv("WEATHER_KEY")

# using external text file to get and set id of last tweet fetched
FILENAME = 'last_id.txt'


# function to get id from text file


def getlastid(filename):
    readfile = open(filename, 'r')
    lastid = int(readfile.read().strip())
    readfile.close()
    return lastid


# function to write last id into file


def setlastid(lastid, filename):
    writefile = open(filename, 'w')
    writefile.write(str(lastid))
    writefile.close()
    return


# function to remove spaces in strings


def removeSpace(string):
    return string.replace(" ", "")


# function to fetch weather data


def getWeather(location):
    wapi = wapi_url + removeSpace(location) + wapi_url_end
    response = requests.get(wapi)
    dicts = response.json()
    maindata = dicts["main"]
    temp = maindata["temp"] - 273.15
    return temp


# function to reply to mentions


def responding():
    print('Online ...')
    # Access twitter api
    lastid = getlastid(FILENAME)
    mentions = twtapi.mentions_timeline(lastid)

    # loop to iterate over fetched tweets
    for mention in reversed(mentions):
        lastid = mention.id
        setlastid(lastid, FILENAME)
        if 'good morning' in mention.text.lower():
            twtapi.update_status(
                '@' + mention.user.screen_name + ' Good Morning ' + mention.user.name + '! The current temperature in ' + mention.user.location + ' is ' + str(int(getWeather(mention.user.location))) + ' degrees.', mention.id)


# Infinite loop to keep running response function
while True:
    responding()
    time.sleep(5)
