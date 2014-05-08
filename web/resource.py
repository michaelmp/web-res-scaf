from twisted.web import resource

class DynamicResource(resource.Resource):
  def __init__(self, name="", parent=None):
    resource.Resource.__init__(self)
    self.name = name
    self.children = {}
    self.parent = parent
    self.data = None

  def getChild(self, name, request):
    if name not in self.children:
      self.children[name] = DynamicResource(name, self)
    return self.children[name]

  def getPath(self):
    if self.parent:
      return "%s/%s" % (self.parent.getPath(), self.name)
    return self.name

  def render_GET(self, request):
    return self.data

  def render_POST(self, request):
    pass
