import globall
import countup
import c01
import cricket
import os
import time
from tornado import web, ioloop, websocket
from tornado.options import define, options

define("ip", default="localhost")
define("port", default=8888)

class ChatManager(object):
    users = []
    @classmethod
    def add_user(cls, websocket):
        cls.users.append(websocket)

    @classmethod
    def remove_user(cls, websocket):
        cls.users.remove(websocket)

class Chat(web.RequestHandler):
    def get(self):
        self.render("main.html")

class Socket(websocket.WebSocketHandler):
    def open(self):
        print ' [V] connected.'
        ChatManager.add_user(self)
        countup.Client_append(self)
        c01.Client_append(self)
        cricket.Client_append(self)
    def on_close(self):
        print ' [x] disconnected.'
        ChatManager.remove_user(self)

    def on_message(self, message):
        print ' [o] send message.'
        # for user in ChatManager.users:
            # user.write_message(message)
        # print message
        splitString(message)
        # globall.amount = message
        # countup.main()

def splitString(string):
    print string
    splits = string.split()
    print splits
    if(splits[1]=="countup"):
        print "countup"
        globall.amount = str(splits[0])
        print splits
        countup.main()
    elif(splits[1]=="cricket"):
        print "cricket"
        cricket.main(splits[0])
    elif(splits[1]=="301"or"501"or"701"):
        print "c01"
        c01.main(splits[0],splits[1],splits[2])
    else:
        print "error "+str(splits)

settings = dict(
    debug=True,
    autoreload=True,
    compiled_template_cache=False,
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    static_url_prefix="/static/"
)

class Application(web.Application):
    def __init__(self):
        handlers = [
            (r"/", Chat),
            (r"/socket", Socket)
        ]
        web.Application.__init__(self, handlers, **settings)
        print "Server Success"


def main():
    options.parse_command_line()
    app = Application()
    app.listen(8888)
    ioloop.IOLoop.current().start()



if __name__ == "__main__":
    main()
