import unittest
from cv_candidatos import *
from io import StringIO
import sys

class TestAspirante(unittest.TestCase):
    def setUp(self):
        self.aspirante = Aspirante("Juan", "Perez", 30, "juan@example.com", "1234567890", "Ingeniería", "Desarrollador", "http://cv.com/juan")

    def test_creacion_aspirante(self):
        self.assertEqual(self.aspirante.nombre, "Juan")
        self.assertEqual(self.aspirante.apellido, "Perez")
        self.assertEqual(self.aspirante.edad, 30)
        self.assertEqual(self.aspirante.correo, "juan@example.com")
        self.assertEqual(self.aspirante.telefono, "1234567890")
        self.assertEqual(self.aspirante.educacion, "Ingeniería")
        self.assertEqual(self.aspirante.cargo, "Desarrollador")
        self.assertEqual(self.aspirante.enlace_cv, "http://cv.com/juan")
    
    def test_creacion_sin_cv(self):
        aspirante_sin_cv = Aspirante("Ana", "Lopez", 25, "ana@example.com", "0987654321", "Arquitectura", "Diseñador", "")
        self.assertEqual(aspirante_sin_cv.enlace_cv, "N/A")

    def test_str(self):
        resultado_esperado = ("Juan Perez - Desarrollador\n"
                              "   Edad: 30, Correo: juan@example.com, Teléfono: 1234567890\n"
                              "   Educación: Ingeniería\n"
                              "   Enlace CV: http://cv.com/juan\n"
                              + "-" * 50)
        self.assertEqual(str(self.aspirante), resultado_esperado)

class TestRegistroAspirantes(unittest.TestCase):
    def setUp(self):
        self.registro = RegistroAspirantes()
        self.aspirante = Aspirante("Carlos", "Ramirez", 28, "carlos@example.com", "1112223333", "Administración", "Gerente", "http://cv.com/carlos")
        self.registro.aspirantes.append(self.aspirante)

    def test_registrar_manual(self):
        self.assertEqual(len(self.registro.aspirantes), 1)
        self.assertEqual(self.registro.aspirantes[0].nombre, "Carlos")
    
    def test_listar(self):
        salida_esperada = "\nLista de Aspirantes:\n1. Carlos Ramirez - Gerente\n"
        salida_esperada += "   Edad: 28, Correo: carlos@example.com, Teléfono: 1112223333\n"
        salida_esperada += "   Educación: Administración\n   Enlace CV: http://cv.com/carlos\n"
        salida_esperada += "-" * 50 + "\n"
        
        sys.stdout = StringIO()
        self.registro.listar()
        salida_obtenida = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__
        
        self.assertEqual(salida_obtenida, salida_esperada)

if __name__ == "__main__":
    unittest.main()
