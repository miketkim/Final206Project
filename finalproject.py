#SI 206 Final Project
# Michael Kim 
# Option 2 

#Import Statements 
import requests
import unittest 
import itertools 
import collections 
import tweepy 
import twitter_info 
import json 
import sqlite3
from pprint import pprint

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Begin filling in instructions....

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OMDB caching~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

omdb_moviedata = "omdb_data.json" #caching pattern for OMDB Data 
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	omdb_diction = json.loads(cache_contents)
except:
	omdb_diction = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    OMDB API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def omdb_data(movie_title): #Defining a function to use OMDB API 	
	movie_data_by_title = requests.get('http://www.omdbapi.com?', params = {'t': movie_title})
	url = movie_data_by_title.text
	if movie_title in omdb_diction:
		return omdb_diction[movie_title]
	else:
		omdb_diction[movie_title] = url 
		omdb_data = url 
		cache_file = open(omdb_moviedata, 'w')
		cache_file.write(json.dumps(omdb_diction, indent=2))
		cache_file.close()
		return json.loads(omdb_data)

list_of_movie_titles = ['Source Code', 'Edge of Tomorrow', 'Star Wars'] #making a list of at least three movies 

movie1 = omdb_data(list_of_movie_titles[0])
movie2 = omdb_data(list_of_movie_titles[1])
movie3 = omdb_data(list_of_movie_titles[2])

list_of_movie_dictionaries = [movie1, movie2, movie3]  #Creating a list of Movie dictionaries using omdb_data function (defined above)


class Movie():
	def __init__(self, omdb_moviedata):
		self.omdb_moviedata = omdb_moviedata
		self.title = omdb_moviedata['Title']
		self.runtime = omdb_moviedata['Runtime']
		self.director = omdb_moviedata['Director']

	def get_best_actor(self):
		return self.omdb_moviedata['Actors'].split(',')[0]

	def get_number_of_languages(self):
		return len(self.omdb_moviedata['Language'].split(','))

	def get_movie_rating(self):
		return float(self.omdb_moviedata['imdbRating'])

	def get_id(self):
		return self.omdb_moviedata['imdbID']

	def __str__(self):
		return "{} is directed by {} and is {}".format(self.title, self.director, self.runtime)

movie_objects=[] 			# Creating a Movie instances in a list for three movies 
for x in list_of_movie_dictionaries:
	mov_object = Movie(x)
	movie_objects.append(mov_object)



def get_movie_data(movie_lst):  #CHANGE THIS 
	movie_tuple_list = []
	for movie in movie_objects:  
		movie_id = movie.get_id()
		movie_director = movie.director
		movie_title = movie.title
		movie_imdb_rating = movie.get_movie_rating() 
		movie_lead_actor = movie.get_best_actor()
		movie_num_lang = movie.get_number_of_languages()

		movie_tup = (movie_id, movie_title, movie_director, movie_num_lang, movie_imdb_rating, movie_lead_actor)
		movie_tuple_list.append(movie_tup)

	return movie_tuple_list

movie_tuple_list = get_movie_data(movie_objects)
print (type(movie_tuple_list))
# pprint (movie_tuple_list)






#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Tweets~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

