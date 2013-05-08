""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Skyhook Dependencies
import webapp2, markupsafe, accounts
from webapp2_extras import jinja2

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Default Request Handler
class BaseHandler(accounts.UserAwareHandler):

    # Cache a Jinja Renderer Instance in the App Registry
    @webapp2.cached_property
    def jinja2(self): return jinja2.get_jinja2(app=self.app)

    # Render a Template and Output the Response
    def render_response(self, template, **context):
        context['continue_url'] = self.request.path_qs
        context['Stylesheet'] = template[:-5] + ".css"
        context['Javascript'] = template[:-5] + ".js"
        context['User'] = self.user_model[0]
        self.response.write( # Render Template and Output
        self.jinja2.render_template(template, **context))

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Default Secure Handler -- Requires Existing User Session
class SecureHandler(BaseHandler):

    # Authentication Override Failsafe
    @accounts.login_required
    def render_response(self, template, **context): 
        super(SecureHandler, self).render_response(template, **context)

    # Render the Secure Landing Page
    @accounts.login_required
    def get(self): self.render_response(
              template="views/secure.html",
             PageTitle="Secure Landing")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Default Admin-Restricted Handler -- Requires Existing Admin Session






""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##############################################################################
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main Application Routing Handler
class MainHandler(BaseHandler):

    # Render the Index Page
    def get(self): self.render_response(
              template="views/index.html",
             PageTitle="Index")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# User Account Handler (Registration|Login|Logout)
class AccountHandler(BaseHandler):

    # Display the Account Registration Form
    def get(self): self.render_response(
              template="auth/registration.html", 
             PageTitle="Register")

    # Create User Account from Form Data
    def post(self): self.register()

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        