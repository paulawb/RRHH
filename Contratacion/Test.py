import unittest
import datetime
from Contratacion_Prueba import SistemaRRHH, OfertaLaboral  # Reemplaza 'your_module' con el nombre real del archivo

class TestSistemaRRHH(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaRRHH()

    def test_validar_texto(self):
        self.assertEqual(self.sistema.validar_texto("Programador", "cargo"), "Programador")
        with self.assertRaises(ValueError):
            self.sistema.validar_texto(" ", "cargo")
        with self.assertRaises(ValueError):
            self.sistema.validar_texto("", "cargo")

    def test_validar_fecha(self):
        fecha_valida = "25/12/2025"
        fecha_invalida = "01/01/2020"
        self.assertEqual(self.sistema.validar_fecha(fecha_valida, "fecha de cierre"), datetime.date(2025, 12, 25))
        with self.assertRaises(ValueError):
            self.sistema.validar_fecha(fecha_invalida, "fecha de cierre")
        with self.assertRaises(ValueError):
            self.sistema.validar_fecha("32/13/2023", "fecha de cierre")  # Fecha inválida

    def test_validar_salario(self):
        self.assertEqual(self.sistema.validar_salario("5000"), 5000.0)
        self.assertEqual(self.sistema.validar_salario("1000.50"), 1000.5)
        with self.assertRaises(ValueError):
            self.sistema.validar_salario("-100")
        with self.assertRaises(ValueError):
            self.sistema.validar_salario("abc")

    def test_agregar_oferta(self):
        oferta = OfertaLaboral("Desarrollador", "Python", 3000.0, datetime.date.today(), datetime.date.today(), "Madrid", "IT", "Indefinido")
        self.sistema.ofertas.append(oferta)
        self.assertEqual(len(self.sistema.ofertas), 1)
        self.assertEqual(self.sistema.ofertas[0].cargo, "Desarrollador")

    def test_actualizar_ofertas(self):
        oferta_activa = OfertaLaboral("Dev", "Python", 3000, datetime.date.today(), datetime.date.today() + datetime.timedelta(days=5), "Madrid", "IT", "Indefinido")
        oferta_cerrada = OfertaLaboral("Tester", "QA", 2000, datetime.date.today(), datetime.date.today() - datetime.timedelta(days=1), "Barcelona", "QA", "Temporal")
        self.sistema.ofertas.append(oferta_activa)
        self.sistema.ofertas.append(oferta_cerrada)
        self.sistema.actualizar_ofertas()
        self.assertTrue(self.sistema.ofertas[0].activa)
        self.assertFalse(self.sistema.ofertas[1].activa)

if __name__ == "__main__":
    unittest.main()