twitter_data = "twitter_data.json"
try:
	cache_file = open(twitter_data, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	twitter_diction = json.loads(cache_contents)
except:
	twitter_diction = {}


def tweets(search):
	if search in twitter_diction:
		tweets = twitter_diction[search]
	else:
		tweets = api.search(q = search) 
		twitter_diction[search] = tweets		
		cache = open(twitter_data,'w')
		cache.write(json.dumps(twitter_diction, indent=2))
		cache.close()
	return tweets['statuses']


movie1tweets = tweets(list_of_movie_titles[0])
movie2tweets = tweets(list_of_movie_titles[1])
movie3tweets = tweets(list_of_movie_titles[2])

movietweet = [movie1tweets, movie2tweets, movie3tweets]  #Making a list of tweets using the title of each movie 
movietweetlist = zip(movietweet, list_of_movie_titles)
# pprint (movie1tweets)


tweet_tuple_list = []
for x in movietweetlist:
	for movie in x[0]:
		text = movie['text']	
		tweet_id = movie['id_str']
		user_id = movie['user']['id_str']
		favorites = movie['favorite_count']
		retweets = movie['retweet_count']
		movie_name = x[1]

		tweet_tuple = (tweet_id, text, user_id, favorites, retweets, movie_name)
		tweet_tuple_list.append(tweet_tuple)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Twitter Users~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


twitter_user_data = 'twitter_user_data.json'
try:
	cache_file = open(twitter_user_data, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	twitter_user_diction = json.loads(cache_contents)
except:
	twitter_user_diction = {}



def getting_twitter_user_info(movietweetsdict):
	twitter_user_tuples = []	
	for x in movietweetsdict:
		user_id = x['user']['id_str']
		screen_name = x['user']['screen_name']
		num_favs = x['user']['favourites_count']
		num_followers = x['user']['followers_count']
		location = x['user']['location']
		movie_tweets_user_tup = (user_id, screen_name, num_favs, num_followers, location)
		twitter_user_tuples.append(movie_tweets_user_tup)

		if screen_name not in twitter_user_diction:
			twitter_user_diction[screen_name] = x['user']
			cache_file = open(twitter_user_data, 'w')
			cache_file.write(json.dumps(twitter_user_diction, indent =2))
			cache_file.close()
	return twitter_user_tuples

def getting_twitter_user_mentions(movietweetsdict):
	twitter_user_list = []
	for x in movietweetsdict:
		user_mentions = x['entities']['user_mentions']
		for y in user_mentions:
			user_mentions_info = api.get_user(y['screen_name'])
			user_id = y['id_str']
			screen_name = y['screen_name']
			num_favs = user_mentions_info['favourites_count']
			num_followers = user_mentions_info['followers_count']
			location = user_mentions_info['location']
			movie_tweets_user_tup = (user_id, screen_name, num_favs, num_followers, location)
			twitter_user_list.append(movie_tweets_user_tup)

			if y["screen_name"] not in twitter_user_diction:
				twitter_user_diction[y["screen_name"]] = user_mentions
				cache_file = open(twitter_user_data, 'w')
				cache_file.write(json.dumps(twitter_user_diction, indent =2))
				cache_file.close()
	return twitter_user_list


movie1users = getting_twitter_user_info(movie1tweets)

movie1usermentions = getting_twitter_user_mentions(movie1tweets)

movie2users = getting_twitter_user_info(movie2tweets)

movie2usermentions = getting_twitter_user_mentions(movie2tweets)

movie3users = getting_twitter_user_info(movie3tweets)

movie3usermentions = getting_twitter_user_mentions(movie3tweets)


twitter_user_list = [movie1users + movie1usermentions + movie2users + movie2usermentions + movie3users + movie3usermentions]

twitter_touple_lst = []
for x in twitter_user_list:
	for y in x:
		twitter_touple_lst.append(y)





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SQL Database Loading~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('DROP TABLE IF EXISTS Movies')


tweets_table_spec = 'CREATE TABLE IF NOT EXISTS Tweets (tweet_id TEXT PRIMARY KEY, message TEXT, user_id TEXT, num_favs INTEGER, num_retweets INTEGER, movie_name TEXT)' 
cur.execute(tweets_table_spec)	

tweet_db = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for tweet in tweet_tuple_list:
	cur.execute(tweet_db, tweet)
conn.commit()

movies_table_spec = 'CREATE TABLE IF NOT EXISTS Movies (movie_ID TEXT PRIMARY KEY, title TEXT, director TEXT, num_languages INT, IMDB_rating TEXT, best_actor TEXT)'
cur.execute(movies_table_spec)

movie_db = "INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)"
for movie in movie_tuple_list:
	cur.execute(movie_db, movie)
conn.commit()


users_table = 'CREATE TABLE IF NOT EXISTS Users (user_ID TEXT PRIMARY KEY, user TEXT, number_favs_by_user INTEGER, number_followers INTEGER, location TEXT)'
cur.execute(users_table)

user_db = 'INSERT or IGNORE INTO Users VALUES (?, ?, ?, ?, ?)'
for user in twitter_touple_lst:
	cur.execute(user_db, user)
conn.commit()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SQL Queries~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cur.execute('SELECT user FROM Users')
list_of_screen_names = [user[0] for user in cur.fetchall()]
print (list_of_screen_names)


cur.execute("SELECT Movies.title, Users.user FROM Movies INNER JOIN Users ON Users.number_followers > 100000")
popular_followers = cur.fetchall()
print (popular_followers)

cur.execute('SELECT title, IMDB_rating FROM Movies')
movie_ratings = cur.fetchall()
print (movie_ratings)

conn.close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  DATA PROCESSING  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Data Processing Method #1: Dictionary Accumulation 

movies_getting_tweets_from_popular_users = {}
for movie in popular_followers:
	if movie[0] in movies_getting_tweets_from_popular_users: 
		movies_getting_tweets_from_popular_users[movie[0]] +=1 
	else:
		movies_getting_tweets_from_popular_users[movie[0]] = 1 

dp1 = str(movies_getting_tweets_from_popular_users)
print (dp1)

# Data Processing Method #2: Sorting 

movie_rating = sorted(movie_ratings, key = lambda x: x[-1])
movie_rating1 = "The movie " + str(movie_rating[0][0]) + " has a rating of " + str(movie_rating[0][1]) + ".  "
movie_rating2 = "The movie " + str(movie_rating[1][0]) + ' has a rating of ' + str(movie_rating[1][1]) + '.  '
movie_rating3 = "The movie " + str(movie_rating[2][0]) + " has a rating of " + str(movie_rating[2][1]) + '.  '
movie_rating_summary = movie_rating1 + movie_rating2 + movie_rating3 + "I love all these movies, but the ratings from smallest to largest are here if you like to pick movies based on that!"
print (movie_rating_summary)

# Data Processing Method #3: Mapping

# favorite_count

# Data Processing Method #4: 

# favorite_count

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Textfile Output From Data Processing Techniques ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Adding the findings from the data processing to textfile 

# Textfile = 'finalproject.txt'
# _file = open(Textfile, 'w')
# _file.write(dp1)
# _file.write(dp2)
# _file.write(dp3)
# _file.write(dp4)
# _file.close()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST CASES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The following code below is written for the purpose of testing to make sure that the program is running correctly.  

source = omdb_data('Source Code')
print (source)
# a = Movie(source)
# print (a.get_id())
# print (a.title)
# print (a.director)
# print (a.get_best_actor())

conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()
cur.execute('SELECT movie_ID FROM Movies');
result = cur.fetchall()
# print (result[1][0])


# print (movie_objects[1].get_id())
# print (movie_objects[1].title)
# print (movie_objects[1].runtime)
# print (movie_objects[1].director)
# print (movie_objects[1].get_best_actor())
# print (movie_objects[1].get_number_of_languages())
# print (movie_objects[1].get_plot())
# print (movie_objects[1].get_year_of_release())
# print (movie_objects[1].get_movie_rating())
# print (movie_objects[1].get_id())

class FunctionTests(unittest.TestCase):
	def test_omdb_data(self):
		self.assertEqual(type(movie1), dict)

	def test_get_movie_data(self):
		self.assertEqual(type(movie_tuple_list), list)

	def test_tweets(self):
		self.assertEqual(type(movie1tweets), list)

	def test_getting_twitter_user_info(self):
		self.assertEqual(type(movie1users), list)

	def test_getting_twitter_user_mentions(self):
		self.assertEqual(type(movie1usermentions), list)

class MovieClassTests(unittest.TestCase):
	def test_id(self):
		self.assertEqual(movie_objects[1].get_id(), 'tt1631867')

	def test_title(self):
		self.assertEqual(movie_objects[1].title, "Edge of Tomorrow")

	def test_best_actor(self):
		self.assertIn(movie_objects[1].get_best_actor(), 'Tom Cruise')

	def test_languages(self):
		self.assertEqual(movie_objects[1].get_number_of_languages(), 1)

	def test_rating(self):
		self.assertEqual(movie_objects[1].get_movie_rating(), 7.9)
		
	def test_string_method(self):
		self.assertEqual(movie_objects[1].__str__(), 'Edge of Tomorrow is directed by Doug Liman and is 113 min')


# ## Remember to invoke all your tests...
if __name__ == "__main__":
    unittest.main(verbosity=2)




