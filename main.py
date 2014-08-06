#!/usr/bin/env python
#
# SPEC-TACULAR PROJECT
#

__author__ = 'Didier Dulac'

import webapp2

from actions import BaseRequestHandler
from actions import AddProjet
from actions import ListProjets
from actions import ViewProjet

class MainPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('index.html', template_values)


application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/addProjet', AddProjet),
  ('/projet/([-\w]+)', ViewProjet),
  ('/projets', ListProjets),
], debug=True)
