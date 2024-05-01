from flask_login import UserMixin
import mongoengine as me
import datetime

class articulos(me.Document):
    titulo = me.StringField()
    portada = me.StringField()
    sipnosis = me.StringField()
    tipo = me.StringField()
    estado = me.StringField()
    generos = me.ListField(me.StringField())
    autor = me.StringField()
    link = me.StringField()
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

class carrusel(me.Document):
    titulo = me.StringField()
    link = me.StringField()
    ruta = me.StringField()
    createdAt = me.DateField(required=True, default=datetime.datetime.now())
    updatedAt = me.DateField(required=True, default=datetime.datetime.now())