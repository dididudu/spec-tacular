#!/usr/bin/env python
#
# SPEC-TACULAR PROJECT
#

__author__ = 'Didier Dulac'

import webapp2

from actions import BaseRequestHandler
from actions import AddProject
from actions import ListProjects
from actions import ViewProject

class MainPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('index.html', template_values)


application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/addProject', AddProject),
  ('/editProject', EditProject),
  ('/project/([-\w]+)', ViewProject),
  ('/projects', ListProjects),
], debug=True)
