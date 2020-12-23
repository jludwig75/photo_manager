#!/usr/bin/env python3
import cherrypy
import os
from mediaserver import MediaServer


class Root(object):
    @cherrypy.expose
    def index(self):
        with open('html/index.html') as webPage:
            return webPage.read()

if __name__ == "__main__":
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./html')
        },
        '/photos': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./photos')
        }
    }
    cherrypy.config.update({'server.socket_port': 8086})
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.tree.mount(MediaServer('photos'), '/folders', conf)
    cherrypy.quickstart(Root(), '/', conf)
