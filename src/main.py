import webapp2
import heatmap
import root

import os
from django.template import Template, Context, loader
from django.conf import settings


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) 
TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, "views").replace('\\','/')

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
    TEMPLATE_DIRS = (TEMPLATE_ROOT,)) #the comma is important, damn it

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler='root.RootHandler', name='root'),
    webapp2.Route(r'/<location>/heatmap', handler='heatmap.HeatmapHandler' , name='heatmap'),
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()