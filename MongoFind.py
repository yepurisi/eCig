__author__ = 'sidhardha'

import pymongo
from pymongo import MongoClient
import html
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

    #Removing HTML Characters
    #HTML_Parser = HTMLParser
    tweet = html.unescape(tweet)

    #Decoding the character set
    tweet = tweet.encode('ascii', 'ignore').decode(encoding='utf-8')

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

    #Parse Multiple words written together
    reformedTweet = " ".join(re.findall('[A-Z][^A-Z]*', reformedTweet))

    #Converting the case to be consistent
    reformedTweet = reformedTweet.lower()

    return reformedTweet


count = 0
tweets_iterator = collection.find()
for eachTweet in tweets_iterator:
    count = count + 1
    print ("*" * 80)
    print (eachTweet['text'])
    print (preProcessTweet(eachTweet['text']))
    if count == 30:
        break

