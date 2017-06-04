from django.urls import reverse
from webapp.forms import PostForm
from webapp.forms import PostForm2
from django.shortcuts import redirect
from django.shortcuts import render
from difflib import SequenceMatcher
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import cgi
import webbrowser
import os
import bs4 as bs
import wikipedia
import urllib
import difflib
import lxml
import sys
import jsonpickle
import os
import tweepy
from textblob import TextBlob
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from webapp.models import Post
from webapp.models import Post2
from multiprocessing import Process
from django.core.files import File


searchQuery = '#spyder'  # this is what we're searching for
maxTweets = 10000  # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'tweets.txt'  # We'll store the tweets in a text file.

# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler('R0qaWBnp3VGyptFvnCyNxc5Sq', 'L53X1qOBB5AlJXDcFUikFIwzCAaliutMDduOp2HO7kzwj6IssV')

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L

tweetCount = 0
positivetweets = 0
negativetweets = 0
neutraltweets = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet.text, unpicklable=False) +
                        '\n')
              #  print(tweet.text)
                analysis = TextBlob(tweet.text)
                # set sentiment
                if analysis.sentiment.polarity > 0:
                    positivetweets += 1
                if analysis.sentiment.polarity < 0:
                    negativetweets += 1
                else:
                    neutraltweets += 1
            tweetCount += len(new_tweets)

            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break
print(positivetweets)
print('\n')
print(negativetweets)
print('\n')
print(neutraltweets)
print('\n')
print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
