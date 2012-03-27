import webapp2
import heatmap
import root

import os
from django.template import Template, Context, loader
from django.conf import settings

from paste.urlparser import StaticURLParser
from paste.cascade import Cascade
from paste import httpserver

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) 
TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, "views").replace('\\','/')

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
    TEMPLATE_DIRS = (TEMPLATE_ROOT,)) #the comma is important, damn it


web_app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler='root.RootHandler', name='root'),
    webapp2.Route(r'/<place>/heatmap/<type>', handler='heatmap.HeatmapHandler' , name='heatmap'),
], debug=True)

# serving static files in webapp2: http://stackoverflow.com/questions/8470733/how-can-i-handle-static-files-with-python-webapp2-in-heroku
# Create an app to serve static files
# Choose a directory separate from your source (e.g., "static/") so it isn't dl'able
static_app = StaticURLParser("static/")

# Create a cascade that looks for static files first, then tries the webapp
app = Cascade([static_app, web_app])



def main():
    from paste import httpserver
    httpserver.serve(app, host='192.168.1.87', port='1234')

if __name__ == '__main__':
    main()
