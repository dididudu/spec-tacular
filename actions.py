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
from models import Package
from models import Project
from models import UseCase

from forms import ActorForm
from forms import PackageForm
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

class AddActor(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start actor adding request')

    i = self.request.get('id')
    n = self.request.get('name')
    actor = Actor(name=n,description='')

    try:
      id = int(i)
      project = Project.get(db.Key.from_path('Project', id))
      actor.project = project
    except:
      logging.error('There was an error retreiving project from the datastore')

    user = users.GetCurrentUser()
    if user:
      logging.info('Actor %s added by user %s' % (n, user.nickname()))
      actor.created_by = user
      actor.updated_by = user
    else:
      logging.info('Actor %s added by anonymous user' % n)

    try:
      actor.put()
    except:
      logging.error('There was an error adding actor %s' % n)

    logging.debug('Finish actor adding')
    self.redirect('/project/%s' % i)

class AddPackage(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start package adding request')

    i = self.request.get('id')
    n = self.request.get('name')
    package = Package(name=n,description='')

    try:
      id = int(i)
      project = Project.get(db.Key.from_path('Project', id))
      package.project = project
    except:
      logging.error('There was an error retreiving project from the datastore')

    user = users.GetCurrentUser()
    if user:
      logging.info('Package %s added by user %s' % (n, user.nickname()))
      package.created_by = user
      package.updated_by = user
    else:
      logging.info('Package %s added by anonymous user' % n)

    try:
      package.put()
    except:
      logging.error('There was an error adding package %s' % n)

    logging.debug('Finish package adding')
    self.redirect('/project/%s' % i)

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

class AddUsecase(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start use case adding request')

    i = self.request.get('id')
    n = self.request.get('name')
    usecase = Usecase(name=n,description='')

    try:
      id = int(i)
      package = Package.get(db.Key.from_path('Package', id))
      usecase.package = package
    except:
      logging.error('There was an error retreiving package from the datastore')

    user = users.GetCurrentUser()
    if user:
      logging.info('Use case %s added by user %s' % (n, user.nickname()))
      usecase.created_by = user
      usecase.updated_by = user
    else:
      logging.info('Use case %s added by anonymous user' % n)

    try:
      usecase.put()
    except:
      logging.error('There was an error adding use case %s' % n)

    logging.debug('Finish use case adding')
    self.redirect('/package/%s' % i)

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

class ViewActor(BaseRequestHandler):
  def get(self, arg):
    title = 'Acteur introuvable'
    actor = None
    # Get and displays the actor informations
    try:
      id = int(arg)
      actor = Actor.get(db.Key.from_path('Actor', id))
    except:
      actor = None
      logging.error('There was an error retreiving actor and its informations from the datastore')

    if not actor:
      self.error(403)
      return
    else:
      title = actor.name

    template_values = {
      'title': title,
      'actor': actor
      }

    self.generate('actor.html', template_values)

class ViewPackage(BaseRequestHandler):
  def get(self, arg):
    title = 'Package introuvable'
    package = None
    # Get and displays the package informations
    try:
      id = int(arg)
      package = Package.get(db.Key.from_path('Package', id))
    except:
      package = None
      logging.error('There was an error retreiving package and its informations from the datastore')

    if not package:
      self.error(403)
      return
    else:
      title = package.name

    template_values = {
      'title': title,
      'package': package
      }

    self.generate('package.html', template_values)

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

class EditActor(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition d'acteur",
      'action': "/editActor",
      'id': id,
      'form': form
    }
    self.generate('editActor.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Actor.get(db.Key.from_path('Actor', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, ActorForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Actor.get(db.Key.from_path('Actor', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = ActorForm(self.request.POST, obj)
    if form.validate():
      logging.info('Actor %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating Actor %s' % self.request.get('name'))
      self.redirect('/actor/%s' % id)
    else:
      self.go(id, form)

class EditPackage(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de package",
      'action': "/editPackage",
      'id': id,
      'form': form
    }
    self.generate('editPackage.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Package.get(db.Key.from_path('Package', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, PackageForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Package.get(db.Key.from_path('Package', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = PackageForm(self.request.POST, obj)
    if form.validate():
      logging.info('Package %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating Package %s' % self.request.get('name'))
      self.redirect('/package/%s' % id)
    else:
      self.go(id, form)

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

