""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Skyhook Dependencies
import webapp2, markupsafe, accounts
from webapp2_extras import jinja2

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Default Request Handler
class BaseHandler(accounts.UserHandler):

    # Cache a Jinja Renderer Instance in the App Registry
    @webapp2.cached_property
    def jinja2(self): return jinja2.get_jinja2(app=self.app)

    # Render a Template and Output the Response
    def render_response(self, template, **context):
        self.response.write(
        self.jinja2.render_template(template, **context))

    # Fallback GET Response
    def get(self): self.render_response(
        "template.html", PageTitle="Template")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main Application Routing Handler
class MainHandler(BaseHandler):
    def root(self):
        context = { 'PageTitle' : "Index",
                   'Stylesheet' : "index.css",
                  'TemplateVar' : "Lorem Ipsum" }
        self.render_response("index.html", **context)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""