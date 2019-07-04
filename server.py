import os

import tornado.ioloop
import tornado.web
import sys

from DFA import DFAFilter
from Fast_DFA import Fast_DFAFilter
from Pure_DFA import Pure_DFAFilter

gfw1 = Pure_DFAFilter()
gfw2 = Fast_DFAFilter()
gfw3 = DFAFilter()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        level = str(self.get_argument("level"))
        text = str(self.get_argument("text"))
        result = {}
        if level == "1":
            result = gfw1.DFA(text)
            result["state"] = "success"
        elif level == "2":
            result = gfw2.DFA(text)
            result["state"] = "success"
        elif level == "3":
            result = gfw3.DFA(text)
            result["state"] = "success"
        else:
            result["state"] = "Not Valid Level"
        result = str(result).replace("'", "\"")
        self.write(result)

def make_app():
    return tornado.web.Application([(r"/", MainHandler), ], static_path=os.path.join(os.path.dirname(__file__), 'static'))

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
    # http://192.168.5.121/?level=3&text=高价出售考生信息QQ