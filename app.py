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


# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rutas para Aspirantes
@app.route('/aspirantes')
def aspirantes_index():
    aspirantes = Aspirante.query.all()
    return render_template('aspirantes/index.html', aspirantes=aspirantes)

@app.route('/aspirantes/<int:aspirante_id>')
def aspirante_detail(aspirante_id):
    aspirante = Aspirante.query.get_or_404(aspirante_id)
    postulaciones = Postulacion.query.filter_by(aspirante_id=aspirante_id).all()
    return render_template('aspirantes/detail.html', aspirante=aspirante, postulaciones=postulaciones)

@app.route('/aspirantes/nuevo', methods=['GET', 'POST'])
def aspirante_create():
    if request.method == 'POST':
        try:
            nuevo_aspirante = Aspirante(
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                edad=request.form['edad'],
                email=request.form['email'],
                telefono=request.form['telefono'],
                area_interes=request.form['area_interes'],
                puesto_deseado=request.form['puesto_deseado'],
                url_cv=request.form['url_cv']
            )
            db.session.add(nuevo_aspirante)
            db.session.commit()
            flash('Aspirante registrado exitosamente', 'success')
            return redirect(url_for('aspirante_detail', aspirante_id=nuevo_aspirante.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar aspirante: {str(e)}', 'danger')
    return render_template('aspirantes/form.html')

@app.route('/aspirantes/editar/<int:aspirante_id>', methods=['GET', 'POST'])
def aspirante_edit(aspirante_id):
    aspirante = Aspirante.query.get_or_404(aspirante_id)
    if request.method == 'POST':
        try:
            aspirante.nombre = request.form['nombre']
            aspirante.apellido = request.form['apellido']
            aspirante.edad = request.form['edad']
            aspirante.email = request.form['email']
            aspirante.telefono = request.form['telefono']
            aspirante.area_interes = request.form['area_interes']
            aspirante.puesto_deseado = request.form['puesto_deseado']
            aspirante.url_cv = request.form['url_cv']

            db.session.commit()
            flash('Aspirante actualizado exitosamente', 'success')
            return redirect(url_for('aspirante_detail', aspirante_id=aspirante.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar aspirante: {str(e)}', 'danger')
    return render_template('aspirantes/form.html', aspirante=aspirante)

@app.route('/aspirantes/eliminar/<int:aspirante_id>', methods=['POST'])
def aspirante_delete(aspirante_id):
    aspirante = Aspirante.query.get_or_404(aspirante_id)
    try:
        db.session.delete(aspirante)
        db.session.commit()
        flash('Aspirante eliminado exitosamente', 'success')
        return redirect(url_for('aspirantes_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar aspirante: {str(e)}', 'danger')
        return redirect(url_for('aspirante_detail', aspirante_id=aspirante_id))

# Rutas para Empleadores
@app.route('/empleadores')
def empleadores_index():
    empleadores = Empleador.query.all()
    return render_template('empleadores/index.html', empleadores=empleadores)

@app.route('/empleadores/<int:empleador_id>')
def empleador_detail(empleador_id):
    empleador = Empleador.query.get_or_404(empleador_id)
    ofertas = OfertaLaboral.query.filter_by(empleador_id=empleador_id).all()
    return render_template('empleadores/detail.html', empleador=empleador, ofertas=ofertas)

@app.route('/empleadores/nuevo', methods=['GET', 'POST'])
def empleador_create():
    if request.method == 'POST':
        try:
            nuevo_empleador = Empleador(
                nombre_empresa=request.form['nombre_empresa'],
                sector=request.form['sector'],
                email_contacto=request.form['email_contacto'],
                telefono_contacto=request.form['telefono_contacto']
            )
            db.session.add(nuevo_empleador)
            db.session.commit()
            flash('Empleador registrado exitosamente', 'success')
            return redirect(url_for('empleador_detail', empleador_id=nuevo_empleador.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar empleador: {str(e)}', 'danger')
    return render_template('empleadores/form.html')

@app.route('/empleadores/editar/<int:empleador_id>', methods=['GET', 'POST'])
def empleador_edit(empleador_id):
    empleador = Empleador.query.get_or_404(empleador_id)
    if request.method == 'POST':
        try:
            empleador.nombre_empresa = request.form['nombre_empresa']
            empleador.sector = request.form['sector']
            empleador.email_contacto = request.form['email_contacto']
            empleador.telefono_contacto = request.form['telefono_contacto']

            db.session.commit()
            flash('Empleador actualizado exitosamente', 'success')
            return redirect(url_for('empleador_detail', empleador_id=empleador.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar empleador: {str(e)}', 'danger')
    return render_template('empleadores/form.html', empleador=empleador)

@app.route('/empleadores/eliminar/<int:empleador_id>', methods=['POST'])
def empleador_delete(empleador_id):
    empleador = Empleador.query.get_or_404(empleador_id)
    try:
        db.session.delete(empleador)
        db.session.commit()
        flash('Empleador eliminado exitosamente', 'success')
        return redirect(url_for('empleadores_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar empleador: {str(e)}', 'danger')
        return redirect(url_for('empleador_detail', empleador_id=empleador_id))

# Rutas para Ofertas Laborales
@app.route('/ofertas')
def ofertas_index():
    ofertas = OfertaLaboral.query.all()
    return render_template('ofertas/index.html', ofertas=ofertas)

@app.route('/ofertas/<int:oferta_id>')
def oferta_detail(oferta_id):
    oferta = OfertaLaboral.query.get_or_404(oferta_id)
    postulaciones = Postulacion.query.filter_by(oferta_id=oferta_id).all()
    return render_template('ofertas/detail.html', oferta=oferta, postulaciones=postulaciones)

@app.route('/ofertas/nuevo', methods=['GET', 'POST'])
def oferta_create():
    empleadores = Empleador.query.all()
    if request.method == 'POST':
        try:
            nueva_oferta = OfertaLaboral(
                titulo=request.form['titulo'],
                descripcion=request.form['descripcion'],
                requisitos=request.form['requisitos'],
                salario=request.form['salario'] if request.form['salario'] else None,
                ubicacion=request.form['ubicacion'],
                area=request.form['area'],
                empleador_id=request.form['empleador_id']
            )
            db.session.add(nueva_oferta)
            db.session.commit()
            flash('Oferta laboral publicada exitosamente', 'success')
            return redirect(url_for('oferta_detail', oferta_id=nueva_oferta.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al publicar oferta: {str(e)}', 'danger')
    return render_template('ofertas/form.html', empleadores=empleadores)

@app.route('/ofertas/editar/<int:oferta_id>', methods=['GET', 'POST'])
def oferta_edit(oferta_id):
    oferta = OfertaLaboral.query.get_or_404(oferta_id)
    empleadores = Empleador.query.all()
    if request.method == 'POST':
        try:
            oferta.titulo = request.form['titulo']
            oferta.descripcion = request.form['descripcion']
            oferta.requisitos = request.form['requisitos']
            oferta.salario = request.form['salario'] if request.form['salario'] else None
            oferta.ubicacion = request.form['ubicacion']
            oferta.area = request.form['area']
            oferta.empleador_id = request.form['empleador_id']

            db.session.commit()
            flash('Oferta laboral actualizada exitosamente', 'success')
            return redirect(url_for('oferta_detail', oferta_id=oferta.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar oferta: {str(e)}', 'danger')
    return render_template('ofertas/form.html', oferta=oferta, empleadores=empleadores)

@app.route('/ofertas/eliminar/<int:oferta_id>', methods=['POST'])
def oferta_delete(oferta_id):
    oferta = OfertaLaboral.query.get_or_404(oferta_id)
    try:
        db.session.delete(oferta)
        db.session.commit()
        flash('Oferta laboral eliminada exitosamente', 'success')
        return redirect(url_for('ofertas_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar oferta: {str(e)}', 'danger')
        return redirect(url_for('oferta_detail', oferta_id=oferta_id))

# Rutas para Postulaciones
@app.route('/postulaciones')
def postulaciones_index():
    postulaciones = Postulacion.query.all()
    aspirantes = Aspirante.query.all()
    ofertas = OfertaLaboral.query.all()
    return render_template('postulaciones/index.html', postulaciones=postulaciones, aspirantes=aspirantes, ofertas=ofertas)

@app.route('/postulaciones/<int:postulacion_id>')
def postulacion_detail(postulacion_id):
    postulacion = Postulacion.query.get_or_404(postulacion_id)
    return render_template('postulaciones/detail.html', postulacion=postulacion)

@app.route('/postulaciones/nuevo', methods=['GET', 'POST'])
def postulacion_create():
    aspirantes = Aspirante.query.all()
    ofertas = OfertaLaboral.query.all()
    if request.method == 'POST':
        try:
            nueva_postulacion = Postulacion(
                aspirante_id=request.form['aspirante_id'],
                oferta_id=request.form['oferta_id']
            )
            db.session.add(nueva_postulacion)
            db.session.commit()
            flash('Postulación registrada exitosamente', 'success')
            return redirect(url_for('postulacion_detail', postulacion_id=nueva_postulacion.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar postulación: {str(e)}', 'danger')
    return render_template('postulaciones/form.html', aspirantes=aspirantes, ofertas=ofertas)

@app.route('/postulaciones/editar/<int:postulacion_id>', methods=['GET', 'POST'])
def postulacion_edit(postulacion_id):
    postulacion = Postulacion.query.get_or_404(postulacion_id)
    aspirantes = Aspirante.query.all()
    ofertas = OfertaLaboral.query.all()
    if request.method == 'POST':
        try:
            if 'estado' in request.form:
                postulacion.estado = request.form['estado']

            db.session.commit()
            flash('Postulación actualizada exitosamente', 'success')
            return redirect(url_for('postulacion_detail', postulacion_id=postulacion.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar postulación: {str(e)}', 'danger')
    return render_template('postulaciones/form.html', postulacion=postulacion, aspirantes=aspirantes, ofertas=ofertas)

@app.route('/postulaciones/cambiar-estado/<int:postulacion_id>', methods=['POST'])
def postulacion_cambiar_estado(postulacion_id):
    postulacion = Postulacion.query.get_or_404(postulacion_id)
    try:
        postulacion.estado = request.form['estado']
        db.session.commit()
        flash(f'Estado de postulación actualizado a {postulacion.estado}', 'success')
        return redirect(url_for('postulacion_detail', postulacion_id=postulacion.id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado: {str(e)}', 'danger')
        return redirect(url_for('postulacion_detail', postulacion_id=postulacion.id))

@app.route('/postulaciones/eliminar/<int:postulacion_id>', methods=['POST'])
def postulacion_delete(postulacion_id):
    postulacion = Postulacion.query.get_or_404(postulacion_id)
    try:
        db.session.delete(postulacion)
        db.session.commit()
        flash('Postulación eliminada exitosamente', 'success')
        return redirect(url_for('postulaciones_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar postulación: {str(e)}', 'danger')
        return redirect(url_for('postulacion_detail', postulacion_id=postulacion_id))

# Ruta para la API
@app.route('/api')
def api_index():
    return jsonify({
        'mensaje': 'API de Sistema de Contratación',
        'endpoints': {
            'aspirantes': '/api/aspirantes',
            'empleadores': '/api/empleadores',
            'ofertas': '/api/ofertas',
            'postulaciones': '/api/postulaciones'
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
