import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop

import settings
import api
from handlers import MainHandler


tornado.options.define('port', type=int, default=settings.port)


def serve():
    handlers = [(r'/', MainHandler)]
    if hasattr(settings, 'favicon_path'):
        handlers.append((r'/(favicon.ico)', tornado.web.StaticFileHandler,
                        {'path': settings.favicon_path}))
    handlers.append((r'/static/(.*)', tornado.web.StaticFileHandler,
                    {'path': settings.static_path}))
    handlers.extend(api.GetRegisteredResources())
    tornado_app = tornado.web.Application(handlers)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    serve()
