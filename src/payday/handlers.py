import tornado.web
import os


templatepath = os.path.join(os.path.join(os.path.dirname(__file__), 'static'), 'templates')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print os.getcwd()
        template = open(os.path.join(templatepath, 'index.html'), 'r')
        self.write(template.read())
