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

def index(request):
    print 'asdjlaj'
    return 	render(request,'webapp/base.html')

def contact1(request):
	return 	render(request,'webapp/post_list.html')

def post_detail(request, pk):
      x=0

      post = get_object_or_404(Post, pk=pk)
      searchterm = wikipedia.search(post.title +" (film)")
      htmltext=""
      tiltle2=post.title+" film"
      #post.text
      default_data = {}
      for searchterm3 in searchterm:
       if ((SequenceMatcher(None, post.title +" (film)", searchterm3).ratio()) > 0.2 ):
        url = 'https://en.wikipedia.org/wiki/' + searchterm3
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'lxml')  # choose lxml parser
        image_tags = soup.findAll('img')
        table_tags = soup.findAll('table')


        for table in table_tags:
            # print (table.get('class')[0])

            if (table.get('class')):
              if (table.get('class')[0] == "infobox"):
                if (len(table.get('class'))>1):
                  if (table.get('class')[1]):
                      if (table.get('class')[1] == "vevent"):
                          comments =  table.find_all("th")[0].text
                         # print(comments)
                # iif (table.get('width') == '22em')
                          if((SequenceMatcher(None, comments +" (film)", searchterm3).ratio()) > 0.65 ):

                               default_data[searchterm3] = str(table)+'<form method="POST" action="/post/{0}/tweetmeter/{1}/">{% csrf_token %}<input type="submit" value="Submit"></form> '.format(pk,comments)
                               htmltext =htmltext+ str(table) +default_data[searchterm3]



      post.htmltext=htmltext
      post.save()
      return render(request,'webapp/post_detail.html', {
            'default_data': default_data,
        'pk': post.pk
       })



def contact123(request):   
    return render(request, 'webapp/post_detail.html')

def contact(request):
	return render(request,'webapp/basic.html', {'content':['If you like to contact me , please email me','deviprasad303@gmail.com']})

def tweetmeter(request,pk,search):
    default_data={}
    default_data[search]=search
    return render(request, 'webapp/tweetmeter.html')
    {
        'default_data': default_data,
    }
    # p2=Process(target=func2(request))
    # p1 = Process(target=func1(search))
    #
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()

# if request.method == "POST":
  #form = PostForm2(request.POST)
 # if form.is_valid():


                # for tweet in new_tweets:
                #     f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                #             '\n')
                #     post.htmltext+=tweet.text
                #     post.save()
                #     analysis = TextBlob(tweet.text)
                #     # set sentiment
                #     if analysis.sentiment.polarity > 0:
                #         positivetweets += 1
                #     if analysis.sentiment.polarity < 0:
                #         negativetweets += 1
                #     else:
                #         neutraltweets += 1
                # tweetCount += len(new_tweets)

    #             print("Downloaded {0} tweets".format(tweetCount))
    #             max_id = new_tweets[-1].id
    #         except tweepy.TweepError as e:
    #             # Just exit if any error
    #             print("some error : " + str(e))
    #             break
    # print(positivetweets)
    # print('\n')
    # print(negativetweets)
    # print('\n')
    # print(neutraltweets)
    # print('\n')
    # print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
    #
    # default_data[post.name]=post.htmltext
    # return render(request, 'webapp/tweetmeter.html', {
    #     'default_data': default_data,
    #     'search': post.search
    # })



def func1(search):
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
def func2(request):
     return render(request, 'webapp/tweetmeter.html')
     {
     'search': search,
     }
     #webbrowser.open('http://google.com')


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            title = request.POST.get("title")
            try:
             if   Post.objects.get(title=title):
                 default_data = {}
                 title = request.POST.get("title")
                 objectforthetitle = Post.objects.get(title=title)
                 default_data[objectforthetitle.title] = objectforthetitle.htmltext
                 return render(request, 'webapp/post_detail.html', {
                     'default_data': default_data,
                     'pk': objectforthetitle.pk
                 })
            except ObjectDoesNotExist:
              post = form.save(commit=False)
              post.author = request.user
              post.published_date = timezone.now()
              post.save()
              return redirect('post_detail', pk=post.pk)



    else:
        form = PostForm()
    return render(request, 'webapp/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'webapp/post_edit.html', {'form': form})