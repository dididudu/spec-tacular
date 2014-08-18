#!/usr/bin/env python
#
# SPEC-TACULAR PROJECT
#

__author__ = 'Didier Dulac'

import datetime
import logging

from google.appengine.ext import db

class Objet(db.Model):
  created_by = db.UserProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  updated_by = db.UserProperty()
  updated = db.DateTimeProperty(auto_now=True)

class Project(Objet):
  name = db.StringProperty()
  description = db.TextProperty()
  intro_actors = db.TextProperty()
  intro_packages = db.TextProperty()
  def get_packages(self):
    """Return the packages for this project."""
    packages = Package.gql("WHERE project = :1 ORDER BY order", self.key())
    return packages
  def __str__(self):
    return self.name

class Package(Objet):
  project = db.ReferenceProperty(Project, collection_name='packages')
  name = db.StringProperty()
  order = db.IntegerProperty()
  description = db.TextProperty()
  def get_usecases(self):
    """Return the usecases for this package."""
    usecases = UseCase.gql("WHERE package = :1 ORDER BY order", self.key())
    return usecases
  def __str__(self):
    return self.name

class Actor(Objet):
  project = db.ReferenceProperty(Project, collection_name='actors')
  name = db.StringProperty()
  type = db.StringProperty()
  description = db.TextProperty()
  def usecases(self):
    return UseCase.gql("WHERE actors = :1", self.key())
  def __str__(self):
    return self.name

class UseCase(Objet):
  package = db.ReferenceProperty(Package, collection_name='usecases')
  name = db.StringProperty()
  order = db.IntegerProperty()
  description = db.TextProperty()
  actors = db.ListProperty(db.Key)

  def my_actors(self):
    return Actor.get(self.actors)

  def __str__(self):
    return self.name


