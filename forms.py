#!/usr/bin/env python
#
# SPEC-TACULAR PROJECT
#

__author__ = 'Didier Dulac'

from wtforms import Form, BooleanField, DateField, FloatField, IntegerField, SelectField, TextField, TextAreaField, validators
from wtforms.ext.appengine.fields import ReferencePropertyField

from models import Actor
from models import Package
from models import Project
from models import UseCase

class ProjectForm(Form):
  name = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class PackageForm(Form):
  project = ReferencePropertyField(u'Projet', reference_class=Project)
  name = TextField(u'Nom', validators=[validators.required()])
  order = IntegerField(u'Rang', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class ActorForm(Form):
  project = ReferencePropertyField(u'Projet', reference_class=Project)
  name = TextField(u'Nom', validators=[validators.required()])
  type = TextField(u'Type', validators=[validators.optional()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class UseCaseForm(Form):
  project = ReferencePropertyField(u'Projet', reference_class=Project)
  name = TextField(u'Nom', validators=[validators.required()])
  order = IntegerField(u'Rang', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])
