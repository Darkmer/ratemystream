""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import webapp2
import webapp2_extras.appengine.auth.models as auth_models
from webapp2_extras import auth, sessions, security
from google.appengine.ext import ndb

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class User(auth_models.User):
    # Datastore Columns
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()

    def set_password(self, raw_password):
        self.password = webapp2_extras.security.generate_password_hash(
            raw_password, length=32)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class UserHandler(webapp2.RequestHandler):

    # SessionStore Provides/Creates User Sessions
    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    # Session :: Dict-Like Object Storing Data
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session(backend="datastore")

    # Modify Request Dispatch to Save Sessions
    def dispatch(self):
        try: super(UserHandler, self).dispatch()
        finally: self.session_store.save_sessions(self.response)

    # Handle User Authentication
    @webapp2.cached_property
    def auth(self): return auth.get_auth(request=self.request)
    
    # Retrieve User Identification by Session
    @webapp2.cached_property
    def user(self): return self.auth.get_user_by_session()

    # Retrieve User Attributes from Datastore
    @webapp2.cached_property
    def user_model(self):
        user_model, timestamp = self.auth.store.user_model.get_by_auth_token(
            self.user['user_id'], 
            self.user['token']) if self.user else (None, None)
        return user_model

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""