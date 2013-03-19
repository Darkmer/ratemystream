""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Skyhook Dependencies
from webapp2_extras.routes import RedirectRoute
import handlers as hdls
app_routes = [] # Routes Listing

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Skyhook Application URI Routing Table
app_route_info = [
    ( None, hdls.MainHandler, "root", "/", "root"),
    ( "GET", hdls.BaseHandler, "get", "/base/", "base"),
] # HTTP Method , Handler Class , Handler Method , URI , Name

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Iterate Through Standard Routes
for http_method, handler_class, handler_method, uri, name in app_route_info:

    # Construct a Redirect Route
    route = RedirectRoute(handler_method=handler_method,
             methods=http_method, handler=handler_class,
             name=name, template=uri, strict_slash=True)

    # Add Route to Public List
    app_routes.append(route)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""