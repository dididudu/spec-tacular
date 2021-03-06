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

from models import Acronym
from models import Actor
from models import Package
from models import Project
from models import UseCase

from forms import AcronymForm
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

class AddActorToUseCase(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start actor adding to use case request')

    actor = None
    try:
      id = int(self.request.get('a'))
      actor = Actor.get(db.Key.from_path('Actor', id))
    except:
      actor = None

    if actor:
      usecase = None
      try:
        id = int(self.request.get('id'))
        usecase = UseCase.get(db.Key.from_path('UseCase', id))
      except:
        usecase = None

      if usecase:
        if actor.key() not in usecase.actors:
          usecase.actors.append(actor.key())
          usecase.put()
          logging.info('Finish actor adding')
        else:
          usecase.actors.remove(actor.key())
          usecase.put()
          logging.info('Actor already added')
      else:
        logging.info('Use case not found so no actor adding')
    else:
      logging.info('Actor not found so no actor adding')

    self.redirect('/usecase/%s' % id)

class AddAcronym(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start acronym adding request')

    i = self.request.get('id')
    n = self.request.get('name')
    acronym = Acronym(name=n,description='')

    try:
      id = int(i)
      project = Project.get(db.Key.from_path('Project', id))
      acronym.project = project
    except:
      logging.error('There was an error retreiving project from the datastore')

    user = users.GetCurrentUser()
    if user:
      logging.info('Acronym %s added by user %s' % (n, user.nickname()))
      acronym.created_by = user
      acronym.updated_by = user
    else:
      logging.info('Acronym %s added by anonymous user' % n)

    try:
      acronym.put()
    except:
      logging.error('There was an error adding acronym %s' % n)

    logging.debug('Finish acronym adding')
    self.redirect('/project/%s' % i)

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

class AddUseCase(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start use case adding request')

    i = self.request.get('id')
    n = self.request.get('name')
    usecase = UseCase(name=n,description='')

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

class ViewAcronym(BaseRequestHandler):
  def get(self, arg):
    title = 'Acronyme introuvable'
    acronym = None
    # Get and displays the acronym informations
    try:
      id = int(arg)
      acronym = Acronym.get(db.Key.from_path('Acronym', id))
    except:
      acronym = None
      logging.error('There was an error retreiving acronym and its informations from the datastore')

    if not acronym:
      self.error(403)
      return
    else:
      title = acronym.name

    template_values = {
      'title': title,
      'acronym': acronym
      }

    self.generate('acronym.html', template_values)

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

class ViewUseCase(BaseRequestHandler):
  def get(self, arg):
    title = 'Use case introuvable'
    usecase = None
    # Get and displays the use case informations
    try:
      id = int(arg)
      usecase = UseCase.get(db.Key.from_path('UseCase', id))
    except:
      usecase = None
      logging.error('There was an error retreiving use case and its informations from the datastore')

    if not usecase:
      self.error(403)
      return
    else:
      title = usecase.name

    template_values = {
      'title': title,
      'usecase': usecase
      }

    self.generate('usecase.html', template_values)

class EditAcronym(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition d'acronyme",
      'action': "/editAcronym",
      'id': id,
      'form': form
    }
    self.generate('editAcronym.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Acronym.get(db.Key.from_path('Acronym', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, AcronymForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Acronym.get(db.Key.from_path('Acronym', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = AcronymForm(self.request.POST, obj)
    if form.validate():
      logging.info('Acronym %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating Acronym %s' % self.request.get('name'))
      self.redirect('/acronym/%s' % id)
    else:
      self.go(id, form)

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

class EditUseCase(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de use case",
      'action': "/editUseCase",
      'id': id,
      'form': form
    }
    self.generate('editUsecase.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = UseCase.get(db.Key.from_path('UseCase', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, UseCaseForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = UseCase.get(db.Key.from_path('UseCase', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = UseCaseForm(self.request.POST, obj)
    if form.validate():
      logging.info('Use case %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating Use case %s' % self.request.get('name'))
      self.redirect('/usecase/%s' % id)
    else:
      self.go(id, form)

