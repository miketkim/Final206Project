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

list_of_movie_titles = ['Source Code', 'Edge of Tomorrow', 'Star Wars: Episode IV - A New Hope'] #making a list of at least three movies 

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
	movies = Movie(x)
	movie_objects.append(movies)


def movie_data_in_tuples(movie_objects):
	movie_tuple_data =[]
	for x in movie_objects:
		movie_id = x.get_id()
		movie_title = x.title
		movie_director = x.director
		movie_languages = x.get_number_of_languages()
		movie_imdb_rating = x.get_movie_rating()
		movie_best_actor = x.get_best_actor()
		movie_tuples = (movie_id, movie_title, movie_director, movie_languages, movie_imdb_rating, movie_best_actor)

		movie_tuple_data.append(movie_tuples)
	return movie_tuple_data 

movie_tuple_list = movie_data_in_tuples(movie_objects)
# print (type(movie_tuple_list))
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

tweet_db = 'INSERT or IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
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



cur.execute("SELECT Movies.Title, Tweets.num_retweets from Movies INNER JOIN Tweets on Movies.title = Tweets.movie_name")
movie_retweets = cur.fetchall()
# print (movie_retweets)

cur.execute('SELECT Movies.Title, Tweets.message from Movies INNER JOIN Tweets on Movies.title = Tweets.movie_name')
movie_tweets = cur.fetchall()
# print (movie_tweets)

cur.execute('SELECT title, IMDB_rating FROM Movies')
movie_ratings = cur.fetchall()
# print (movie_ratings)

cur.execute('SELECT Users.user, Tweets.message From Users INNER JOIN Tweets on Tweets.user_id = Users.user_ID WHERE Users.number_followers>10000')
tweets_d = cur.fetchall()
print (tweets_d)



conn.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  DATA PROCESSING  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Data Processing Method #1: Dictionary Accumulation 

movies_getting_lots_of_retweets = {}
for movie in movie_retweets:
	if int(movie[1]) > 50:
		if movie[0] in movies_getting_lots_of_retweets: 
			movies_getting_lots_of_retweets[movie[0]] += 1 
		else:
			movies_getting_lots_of_retweets[movie[0]] = 1 

retweet_summary = str(movies_getting_lots_of_retweets)
print ("The following stats on number of times one my favorites movies got over 50 retweets " + retweet_summary)

# Data Processing Method #2: Sorting 

movie_rating = sorted(movie_ratings, key = lambda x: x[-1])
movie_rating1 = "The movie " + str(movie_rating[0][0]) + " has a rating of " + str(movie_rating[0][1]) + ".  "
movie_rating2 = "The movie " + str(movie_rating[1][0]) + ' has a rating of ' + str(movie_rating[1][1]) + '.  '
movie_rating3 = "The movie " + str(movie_rating[2][0]) + " has a rating of " + str(movie_rating[2][1]) + '.  '
movie_rating_summary = movie_rating1 + movie_rating2 + movie_rating3 + "I love all these movies, but the ratings from smallest to largest are here if you like to pick movies based on that!"
print (movie_rating_summary)

# Data Processing Method #3: Mapping

def return_character_count(x):
	return (x[0], len(x[1]))

character_count = map(return_character_count, movie_tweets)
# print (character_count)


over_140_characters = []
for x in character_count:
	if x[1] > 140:
		over_140_characters.append(x)
character_count_summary = "The following movies had tweets with over 140 characters: " + str(over_140_characters[0]) + " and " + str(over_140_characters[1]) + ".  Clearly these users are passionate about their movies! "
print (character_count_summary)

# Data Processing Method #4: List Comprehension 
twitter_handles = [x[0] for x in tweets_d]

twitter_handle_summary = "The following users who tweeted about my favorite moves have more than 10000 followers on twitter: " + str(twitter_handles) + "."
print (twitter_handle_summary)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Textfile Output From Data Processing Techniques ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Adding the findings from the data processing to textfile 

Textfile = 'finalproject.txt'
_file = open(Textfile, 'w')
_file.write("Michael's Summary of Twitter For His Favorite Moves (4/25/17): \n\n\n")
_file.write(retweet_summary + "\n\n")
_file.write(movie_rating_summary + "\n\n")
_file.write(character_count_summary + "\n\n")
_file.write(twitter_handle_summary + "\n\n")
_file.close()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST CASES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The following code below is written for the purpose of testing to make sure that the program is running correctly.  

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

	def test_movie_data(self):
		self.assertEqual(type(movie_tuple_list), list)

	def test_tweets(self):
		self.assertEqual(type(movie1tweets), list)

	def test_getting_twitter_user_info(self):
		self.assertEqual(type(movie1users), list)

	def test_getting_twitter_user_mentions(self):
		self.assertEqual(type(movie1usermentions), list)

	def test_return_character_count(self):
		self.assertEqual(type(character_count), map)

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

class DBTests(unittest.TestCase):
	def test_1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[0]), 5)
		conn.close()

	def test_2(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT movie_ID FROM Movies');
		result = cur.fetchall()
		self.assertEqual(len(result[1][0]), 9)

	def test_3(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertEqual(len(result[0]), 6)	

# ## Remember to invoke all your tests...
if __name__ == "__main__":
    unittest.main(verbosity=2)




