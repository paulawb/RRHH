from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Aspirante(db.Model):
    __tablename__ = 'aspirantes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    area_interes = db.Column(db.String(100), nullable=False)
    puesto_deseado = db.Column(db.String(100), nullable=False)
    url_cv = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, nombre, apellido, edad, email, telefono, area_interes, puesto_deseado, url_cv):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.email = email
        self.telefono = telefono
        self.area_interes = area_interes
        self.puesto_deseado = puesto_deseado
        self.url_cv = url_cv
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.email} - {self.area_interes} - {self.puesto_deseado}"

class Empleador(db.Model):
    __tablename__ = 'empleadores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    email_contacto = db.Column(db.String(100), unique=True, nullable=False)
    telefono_contacto = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    ofertas = db.relationship('OfertaLaboral', backref='empleador', lazy=True)
    
    def __init__(self, nombre_empresa, sector, email_contacto, telefono_contacto):
        self.nombre_empresa = nombre_empresa
        self.sector = sector
        self.email_contacto = email_contacto
        self.telefono_contacto = telefono_contacto
    
    def __str__(self):
        return f"{self.nombre_empresa} - {self.sector} - {self.email_contacto}"

class OfertaLaboral(db.Model):
    __tablename__ = 'ofertas_laborales'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    requisitos = db.Column(db.Text, nullable=False)
    salario = db.Column(db.Float, nullable=True)
    ubicacion = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    empleador_id = db.Column(db.Integer, db.ForeignKey('empleadores.id'), nullable=False)
    postulaciones = db.relationship('Postulacion', backref='oferta', lazy=True)
    
    def __init__(self, titulo, descripcion, requisitos, salario, ubicacion, area, empleador_id):
        self.titulo = titulo
        self.descripcion = descripcion
        self.requisitos = requisitos
        self.salario = salario
        self.ubicacion = ubicacion
        self.area = area
        self.empleador_id = empleador_id
    
    def __str__(self):
        return f"{self.titulo} - {self.ubicacion} - {self.area}"

class Postulacion(db.Model):
    __tablename__ = 'postulaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_postulacion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='Pendiente')
    
    aspirante_id = db.Column(db.Integer, db.ForeignKey('aspirantes.id'), nullable=False)
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas_laborales.id'), nullable=False)
    
    aspirante = db.relationship('Aspirante', backref=db.backref('postulaciones', lazy=True))
    
    def __init__(self, aspirante_id, oferta_id):
        self.aspirante_id = aspirante_id
        self.oferta_id = oferta_id
    
    def __str__(self):
        return f"Postulación: {self.aspirante_id} - {self.oferta_id} - {self.estado}"
