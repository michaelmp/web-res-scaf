import json
from twisted.web import resource

import log
import headers
import options

"""
A recursive, dynamically-defined HTTP resource.
"""
class DynamicResource(resource.Resource):
  def __init__(self, name="", parent=None):
    resource.Resource.__init__(self)
    self.name = name
    self.children = {}
    self.parent = parent
    self.data = {}
    log.create(self)

  """
  Define a new child resource when the method is POST.
  Return 404 if the resource does not exist and the method is not OPTIONS.
  """
  def getChild(self, name, request):
    if name == "":
      return self
    if request.method in ("OPTIONS"):
      return options.DynamicOptions()
    if request.method in ("POST") and name not in self.children:
      self.children[name] = DynamicResource(name, self)
    if name in self.children:
      return self.children[name]
    print("no child resource {%s}" % name)
    return resource.NoResource() 

  """
  Full URI for this resource.
  """
  def getPath(self):
    if self.parent:
      return "%s%s/" % (self.parent.getPath(), self.name)
    return "%s/" % (self.name)

  """
  Read stuff.
  """
  def render_GET(self, request):
    headers.setContentHeaders(request)
    headers.setAccessControlHeaders(request)
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
    headers.setAccessControlHeaders(request)
    try:
      self.data = json.loads(request.content.read())
      request.setResponseCode(200)
      log.write(self)
    except ValueError:
      request.setResponseCode(400)
      log.oops(self)
    return "" 
