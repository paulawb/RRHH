class Aspirante:
    def __init__(self, nombre, apellido, edad, correo, telefono, educacion, cargo, enlace_cv="N/A"):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.correo = correo
        self.telefono = telefono
        self.educacion = educacion
        self.cargo = cargo
        self.enlace_cv = enlace_cv if enlace_cv else "N/A"
    
    def __str__(self):
        return (f"{self.nombre} {self.apellido} - {self.cargo}\n"
                f"   Edad: {self.edad}, Correo: {self.correo}, Teléfono: {self.telefono}\n"
                f"   Educación: {self.educacion}\n"
                f"   Enlace CV: {self.enlace_cv}\n"
                + "-" * 50)

class RegistroAspirantes:
    def __init__(self):
        self.aspirantes = []
    
    def registrar(self):
        while True:
            print("\nIngrese los datos del aspirante (o escriba 'salir' en nombre para terminar):")
            nombre = input("Nombre: ")
            if nombre.lower() == 'salir':
                break
            apellido = input("Apellido: ")
            edad = input("Edad: ")
            correo = input("Correo: ")
            telefono = input("Teléfono: ")
            educacion = input("Educación: ")
            cargo = input("Cargo a aspirar: ")
            enlace_cv = input("Enlace al CV (opcional): ")
            
            aspirante = Aspirante(nombre, apellido, edad, correo, telefono, educacion, cargo, enlace_cv)
            self.aspirantes.append(aspirante)
            print("Aspirante registrado con éxito.\n")
    
    def listar(self):
        print("\nLista de Aspirantes:")
        for i, aspirante in enumerate(self.aspirantes, start=1):
            print(f"{i}. {aspirante}")

if __name__ == '__main__':
    # Ejecución del programa
    registro = RegistroAspirantes()
    registro.registrar()
    registro.listar()
