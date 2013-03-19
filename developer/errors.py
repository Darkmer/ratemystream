""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Skyhook Dependencies
from handlers import BaseHandler
import logging

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# List of Available Exception Responses
errors = {
    # 4xx Client Errors
    401 : ("Unauthorized"  , "Insufficient Level of Access"),
    403 : ("Forbidden"     , "Access Prohibited"),
    404 : ("Not Found"     , "The Page Could Not Be Displayed"),
    409 : ("Edit Conflict" , "Entry Already Exists"),

    # 5xx Server Errors
    500 : ("Server Error" , "Internal Server Error :: Please Try Again"),
    501 : ("Unhandled"    , "An Unhandled Exception Occurred"),
}   # Exception Code , Page Title , Description (Message)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Default Error Handler
class ErrorHandler(BaseHandler):

    # Handle Rendering and Exception Logging
    def handle_error(self, request, response, exception):
        
        # Set Instance Variables
        logging.exception(exception)
        self.exception = exception
        self.request = request
        self.response = response
        
        # Retrieve Exception Information and Render
        context = self.get_exception_info(exception)
        context['Stylesheet'] = "error.css"
        self.render_response("error.html", **context)

    # Retrieve Exception Data From Dictionary
    def get_exception_info(self, exception):
        
        # Match Exception Code to Available Key Values
        if hasattr(exception, 'code'):
            if errors.has_key(exception.code):
                error_code = exception.code
        else: error_code = 501

        # Set Template Values From Exception Response
        context = { 'ErrorCode' : error_code }
        context['PageTitle'] = errors[error_code][0]
        context['Description'] = errors[error_code][1]
        return context # Return Template Values

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""