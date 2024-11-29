from experta import *
from experta import Rule, Fact
from experta import KnowledgeEngine
from experta import *

class DatosSuelo(Fact):
    """Información del suelo"""
    pass

class DatosClima(Fact):
    """Información del clima"""
    pass

class DatosCultivo(Fact):
    """Información del cultivo"""
    pass

class AsesorAgricola(KnowledgeEngine):
    
    @Rule(DatosSuelo(nutrientes="bajo"), DatosCultivo(tipo_cultivo="maíz"))
    def fertilizacion_maiz(self):
        print("Recomendación: El nivel de nutrientes del suelo es bajo. Para maíz, aplicar fertilizante NPK con mayor concentración de nitrógeno.")
    
    @Rule(DatosSuelo(nutrientes="alto"), DatosCultivo(tipo_cultivo="maíz"))
    def fertilizacion_maiz_alto(self):
        print("Recomendación: El nivel de nutrientes del suelo es alto. Reducir el uso de fertilizantes y monitorear el crecimiento.")

    @Rule(DatosSuelo(humedad=P(lambda x: x < 30)))
    def bajo_nivel_humedad(self):
        print("El suelo tiene un bajo nivel de humedad. Considera aumentar la frecuencia de riego.")
    
    @Rule(DatosSuelo(humedad=P(lambda x: x > 70)))
    def alto_nivel_humedad(self):
        print("El suelo tiene un alto nivel de humedad. Disminuir el riego y revisar drenajes para evitar encharcamiento.")
    
    @Rule(DatosClima(temperatura=P(lambda x: x < 15)))
    def baja_temperatura(self):
        print("Las temperaturas son bajas. Considera proteger los cultivos del frío.")
    
    @Rule(DatosClima(temperatura=P(lambda x: x > 30)))
    def alta_temperatura(self):
        print("Las temperaturas son muy altas. Incrementar la frecuencia de riego para evitar estrés hídrico.")
    
    @Rule(DatosCultivo(tipo_cultivo="trigo", estado="enfermo"))
    def trigo_enfermo(self):
        print("El cultivo de trigo está enfermo. Realizar un análisis fitosanitario y aplicar fungicidas adecuados.")
    
    @Rule(DatosCultivo(tipo_cultivo="tomate", estado="enfermo"))
    def tomate_enfermo(self):
        print("El cultivo de tomate está enfermo. Inspeccionar para detectar plagas y aplicar insecticidas adecuados.")
    
    @Rule(NOT(DatosCultivo(tipo_cultivo="maíz")),
          NOT(DatosCultivo(tipo_cultivo="trigo")),
          NOT(DatosCultivo(tipo_cultivo="tomate")))
    def sin_recomendacion(self):
        print("No hay recomendaciones específicas para este tipo de cultivo.")

# Funciones para validaciones de entradas
def validar_numero(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("Por favor, ingrese un número válido.")

def validar_opcion(mensaje, opciones):
    while True:
        valor = input(mensaje).strip().lower()
        if valor in opciones:
            return valor
        print(f"Por favor, elija una opción válida: {', '.join(opciones)}")

# Iniciar el motor de conocimiento
motor = AsesorAgricola()

motor.reset()

# Solicitar información al usuario con validaciones
humedad_suelo = validar_numero("Ingrese la humedad del suelo (%): ")
pH_suelo = validar_numero("Ingrese el pH del suelo: ")
tipo_suelo = validar_opcion("Ingrese el tipo de suelo (arcilloso/arenoso): ", ["arcilloso", "arenoso"])
nivel_nutrientes = validar_opcion("Nivel de nutrientes del suelo (alto/bajo): ", ["alto", "bajo"])
temperatura = validar_numero("Ingrese la temperatura actual (°C): ")
lluvia = validar_opcion("¿Hay presencia de lluvia? (si/no): ", ["si", "no"])
humedad_ambiental = validar_numero("Ingrese la humedad ambiental (%): ")
tipo_cultivo = validar_opcion("Ingrese el tipo de cultivo (maíz/trigo/tomate): ", ["maíz", "trigo", "tomate"])
estado_cultivo = validar_opcion("Ingrese el estado del cultivo (saludable/enfermo): ", ["saludable", "enfermo"])

# Declarar hechos al motor
motor.declare(DatosSuelo(humedad=humedad_suelo, pH=pH_suelo, tipo_suelo=tipo_suelo, nutrientes=nivel_nutrientes))
motor.declare(DatosClima(temperatura=temperatura, lluvia=lluvia, humedad=humedad_ambiental))
motor.declare(DatosCultivo(tipo_cultivo=tipo_cultivo, estado=estado_cultivo))

# Ejecutar el motor de inferencia
motor.run()
