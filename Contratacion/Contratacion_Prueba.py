import datetime
import re


class OfertaLaboral:
    def __init__(self, cargo, requisitos, salario, fecha_publicacion, fecha_cierre, ubicacion, categoria,
                 tipo_contrato):
        self.cargo = cargo
        self.requisitos = requisitos
        self.salario = salario
        self.fecha_publicacion = fecha_publicacion
        self.fecha_cierre = fecha_cierre
        self.ubicacion = ubicacion
        self.categoria = categoria
        self.tipo_contrato = tipo_contrato
        self.activa = True


class SistemaRRHH:
    def __init__(self):
        self.ofertas = []

    def validar_texto(self, texto, campo):
        """Valida que el texto no esté vacío y tenga formato adecuado"""
        if not texto or texto.isspace():
            raise ValueError(f"El campo {campo} no puede estar vacío")
        return texto.strip()

    def validar_fecha(self, fecha_str, campo):
        """Valida que la fecha tenga formato correcto y sea futura para fechas de cierre"""
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
            if campo == "fecha de cierre" and fecha < datetime.date.today():
                raise ValueError("La fecha de cierre no puede ser anterior al día actual")
            return fecha
        except ValueError:
            raise ValueError(f"Formato de {campo} incorrecto. Use DD/MM/AAAA")

    def validar_salario(self, salario_str):
        """Valida que el salario sea un número positivo"""
        try:
            salario = float(salario_str)
            if salario <= 0:
                raise ValueError("El salario debe ser un valor positivo")
            return salario
        except ValueError:
            raise ValueError("El salario debe ser un número válido")

    def agregar_oferta(self):
        """Agrega una nueva oferta laboral con validación de datos"""
        print("\n--- Crear Nueva Oferta Laboral ---")

        try:
            cargo = self.validar_texto(input("Cargo: "), "cargo")
            requisitos = self.validar_texto(input("Requisitos: "), "requisitos")
            salario = self.validar_salario(input("Salario: "))
            fecha_publicacion = datetime.date.today()
            fecha_cierre = self.validar_fecha(input("Fecha de cierre (DD/MM/AAAA): "), "fecha de cierre")
            ubicacion = self.validar_texto(input("Ubicación: "), "ubicación")
            categoria = self.validar_texto(input("Categoría: "), "categoría")
            tipo_contrato = self.validar_texto(input("Tipo de contrato: "), "tipo de contrato")

            nueva_oferta = OfertaLaboral(
                cargo, requisitos, salario, fecha_publicacion,
                fecha_cierre, ubicacion, categoria, tipo_contrato
            )

            self.ofertas.append(nueva_oferta)
            print("\n Oferta laboral creada exitosamente!")

        except ValueError as e:
            print(f"\n Error: {e}")

    def mostrar_ofertas(self, ofertas=None):
        """Muestra las ofertas laborales"""
        print(len(self.ofertas))
        if ofertas is None:
            ofertas = self.ofertas

        if not ofertas:
            print("\nNo hay ofertas laborales disponibles.")
            return

        print("\n--- Ofertas Laborales ---")
        for i, oferta in enumerate(ofertas, 1):
            print(f"\nOferta #{i}")
            print(f"Cargo: {oferta.cargo}")
            print(f"Requisitos: {oferta.requisitos}")
            print(f"Salario: ${oferta.salario:,.2f}")
            print(f"Fecha Publicación: {oferta.fecha_publicacion.strftime('%d/%m/%Y')}")
            print(f"Fecha Cierre: {oferta.fecha_cierre.strftime('%d/%m/%Y')}")  # Error corregido: era "fecha_cierre"
            print(f"Ubicación: {oferta.ubicacion}")
            print(f"Categoría: {oferta.categoria}")
            print(f"Tipo de Contrato: {oferta.tipo_contrato}")  # Error corregido: era "tipo_contrato"
            print(f"Estado: {'Activa' if oferta.activa else 'Cerrada'}")

    def filtrar_ofertas(self):
        """Permite filtrar ofertas por diferentes criterios"""
        print("\n--- Filtrar Ofertas Laborales ---")
        print("1. Por ubicación")
        print("2. Por categoría")
        print("3. Por tipo de contrato")
        print("4. Por rango salarial")
        print("5. Ofertas activas")
        print("6. Volver al menú principal")

        try:
            opcion = input("\nSeleccione un criterio de filtrado: ")

            if opcion == "1":
                ubicacion = self.validar_texto(input("Ingrese ubicación a buscar: "), "ubicación")
                filtradas = [o for o in self.ofertas if o.ubicacion.lower() == ubicacion.lower()]
                self.mostrar_ofertas(filtradas)

            elif opcion == "2":
                categoria = self.validar_texto(input("Ingrese categoría a buscar: "), "categoría")
                filtradas = [o for o in self.ofertas if o.categoria.lower() == categoria.lower()]
                self.mostrar_ofertas(filtradas)

            elif opcion == "3":
                tipo_contrato = self.validar_texto(input("Ingrese tipo de contrato a buscar: "), "tipo de contrato")
                filtradas = [o for o in self.ofertas if o.tipo_contrato.lower() == tipo_contrato.lower()]
                self.mostrar_ofertas(filtradas)

            elif opcion == "4":
                min_salario = self.validar_salario(input("Salario mínimo: "))
                max_salario = self.validar_salario(input("Salario máximo: "))
                filtradas = [o for o in self.ofertas if min_salario <= o.salario <= max_salario]
                self.mostrar_ofertas(filtradas)

            elif opcion == "5":
                filtradas = [o for o in self.ofertas if o.activa]
                self.mostrar_ofertas(filtradas)

            elif opcion == "6":
                return

            else:
                print("\n Opción no válida")

        except ValueError as e:
            print(f"\n Error: {e}")

    def actualizar_ofertas(self):
        """Actualiza el estado de las ofertas (activa/cerrada) según fecha de cierre"""
        hoy = datetime.date.today()
        for oferta in self.ofertas:
            if oferta.fecha_cierre < hoy:
                oferta.activa = False

    def menu_principal(self):
        """Muestra el menú principal del sistema"""
        while True:
            self.actualizar_ofertas()  # Actualiza estados en tiempo real

            print("\n=== SISTEMA DE GESTIÓN DE OFERTAS LABORALES ===")
            print("1. Crear nueva oferta laboral")
            print("2. Ver todas las ofertas laborales")
            print("3. Filtrar ofertas laborales")
            print("4. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.agregar_oferta()
            elif opcion == "2":
                self.mostrar_ofertas()
            elif opcion == "3":
                self.filtrar_ofertas()
            elif opcion == "4":
                print("\n¡Gracias por usar el sistema de gestión de ofertas laborales!")
                break
            else:
                print("\n Opción no válida. Intente nuevamente.")


# Ejecutar el sistema
if __name__ == "__main__":
    sistema = SistemaRRHH()
    sistema.menu_principal()