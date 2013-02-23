from google.appengine.ext import ndb


class Streamers(ndb.Model):
	streamer = ndb.StringProperty(required=True) #Name of Streamer. Each streamer will only appear once in the db
	avgRating = ndb.FloatProperty() #Their average rating based on our criteria
	
	"""	This line will be repeated for each other rating field we like to go with
	Categories such as teaching, entertainment, and interaction with the viewer
	can be here, leaving it this as a placeholder for now
	XXXrating = ndb.FloatProperty()"""
	
	isLive = ndb.BooleanProperty() #Will say whether this stream is currently live
	location = ndb.StringPropety() #Will list general location such as NY, USA etc.
	timeZone = ndb.StringProperty() #Will be writtem as +/-#GMT


class Users(ndb.Model):
	name = ndb.StringProperty(required="true")
	email = ndb.EmailProperty(required="true")
	avatar = ndb.BlobProperty()
	dateJoined = ndb.DateProperty(required="true")
	numReviews = ndb.IntegerProperty(required="true")


class Reviews(ndb.Model):
	streamer = ndb.ReferenceProperty(Streams) #Every review much be of someone in the Stream datastore
	user = ndb.ReferenceProperty(Users) #Username of the person that wrote the review
	overallRating = ndb.IntegerProperty() #Overal rating value assigned
	
	"""	This line will be repeated for each other rating field we go with.
	Categories such as teaching, entertainment, and interaction with the viewer
	can be here, leaving it this as a placeholder for now
	XXXrating = ndb.IntegerProperty()"""
	
	reviewText = ndb.StringProperty() #500 character review of the stream by the user


class PasswordHashes(ndb.Model):
	user = ndb.ReferenceProperty(Users)
	salt = ndb.IntegerProperty(required="true")
	hash = ndb.IntegerProperty(required="true")