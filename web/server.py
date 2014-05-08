from twisted.web import server
from twisted.internet import reactor

import resource

def start():
  root = resource.DynamicResource()
  reactor.listenTCP(8080, server.Site(root))
  reactor.run()

if __name__ == "__main__":
  start()
