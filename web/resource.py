import json

from twisted.web import resource

import log

"""
A recursive dynamically-defined HTTP resource.
"""
class DynamicResource(resource.Resource):
  def __init__(self, name="", parent=None):
    resource.Resource.__init__(self)
    self.name = name
    self.children = {}
    self.parent = parent
    self.data = {}

  """
  Define a new child resource when the method is POST.
  Return 404 if the resource does not exist.
  """
  def getChild(self, name, request):
    if request.method == "POST" and name not in self.children:
      self.children[name] = DynamicResource(name, self)
      log.create(self.children[name])
    if name in self.children:
      return self.children[name]
    return resource.NoResource() 

  """
  Full URI for this resource.
  """
  def getPath(self):
    if self.parent:
      return "%s/%s" % (self.parent.getPath(), self.name)
    return "%s" % (self.name)

  """
  Indicate CORS headers for preflight requests.
  """
  def render_OPTIONS(self, request):
    request.setHeader("Access-Control-Allow-Origin", "*")
    request.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    request.setHeader("Access-Control-Max-Age", "3600")
    request.setResponseCode(200)
    return ""

  """
  Read stuff.
  """
  def render_GET(self, request):
    request.setHeader("Content-Type", "application/json")
    log.read(self)
    return json.dumps({
      "content": self.data,
      "links": map(lambda(child):{"name": child.name, "location": child.getPath()}, self.children.values()),
      "location": self.getPath(),
      "name": self.name
    })

  """
  Write stuff.
  """
  def render_POST(self, request):
    try:
      self.data = json.loads(request.content.read())
      request.setResponseCode(200)
      log.write(self)
    except ValueError:
      request.setResponseCode(400)
      log.oops(self)
    return ""
