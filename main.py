""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Extend the System Path for Simpler Imports
import os, sys, webapp2
filepath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(filepath + '/developer')

# Skyhook Dependencies
import routes
import settings
import errors

# Determine DebugMode for Production Instances
DebugMode = os.environ.get('SERVER_SOFTWARE', '')
DebugMode = DebugMode.startswith('Dev')

# Create a WSGI Application
app = webapp2.WSGIApplication(
     routes=routes.app_routes,
     config=settings.Settings,
      debug=DebugMode)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Handle Possible Client and Server Errors (400 to 600)
exceptions = errors.ErrorHandler()
for code in range(400,600):
    app.error_handlers[code] = exceptions.handle_error

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
