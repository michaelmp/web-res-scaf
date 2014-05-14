from twisted.web import server
from twisted.internet import reactor

import log
import resource

PORT = 8080

def start():
  root = resource.DynamicResource()
  reactor.listenTCP(PORT, server.Site(root))
  log.init(PORT)
  reactor.run()

if __name__ == "__main__":
  start()
