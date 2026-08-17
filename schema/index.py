import datetime

import mongoengine as me
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class articulos(me.Document):
    titulo = me.StringField()
    portada = me.StringField()
    sipnosis = me.StringField()
    tipo = me.StringField()
    estado = me.StringField()
    generos = me.ListField(me.StringField())
    autor = me.StringField()
    link = me.StringField()
    links = me.ListField(me.DictField())
    createdAt = me.DateTimeField(required=True, default=datetime.datetime.now)
    updatedAt = me.DateTimeField(required=True, default=datetime.datetime.now)

    meta = {"indexes": [{ 
                "fields": ["$titulo", "$sipnosis"]
            }]}
    
class generos(me.Document):
    nombre = me.StringField()
    createdAt = me.DateTimeField(required=True, default=datetime.datetime.now)
    updatedAt = me.DateTimeField(required=True, default=datetime.datetime.now)
    
class users(me.Document, UserMixin):
    username = me.StringField(required=True)
    password = me.StringField(required=True)
    createdAt = me.DateTimeField(required=True, default=datetime.datetime.now)
    updatedAt = me.DateTimeField(required=True, default=datetime.datetime.now)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

class carrusel(me.Document):
    titulo = me.StringField()
    link = me.StringField()
    ruta = me.StringField()
    createdAt = me.DateTimeField(required=True, default=datetime.datetime.now)
    updatedAt = me.DateTimeField(required=True, default=datetime.datetime.now)