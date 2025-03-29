from Models.EulerSimulador import EulerSimulador
from Models.VerletSimulador import VerletSimulador
from Views.VistaOrbital import VistaOrbital
from Controllers.Controlador import Controlador

# Elegir método (EulerSimulador o VerletSimulador)
simulador = VerletSimulador(dt=86400, velocidad_inicial=29783)
vista = VistaOrbital(simulador)
controlador = Controlador(simulador, vista)

controlador.ejecutar_simulacion()
