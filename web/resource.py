from twisted.web import resource

import json

"""
404 - No such resource.
"""
class NullResource(resource.Resource):
  def render(self, request):
    request.setResponseCode(404)
    return ""

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
    if name in self.children:
      return self.children[name]
    return NullResource() 
      
  """
  Full URI for this resource.
  """
  def getPath(self):
    if self.parent:
      return "%s/%s" % (self.parent.getPath(), self.name)
    return self.name

  def render_GET(self, request):
    return json.dumps(self.data)

  def render_POST(self, request):
    try:
      self.data = json.loads(request.content.read())
      request.setResponseCode(200)
    except ValueError:
      request.setResponseCode(400)
    return ""
