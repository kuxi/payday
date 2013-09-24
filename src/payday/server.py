import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop

import settings
import api
from handlers import MainHandler


tornado.options.define('port', type=int, default=settings.port)


def serve():
    tornado_app = tornado.web.Application([
        (r'/', MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler,
            {'path': settings.static_path}),
    ] + api.GetRegisteredResources())
    from models import WorkHours
    from datetime import date
    wh = WorkHours()
    wh.date = date.today()
    wh.hours = 5
    wh.save()
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    serve()
