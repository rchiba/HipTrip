import webapp2
import os
from django.template import Template, Context, loader
from django.conf import settings



class RootHandler(webapp2.RequestHandler):
    def get(self):
        template = loader.get_template( 'index.html');
        context = Context({
        })
    
        self.response.out.write(template.render(context))