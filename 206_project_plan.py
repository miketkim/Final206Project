## Your name: Michael Kim	
## The option you've chosen: Option 2 

# Put import statements you expect to need here!
import re 
import unittest 
import itertools 
import collections 
import tweepy 
import twitter_info 
import json 
import sqlite3
from pprint import pprint

# Write your test cases here.
class MovieTests(unittest.TestCase):
	def test_1(self):
		source_code = Movie(source_code_data)
		self.assertEqual(movie.title, "Source Code")
	def test_2(self):
		source_code_director = Movie(source_code_data)
		self.assertEqual(movie.director, "Duncan Jones")
	def test_3(self):
		source_code_actors = Movie(source_code_data)
		self.assertIn(movie.actors, "Jake Gyllenhaal")
	def test_4(self):
		source_code_length = Movie(source_code_data)
		self.assertEqual(source_code_length.extremely_long_movie(), "This movie is less than 2 hours.  Enjoy!")
class DBTests(unittest.TestCase):
	def test_5(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=20)
		conn.close()
	def test_6(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.excute('SELECT * FROM Tweets'); 
		result = cur.fetchall()
		self.assertEqual(len(result[0]), 6)
		conn.close()
	def test_7(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertEqual(len(result[0]), 6)	
	def test_8(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users'); 
		result = cur.fetchall()
		self.assertEqual(len(resutl[0]), 3)
## Remember to invoke all your tests...
if __name__ == "__main__":
    unittest.main(verbosity=2)