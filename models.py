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
  def __str__(self):
    return self.name

class Actor(Objet):
  project = db.ReferenceProperty(Project, collection_name='actors')
  name = db.StringProperty()
  kind = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.name

class UseCase(Objet):
  project = db.ReferenceProperty(Project, collection_name='usecases')
  name = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.name


