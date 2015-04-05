__author__ = 'sidhardha'

import pymongo
from pymongo import MongoClient
from html.parser import HTMLParser
import re
import pprint

client = MongoClient('localhost', 27017)
db = client['twitter_test_db']
collection = db['twitter_test']

db.collection.ensure_index([('id_str', pymongo.ASCENDING),("unique",True), ("dropDups",True)])

def preProcessTweet(incomingTweet):

    #Remove whitespace characters except space / Flattens the tweets in multiple lines
    tweet = re.sub('\s+', ' ', incomingTweet)

    #Replace multiple spaces with single space
    tweet = re.sub(' +', ' ', tweet)

    #Converting the case to be consistent
    tweet = tweet.lower()

    #Removing HTML Characters
    HTML_Parser = HTMLParser.HTMLParser()
    tweet = HTML_Parser.unescape(tweet)

    #Decoding the character set
    tweet = tweet.decode(encoding='utf-8').encode('ascii', 'ignore')

    #Removing URLs in Tweets
    tweet = re.sub('http://[\w\./]*', '', tweet)
    tweet = re.sub('https://[\w\./]*', '', tweet)

    #Removing/Transforming the apostrophes
    apostrophes = {"'s": " is", "'re": " are", "'ve": " have", "'d": " had"} #can extend the list
    reformedTweet = " ".join([apostrophes[word] if word in apostrophes else word for word in tweet.split()])
    #Replace quotes with null
    reformedTweet = reformedTweet.replace("'\"", "")

    #Remove user mentions
    reformedTweet = re.sub('@\w+', '', reformedTweet)

    #Remove hash tags
    reformedTweet = reformedTweet.replace('#', '')


    return reformedTweet


count = 0
tweets_iterator = collection.find()
for eachTweet in tweets_iterator:
    count = count + 1
    print ("*" * 80)
    print (eachTweet['text'])
    #tweet = " ".join([word for word in re.findall('http\w./', eachTweet['text'])])
    tweet = re.sub('http://[\w\./]*', '', eachTweet['text'])
    print (tweet)
    if count == 30:
        break

