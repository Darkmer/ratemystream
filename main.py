# Modify Python System Path for Simpler Imports
import os, sys
filepath = os.path.dirname(os.path.realpath(__file__))
#sys.path.append(filepath + '/dulwich')

import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)