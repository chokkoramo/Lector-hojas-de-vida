import json

class Applicant:
    """
    Representa la información de un aplicante.
    """
    def __init__(self, nombre, contacto, perfil, experiencia, educacion, referencias):
        self.nombre = nombre
        self.contacto = contacto
        self.perfil = perfil
        self.experiencia = experiencia
        self.educacion = educacion
        self.referencias = referencias

    def to_dict(self):
        return {
            "Nombre": self.nombre,
            "Contacto": self.contacto,
            "Perfil Profesional": self.perfil,
            "Experiencia Profesional": self.experiencia,
            "Educación": self.educacion,
            "Referencias": self.referencias,
        }

    def __str__(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)
