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

from forms import ActorForm
from forms import ProjectForm
from forms import UseCaseForm

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

class AddProject(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start project adding request')

    n = self.request.get('name')
    project = Project(name=n,description='')

    user = users.GetCurrentUser()
    if user:
      logging.info('Project %s added by user %s' % (n, user.nickname()))
      project.created_by = user
      project.updated_by = user
    else:
      logging.info('Project %s added by anonymous user' % n)

    try:
      project.put()
    except:
      logging.error('There was an error adding projet %s' % n)

    logging.debug('Finish project adding')
    self.redirect('/projects')

class ListProjects(BaseRequestHandler):
  def get(self):
    projects = []
    title = 'Projets'
    try:
      projects = Project.gql("ORDER BY name")
      title = 'Projets'
    except:
      logging.error('There was an error retreiving projects from the datastore')

    template_values = {
      'title': title,
      'projects': projects,
      }

    self.generate('projects.html', template_values)

class ViewProject(BaseRequestHandler):
  def get(self, arg):
    title = 'Projet introuvable'
    project = None
    # Get and displays the project informations
    try:
      id = int(arg)
      project = Project.get(db.Key.from_path('Project', id))
    except:
      project = None
      logging.error('There was an error retreiving project and its informations from the datastore')

    if not project:
      self.error(403)
      return
    else:
      title = project.name

    template_values = {
      'title': title,
      'project': project
      }

    self.generate('project.html', template_values)

class EditProject(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de projet",
      'action': "/editProject",
      'id': id,
      'form': form
    }
    self.generate('editProject.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Project.get(db.Key.from_path('Project', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, ProjectForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Project.get(db.Key.from_path('Project', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = ProjectForm(self.request.POST, obj)
    if form.validate():
      logging.info('Project %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating Project %s' % self.request.get('name'))
      self.redirect('/project/%s' % id)
    else:
      self.go(id, form)

