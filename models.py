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
  nom = db.StringProperty()

class Actor(Objet):
  nom = db.StringProperty()

class UseCase(Objet):
  nom = db.StringProperty()


