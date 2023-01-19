import tweepy
import pandas as pd
from datetime import datetime

bearer_token = "My bearer token"

client = tweepy.Client(bearer_token=bearer_token)

def crawl_tweets():
    tweets = client.search_recent_tweets(query="#elonmusk",max_results=10)[0]
    tweets_list=[]
    for tweet in tweets:
        tweets_list.append({"id":tweet.id,"text":tweet.text})


    return(tweets_list)
