#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import sys
sys.path.append("quant")
import quantPy as qp
import wIndicators as wI
import datetime
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

def colToJson(df, col):
    dictlist = []
    tuplelist = df[col].to_dict().items()
    tuplelist.sort()
    for timestamp, value in tuplelist:
        dt = timestamp.to_datetime()
        timefromepoch = int(unix_time_millis(dt))
        dictlist.append([timefromepoch, value])
    return json.dumps(dictlist)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [ 
            (r"/", MainHandler),
            (r"/stock/([a-z]+)", JsonServer),
            (r"/graph/([a-z]+)", GraphHandler),
        ]   
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )   
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("chart.html", symbol = "aapl")

class JsonServer(tornado.web.RequestHandler):
    def get(self, stock):
        result = qp.oneStock(wI.meanReversion, stock)
        self.write(colToJson(result, 'stockValue'))

class GraphHandler(tornado.web.RequestHandler):
    def get(self, symbol):
        self.render("chart.html", symbol = symbol)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
