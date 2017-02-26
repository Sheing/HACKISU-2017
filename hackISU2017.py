from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from auth import TwitterAuth
import json
import pymongo

#collect the tweets in this list
search = []

class StdOutListener(StreamListener):
	
	#This function gets called every time a new tweet is received on the stream
	def on_data(self, data):
		
		#Convert the tweet data to a json object 
		j=json.loads(data)
		#append tweet to search list
		search.append(j)

		print len(search)
		
if __name__ == '__main__':
	
	# Connection to Mongo DB
	try:
		conn=pymongo.MongoClient()
		print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
		print "Could not connect to MongoDB: %s" % e 

	###PLEASE CHANGE THE FOLLOWING LINE
	db = conn.HACKISU2017_tweetsdb #creates a database, if needed
	posts = db.posts #creates collection, if needed

	try:
		#Create the listener
		l = StdOutListener()
		auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
		auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

		#Connect to the Twitter stream
		stream = Stream(auth, l)	

        #Terms to track
        #stream.Filter(track=['hackisu'])
		#Alternatively, location box  for geotagged tweets
		#stream.filter(locations=[-0.530, 51.322, 0.231, 51.707]) #london
		#stream.filter(locations=[-96.0,40.5,-91.0,43.5])		   #iowa
		stream.filter(locations=[-124.5, 25.0, -67.0, 47.5]) #continental U.S. rectangle

	except KeyboardInterrupt:
		#User pressed ctrl+c -- get ready to exit the program
		pass

	for tweet in search:
    # Empty dictionary for storing tweet related data
		data ={}
		data['followers_count'] = tweet[u'user'][u'followers_count']
		data['lang'] = tweet[u'lang']
		data['text'] = tweet[u'text']
		data['hashtags'] =tweet[u'entities'][u'hashtags']
		data['screen_names']=tweet[u'user'][u'screen_name']
		#data['text'] = tweet[u'text']
		#data ['city']=tweet[u'place'][u'street_address']
		data['place']=tweet[u'place']
	
		
    	# Insert document into collection
		posts.insert(data)


