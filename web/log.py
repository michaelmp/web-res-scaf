import sys

def init(port):
  print('Running on port %i' % port)

def create(resource):
  print('%s Create' % resource.getPath())

def read(resource):
  print('%s Read' % resource.getPath())

def write(resource):
  print('%s Write' % resource.getPath())

def remove(resource):
  print('%s Remove' % resource.getPath())

def oops(resource):
  print('%s Failed' % resource.getPath())
