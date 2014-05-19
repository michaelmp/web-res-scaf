from twisted.web import resource

import headers

class DynamicOptions(resource.Resource):
  def getChild(self, name, request):
    return self

  """
  Get HTTP Options
  """
  def render_OPTIONS(self, request):
    headers.setContentHeaders(request)
    headers.setAccessControlHeaders(request)
    request.setResponseCode(200)
    return ""
