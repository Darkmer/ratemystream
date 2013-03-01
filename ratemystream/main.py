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


class Accounts(db.Model):
	name = db.StringProperty(required="true")
	email = db.EmailProperty(required="true")
	avatar = db.BlobProperty()
	dateJoined = db.DateProperty(required="true")
	numReviews = db.IntegerProperty(required="true")


class Reviews(db.Model):
	streamer = db.ReferenceProperty(Streamers) #Every review much be of someone in the Stream datastore
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
		global jinja_environment
		title = "Rate My Stream"
		featured = "Featured Streamers"
		streamer1 = "OddBrah"
		streamer2 = "DanceWithWarricks"
		streamer3 = "LadyOfLuminosity"
		
		template_values = {
			'title' : title,
			'featured' : featured,
			'streamer1' : streamer1,
			'streamer2' : streamer2,
			'streamer3' : streamer3
		}
		
		
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
