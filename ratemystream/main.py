#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import db

import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Streamers(db.Model):
	streamer = db.StringProperty(required=True) #Name of Streamer. Each streamer will only appear once in the db
	avgRating = db.FloatProperty() #Their average rating based on our criteria
	
	"""	This line will be repeated for each other rating field we like to go with
	Categories such as teaching, entertainment, and interaction with the viewer
	can be here, leaving it this as a placeholder for now
	XXXrating = db.FloatProperty()"""
	
	isLive = db.BooleanProperty() #Will say whether this stream is currently live
	location = db.StringProperty() #Will list general location such as NY, USA etc.
	timeZone = db.StringProperty() #Will be writtem as +/-#GMT
	URL = db.StringProperty()


class Accounts(db.Model):
	name = db.StringProperty(required="true")
	email = db.EmailProperty(required="true")
	avatar = db.BlobProperty()
	dateJoined = db.DateProperty(required="true")
	numReviews = db.IntegerProperty(required="true")


class Reviews(db.Model):
	streamer = db.ReferenceProperty(Streamers) #Every review must be someone in the Stream datastore
	name = db.StringProperty()
	user = db.ReferenceProperty(Accounts) #Username of the person that wrote the review
	overallRating = db.IntegerProperty() #Overal rating value assigned
	
	"""	This line will be repeated for each other rating field we go with.
	Categories such as teaching, entertainment, and interaction with the viewer
	can be here, leaving it this as a placeholder for now
	XXXrating = db.IntegerProperty()"""
	
	reviewText = db.StringProperty() #500 character review of the stream by the user


class PasswordHashes(db.Model):
	user = db.ReferenceProperty(Accounts)
	salt = db.IntegerProperty(required="true")
	hash = db.IntegerProperty(required="true")


class MainHandler(webapp2.RequestHandler):
	def get(self):

		template_values = {}

		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))
		

class showReviewHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
          <html>
            <body>
			<div align="center"><br><br><br><br>
			""")

		streamers = db.GqlQuery("SELECT * "
								"FROM Streamers "
								"ORDER BY streamer ASC")
		
		for streamer in streamers:
			streamer_name = streamer.streamer
			self.response.out.write('<form method="post">')
			self.response.out.write('<br><br><input type="submit" name="streamerName" value="%s">' %
									streamer_name)
		self.response.out.write("""
									</input>
									</form>
									</html>
									</body>
									</div>
									""")

	def post(self):
		self.response.out.write("""
          <html>
            <body>
			<div align="center"><br><br><br><br>
			""")
		nName = self.request.get('streamerName')

		reviews = db.GqlQuery("SELECT * FROM Reviews WHERE name = :n", n=nName)
		if reviews is None:
			self.response.out.write('No reviews exist! care to <a href="../addreview"> add a review?</a>')
		for review in reviews:
			self.response.out.write('<br><br>User: admin')
			self.response.out.write('<br>Overall Rating: %s' % review.overallRating)
			self.response.out.write('<br>Review: %s' % review.reviewText)

	
class addReviewHandler(webapp2.RequestHandler):
	def get(self):
		global jinja_environment
		self.response.out.write("""
          <html>
            <body>
			<div align="center"><br><br><br><br>
			""")

		streamers = db.GqlQuery("SELECT * "
								"FROM Streamers "
								"ORDER BY streamer ASC")
		
		for streamer in streamers:
			streamer_name = streamer.streamer
			
			self.response.out.write('<form method="post">')
			self.response.out.write('<input type="submit" name="streamerName" value="%s">' %
									streamer_name)
			self.response.out.write("""
									</input>
									</a>
									</form>
									""")
									
	def post(self):
		streamer_name = self.request.get('streamerName')

		self.response.out.write("""
          <html>
            <body>
			<div align="center"><br><br><br><br>
				<form action="/streamer" method="post"> """)
		self.response.out.write('Streamer: %s' % streamer_name) 
		self.response.out.write('<input type="hidden" name="streamerName" value="%s"' % 
								streamer_name)
		self.response.out.write("""
				<br><br>Overall Rating: <input type="radio" name="rating" value=1> 1
				<input type="radio" name="rating" value=2> 2
				<input type="radio" name="rating" value=3> 3
				<input type="radio" name="rating" value=4> 4
				<input type="radio" name="rating" value=5> 5
                <br><br><div><textarea name="content" rows="3" cols="60"></textarea></div>
                <br><div><input type="submit" value="Add Review (500 characters or less)"></div>
				</form>
			</html>
        </body>
		""")
		  

		  
class streamerHandler(webapp2.RequestHandler):

	def post(self):
		name = self.request.get('streamerName')
		streamer = db.GqlQuery("SELECT * FROM Streamers WHERE streamer = :n", n=name)
		review = Reviews()
		review.streamer = streamer.get()
		review.name = streamer.get().streamer
		review.overallRating = int(self.request.get('rating'))
		review.reviewText = self.request.get('content')
		review.put()
		self.redirect('/')
		

app = webapp2.WSGIApplication([('/', MainHandler),
							 ('/addreview', addReviewHandler),
							 ('/streamer', streamerHandler),
							 ('/showreviews', showReviewHandler),], debug=True)
