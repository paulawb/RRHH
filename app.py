from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_restful import Api, Resource
from flask_bootstrap import Bootstrap
from models import db, Aspirante, Empleador, OfertaLaboral, Postulacion
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///contratacion.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_secreta_por_defecto')
db.init_app(app)
bootstrap = Bootstrap(app)
api = Api(app)

# Crear tablas en la base de datos
with app.app_context():
    db.create_all()

# Recursos de API para Aspirantes
class AspiranteResource(Resource):
    def get(self, aspirante_id=None):
        if aspirante_id:
            aspirante = Aspirante.query.get_or_404(aspirante_id)
            return {
                'id': aspirante.id,
                'nombre': aspirante.nombre,
                'apellido': aspirante.apellido,
                'edad': aspirante.edad,
                'email': aspirante.email,
                'telefono': aspirante.telefono,
                'area_interes': aspirante.area_interes,
                'puesto_deseado': aspirante.puesto_deseado,
                'url_cv': aspirante.url_cv
            }
        else:
            aspirantes = Aspirante.query.all()
            resultado = []
            for a in aspirantes:
                resultado.append({
                    'id': a.id,
                    'nombre': a.nombre,
                    'apellido': a.apellido,
                    'email': a.email,
                    'area_interes': a.area_interes,
                    'puesto_deseado': a.puesto_deseado
                })
            return resultado

    def post(self):
        data = request.get_json()
        try:
            nuevo_aspirante = Aspirante(
                nombre=data['nombre'],
                apellido=data['apellido'],
                edad=data['edad'],
                email=data['email'],
                telefono=data['telefono'],
                area_interes=data['area_interes'],
                puesto_deseado=data['puesto_deseado'],
                url_cv=data['url_cv']
            )
            db.session.add(nuevo_aspirante)
            db.session.commit()
            return {'mensaje': 'Aspirante registrado exitosamente', 'id': nuevo_aspirante.id}, 201
        except KeyError as e:
            return {'error': f'Falta el campo {e}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def put(self, aspirante_id):
        aspirante = Aspirante.query.get_or_404(aspirante_id)
        data = request.get_json()
        try:
            if 'nombre' in data:
                aspirante.nombre = data['nombre']
            if 'apellido' in data:
                aspirante.apellido = data['apellido']
            if 'edad' in data:
                aspirante.edad = data['edad']
            if 'email' in data:
                aspirante.email = data['email']
            if 'telefono' in data:
                aspirante.telefono = data['telefono']
            if 'area_interes' in data:
                aspirante.area_interes = data['area_interes']
            if 'puesto_deseado' in data:
                aspirante.puesto_deseado = data['puesto_deseado']
            if 'url_cv' in data:
                aspirante.url_cv = data['url_cv']

            db.session.commit()
            return {'mensaje': 'Aspirante actualizado exitosamente'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, aspirante_id):
        aspirante = Aspirante.query.get_or_404(aspirante_id)
        try:
            db.session.delete(aspirante)
            db.session.commit()
            return {'mensaje': 'Aspirante eliminado exitosamente'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

# Recursos de API para Empleadores
class EmpleadorResource(Resource):
    def get(self, empleador_id=None):
        if empleador_id:
            empleador = Empleador.query.get_or_404(empleador_id)
            return {
                'id': empleador.id,
                'nombre_empresa': empleador.nombre_empresa,
                'sector': empleador.sector,
                'email_contacto': empleador.email_contacto,
                'telefono_contacto': empleador.telefono_contacto
            }
        else:
            empleadores = Empleador.query.all()
            resultado = []
            for e in empleadores:
                resultado.append({
                    'id': e.id,
                    'nombre_empresa': e.nombre_empresa,
                    'sector': e.sector,
                    'email_contacto': e.email_contacto
                })
            return resultado

    def post(self):
        data = request.get_json()
        try:
            nuevo_empleador = Empleador(
                nombre_empresa=data['nombre_empresa'],
                sector=data['sector'],
                email_contacto=data['email_contacto'],
                telefono_contacto=data['telefono_contacto']
            )
            db.session.add(nuevo_empleador)
            db.session.commit()
            return {'mensaje': 'Empleador registrado exitosamente', 'id': nuevo_empleador.id}, 201
        except KeyError as e:
            return {'error': f'Falta el campo {e}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def put(self, empleador_id):
        empleador = Empleador.query.get_or_404(empleador_id)
        data = request.get_json()
        try:
            if 'nombre_empresa' in data:
                empleador.nombre_empresa = data['nombre_empresa']
            if 'sector' in data:
                empleador.sector = data['sector']
            if 'email_contacto' in data:
                empleador.email_contacto = data['email_contacto']
            if 'telefono_contacto' in data:
                empleador.telefono_contacto = data['telefono_contacto']

            db.session.commit()
            return {'mensaje': 'Empleador actualizado exitosamente'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, empleador_id):
        empleador = Empleador.query.get_or_404(empleador_id)
        try:
            db.session.delete(empleador)
            db.session.commit()
            return {'mensaje': 'Empleador eliminado exitosamente'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

# Recursos de API para Ofertas Laborales
class OfertaLaboralResource(Resource):
    def get(self, oferta_id=None):
        if oferta_id:
            oferta = OfertaLaboral.query.get_or_404(oferta_id)
            return {
                'id': oferta.id,
                'titulo': oferta.titulo,
                'descripcion': oferta.descripcion,
                'requisitos': oferta.requisitos,
                'salario': oferta.salario,
                'ubicacion': oferta.ubicacion,
                'area': oferta.area,
                'empleador_id': oferta.empleador_id,
                'fecha_publicacion': oferta.fecha_publicacion.isoformat()
            }
        else:
            ofertas = OfertaLaboral.query.all()
            resultado = []
            for o in ofertas:
                resultado.append({
                    'id': o.id,
                    'titulo': o.titulo,
                    'ubicacion': o.ubicacion,
                    'area': o.area,
                    'salario': o.salario,
                    'empleador_id': o.empleador_id
                })
            return resultado

    def post(self):
        data = request.get_json()
        try:
            nueva_oferta = OfertaLaboral(
                titulo=data['titulo'],
                descripcion=data['descripcion'],
                requisitos=data['requisitos'],
                salario=data.get('salario'),
                ubicacion=data['ubicacion'],
                area=data['area'],
                empleador_id=data['empleador_id']
            )
            db.session.add(nueva_oferta)
            db.session.commit()
            return {'mensaje': 'Oferta laboral publicada exitosamente', 'id': nueva_oferta.id}, 201
        except KeyError as e:
            return {'error': f'Falta el campo {e}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def put(self, oferta_id):
        oferta = OfertaLaboral.query.get_or_404(oferta_id)
        data = request.get_json()
        try:
            if 'titulo' in data:
                oferta.titulo = data['titulo']
            if 'descripcion' in data:
                oferta.descripcion = data['descripcion']
            if 'requisitos' in data:
                oferta.requisitos = data['requisitos']
            if 'salario' in data:
                oferta.salario = data['salario']
            if 'ubicacion' in data:
                oferta.ubicacion = data['ubicacion']
            if 'area' in data:
                oferta.area = data['area']

            db.session.commit()
            return {'mensaje': 'Oferta laboral actualizada exitosamente'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, oferta_id):
        oferta = OfertaLaboral.query.get_or_404(oferta_id)
        try:
            db.session.delete(oferta)
            db.session.commit()
            return {'mensaje': 'Oferta laboral eliminada exitosamente'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

# Recursos de API para Postulaciones
class PostulacionResource(Resource):
    def get(self, postulacion_id=None):
        if postulacion_id:
            postulacion = Postulacion.query.get_or_404(postulacion_id)
            return {
                'id': postulacion.id,
                'aspirante_id': postulacion.aspirante_id,
                'oferta_id': postulacion.oferta_id,
                'estado': postulacion.estado,
                'fecha_postulacion': postulacion.fecha_postulacion.isoformat()
            }
        else:
            postulaciones = Postulacion.query.all()
            resultado = []
            for p in postulaciones:
                resultado.append({
                    'id': p.id,
                    'aspirante_id': p.aspirante_id,
                    'oferta_id': p.oferta_id,
                    'estado': p.estado,
                    'fecha_postulacion': p.fecha_postulacion.isoformat()
                })
            return resultado

    def post(self):
        data = request.get_json()
        try:
            nueva_postulacion = Postulacion(
                aspirante_id=data['aspirante_id'],
                oferta_id=data['oferta_id']
            )
            db.session.add(nueva_postulacion)
            db.session.commit()
            return {'mensaje': 'Postulación registrada exitosamente', 'id': nueva_postulacion.id}, 201
        except KeyError as e:
            return {'error': f'Falta el campo {e}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def put(self, postulacion_id):
        postulacion = Postulacion.query.get_or_404(postulacion_id)
        data = request.get_json()
        try:
            if 'estado' in data:
                postulacion.estado = data['estado']

            db.session.commit()
            return {'mensaje': 'Estado de postulación actualizado exitosamente'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, postulacion_id):
        postulacion = Postulacion.query.get_or_404(postulacion_id)
        try:
            db.session.delete(postulacion)
            db.session.commit()
            return {'mensaje': 'Postulación eliminada exitosamente'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

# Rutas para los recursos
api.add_resource(AspiranteResource, '/api/aspirantes', '/api/aspirantes/<int:aspirante_id>')
api.add_resource(EmpleadorResource, '/api/empleadores', '/api/empleadores/<int:empleador_id>')
api.add_resource(OfertaLaboralResource, '/api/ofertas', '/api/ofertas/<int:oferta_id>')
api.add_resource(PostulacionResource, '/api/postulaciones', '/api/postulaciones/<int:postulacion_id>')
