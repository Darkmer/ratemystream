""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import webapp2, logging
import webapp2_extras.appengine.auth.models as auth_models
from webapp2_extras import auth, sessions, security
from google.appengine.ext import ndb

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Function Decorators
def login_required(handler):
    def check_login(self, *args, **kwargs):     
        if self.user: return handler(self, *args, **kwargs)
        elif not self.user: webapp2.abort(403)
        else: webapp2.abort(500) # Raise a Server Error
    return check_login

# Admin Handler
def admin_required(handler):
    def check_admin(self, *args, **kwargs):
        user = self.user_model[0]
        if user['Type'] == "Administrator": 
            return handler(self, *args, **kwargs)
        else: webapp2.abort(403) # Raise Error
    return check_admin

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Webapp2 User Model
class User(auth_models.User):

    # Don't Need This Just Yet ...
    def set_password(self, raw_password):
        self.password = webapp2_extras.security.generate_password_hash(
            raw_password, length=32)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class UserAwareHandler(webapp2.RequestHandler):

    # Modify the Dispatch to Include Current Session
    def dispatch(self):
        try: super(UserAwareHandler, self).dispatch()
        finally: self.session_store.save_sessions(self.response)

    # Set the Desired Session Backend
    @webapp2.cached_property
    def session(self): return self.session_store.get_session(
            backend="datastore") # Datastore|Memcache|Cookie

    # Webapp2 Stipulated (Required) Session/User Functions
    @webapp2.cached_property
    def session_store(self): return sessions.get_store(request=self.request)
    @webapp2.cached_property
    def auth(self): return auth.get_auth(request=self.request)
    @webapp2.cached_property
    def user(self): return self.auth.get_user_by_session()

    # Retrieve User Data for Templates
    @webapp2.cached_property
    def user_model(self):
        return self.auth.store.user_model.get_by_auth_token(
            self.user['user_id'], 
            self.user['token']) if self.user else (None, None)
        return user_model 

    # Create a New User in the Datastore
    def register(self):

        # Retrieve Form Data from Request
        username = self.request.get('username')
        password = self.request.get('password')
        pconfirm = self.request.get('pconfirm')
        cont_url = self.request.get('continue')
        email    = self.request.get('email')
        delay    = 5  # Time Before Redirect
        uu_data  = False, list() # User Data
        
        # Confirm Matching Passwords
        if password == pconfirm:

            # Create New, Unique User Object in Datastore
            unique_properties = ['email', 'username']
            uu_data = self.auth.store.user_model.create_user(
                auth_id=username.lower(), password_raw=password,
                unique_properties=unique_properties,
                username=username, email=email.lower(), type="User")

        # Render the Response (MAY REDIRECT THE USER)
        self.render_response(
            template="auth/registration-confirm.html",
            user_data=uu_data, delay=delay)

    # Login Existing Users
    def login(self):

        # Retrieve Form Data from Request
        username = self.request.get('username')
        password = self.request.get('password')
        cont_url = self.request.get('continue')
        remember = self.request.get('remember')

        # Validate User Credentials
        try : self.auth.get_user_by_password(
                 auth_id=username.lower(),
                password=password,
                remember=bool(remember))
        except (auth.InvalidPasswordError, 
                auth.InvalidAuthIdError):
                return webapp2.abort(401)
        return self.redirect(cont_url)

    # Destroy Existing Session
    @login_required
    def logout(self):

        # Unset User Session in Cookie
        cont_url = self.request.params['continue']
        self.auth.unset_session()
        self.redirect(cont_url)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
