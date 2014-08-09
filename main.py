#!/usr/bin/env python
#
# SPEC-TACULAR PROJECT
#

__author__ = 'Didier Dulac'

import webapp2

from actions import BaseRequestHandler
from actions import AddActor
from actions import AddPackage
from actions import AddProject
from actions import EditActor
from actions import EditPackage
from actions import EditProject
from actions import ListProjects
from actions import ViewActor
from actions import ViewPackage
from actions import ViewProject

class MainPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('index.html', template_values)


application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/addActor', AddActor),
  ('/editActor', EditActor),
  ('/actor/([-\w]+)', ViewActor),
  ('/addPackage', AddPackage),
  ('/editPackage', EditPackage),
  ('/package/([-\w]+)', ViewPackage),
  ('/addProject', AddProject),
  ('/editProject', EditProject),
  ('/project/([-\w]+)', ViewProject),
  ('/projects', ListProjects)
], debug=True)
