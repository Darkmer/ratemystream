""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Skyhook Application Settings
AppName = "Skyhook"
Theme = "Default"
Description = "Default Description"

PRIVATE_KEY = "SECRET_KEY"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from webapp2  import uri_for    # Enable 'uri_for()' in Templates
from accounts import User       # Define Webapp2 User Model
Theme = Theme.lower() # Lowercase Themes as Directory
Settings = dict() # Dictionary Keys Override Defaults
Settings['webapp2_extras.jinja2'] = { # Configure Templating
'globals' : { 'AppName' : AppName,
                'Theme' : Theme,
          'Description' : Description,
              'uri_for' : uri_for,
           'image_path' : "/templates/%s/img"  % Theme ,
      'stylesheet_path' : "/templates/%s/css"  % Theme ,
      'javascript_path' : "/templates/%s/js"   % Theme ,
     }, 'template_path' : "templates/%s/html/" % Theme }

Settings['webapp2_extras.auth']     = { 'user_model' : User }
Settings['webapp2_extras.sessions'] = { 'secret_key' : PRIVATE_KEY }

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""