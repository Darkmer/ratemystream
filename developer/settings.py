""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Skyhook Application Settings
AppName = "Skyhook"
Theme = "Default"
Description = "Default Description"

PRIVATE_KEY = "Insert-Secret-Key-Here"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Theme = Theme.lower() # Lowercase Themes as Directory
Settings = dict() # Dictionary Keys Override Defaults
Settings['webapp2_extras.jinja2'] = { # Configure Templating
'globals' : { 'AppName' : AppName,
                'Theme' : Theme,
          'Description' : Description,  
      'stylesheet_path' : "/templates/%s/styles" % Theme
     }, 'template_path' : "templates/%s/layout/" % Theme }

from accounts import User # Define Webapp2 User Model
Settings['webapp2_extras.auth']     = { 'user_model' : User }
Settings['webapp2_extras.sessions'] = { 'secret_key' : PRIVATE_KEY }

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""