def setAccessControlHeaders(request):
  request.setHeader("Access-Control-Allow-Headers", "Content-Type")
  request.setHeader("Access-Control-Allow-Origin", "*")
  request.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
  request.setHeader("Access-Control-Max-Age", "3600")

def setContentHeaders(request):
  request.setHeader("Content-Type", "application/json")
