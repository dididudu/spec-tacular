#!/usr/bin/env python
#
# SPEC-TACULAR PROJECT
#

__author__ = 'Didier Dulac'

import datetime
import logging
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from models import Actor
from models import Project
from models import UseCase

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class BaseRequestHandler(webapp2.RequestHandler):
  def generate(self, template_name, template_values={}):
    values = {
      'request': self.request,
      'user': users.GetCurrentUser(),
      'admin': users.IsCurrentUserAdmin(),
      'login_url': users.CreateLoginURL(self.request.uri),
      'logout_url': users.CreateLogoutURL('http://' + self.request.host + '/'),
      'debug': self.request.get('deb'),
      'application_name': 'Spec-Tacular'
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

class AddProjet(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start projet adding request')

    n = self.request.get('nom')
    projet = Projet(nom=n,description='')

    user = users.GetCurrentUser()
    if user:
      logging.info('Projet %s added by user %s' % (n, user.nickname()))
      projet.created_by = user
      projet.updated_by = user
    else:
      logging.info('Projet %s added by anonymous user' % n)

    try:
      projet.put()
    except:
      logging.error('There was an error adding projet %s' % n)

    logging.debug('Finish projet adding')
    self.redirect('/projets')

class ListProjets(BaseRequestHandler):
  def get(self):
    projets = []
    title = 'Projets'
    try:
      projets = Projet.gql("ORDER BY nom")
      title = 'Projets'
    except:
      logging.error('There was an error retreiving projets from the datastore')

    template_values = {
      'title': title,
      'projets': projets,
      }

    self.generate('projets.html', template_values)

class ViewProjet(BaseRequestHandler):
  def get(self, arg):
    title = 'Projet introuvable'
    projet = None
    # Get and displays the projet informations
    try:
      id = int(arg)
      projet = Projet.get(db.Key.from_path('Projet', id))
    except:
      projet = None
      logging.error('There was an error retreiving projet and its informations from the datastore')

    if not projet:
      self.error(403)
      return
    else:
      title = projet.nom

    template_values = {
      'title': title,
      'projet': projet
      }

    self.generate('projet.html', template_values)
