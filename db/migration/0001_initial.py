# -*- coding: utf-8 -*-
# Generated by Pony ORM 0.8-dev on 2020-10-19 17:30
from __future__ import unicode_literals

import datetime
from pony import orm
import pony.orm.ormtypes

dependencies = []

def define_entities(db):
    class Admin(db.Entity):
        login = orm.Required(str, unique=True)
        name = orm.Optional(str)
        hash = orm.Required(str, unique=True)

    class Settings(db.Entity):
        key = orm.PrimaryKey(str, auto=True)
        value = orm.Required(pony.orm.ormtypes.Json)

    class Post(db.Entity):
        title = orm.Required(str)
        link = orm.Optional(str)
        description = orm.Optional(str)
        category = orm.Optional('Category')
        date = orm.Required(datetime.date)
        hidden = orm.Optional(bool)
        content = orm.Required(str)

    class News(db.Post):
        image = orm.Optional(str)

    class Category(db.Entity):
        name = orm.Required(str)
        link = orm.Optional(str)
        block = orm.Optional('Block')
        hidden = orm.Optional(bool)
        posts = orm.Set(db.Post, cascade_delete=True)

    class Block(db.Entity):
        name = orm.Required(str)
        link = orm.Optional(str)
        categories = orm.Set(db.Category, cascade_delete=True)

    class Header(db.Entity):
        name = orm.Required(str)
        url = orm.Optional(str)
