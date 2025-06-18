"""
Sistema de Emparejamiento de Empleados y Clientes
Implementación usando POO y principios SOLID
Algoritmo de Maximum Bipartite Matching usando Ford-Fulkerson
"""

from abc import ABC, abstractmethod
from typing import List
import os


class Empleado:
    """Clase que representa un empleado con sus características"""

    def __init__(self, nombre: str, ocupacion: str, precio_por_hora: float):
        self._nombre = nombre
        self._ocupacion = ocupacion
        self._precio_por_hora = precio_por_hora

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def ocupacion(self) -> str:
        return self._ocupacion

    @property
    def precio_por_hora(self) -> float:
        return self._precio_por_hora

    def __str__(self) -> str:
        return f"{self._nombre} ({self._ocupacion}, ${self._precio_por_hora}/h)"


class Cliente:
    """Clase que representa un cliente con sus requerimientos"""

    def __init__(self, nombre: str, ocupacion_requerida: str, presupuesto: float):
        self._nombre = nombre
        self._ocupacion_requerida = ocupacion_requerida
        self._presupuesto = presupuesto

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def ocupacion_requerida(self) -> str:
        return self._ocupacion_requerida

    @property
    def presupuesto(self) -> float:
        return self._presupuesto

    def puede_contratar(self, empleado: Empleado) -> bool:
        """Verifica si el cliente puede contratar al empleado"""
        return (
            self._ocupacion_requerida == empleado.ocupacion
            and self._presupuesto >= empleado.precio_por_hora
        )

    def __str__(self) -> str:
        return f"{self._nombre} (necesita {self._ocupacion_requerida}, presupuesto ${self._presupuesto})"


class Emparejamiento:
    """Clase que representa un emparejamiento entre cliente y empleado"""

    def __init__(self, cliente: Cliente, empleado: Empleado):
        self._cliente = cliente
        self._empleado = empleado

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def empleado(self) -> Empleado:
        return self._empleado

    def __str__(self) -> str:
        return f"{self._cliente.nombre} - {self._empleado.nombre}"


class ILectorArchivos(ABC):
    """Interfaz para lectura de archivos (Principio de Inversión de Dependencias)"""

    @abstractmethod
    def leer_empleados(self, ruta_archivo: str) -> List[Empleado]:
        pass

    @abstractmethod
    def leer_clientes(self, ruta_archivo: str) -> List[Cliente]:
        pass


class LectorArchivosTexto(ILectorArchivos):
    """Implementación concreta para leer archivos de texto"""

    def leer_empleados(self, ruta_archivo: str) -> List[Empleado]:
        """Lee desde archivo de texto"""
        empleados = []

        try:
            if not os.path.exists(ruta_archivo):
                raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")

            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                for numero_linea, linea in enumerate(archivo, 1):
                    linea = linea.strip()
                    if not linea:  # Saltar líneas vacías
                        continue

                    try:
                        partes = linea.split(";")
                        if len(partes) != 3:
                            raise ValueError(
                                f"Formato incorrecto en línea {numero_linea}"
                            )

                        nombre, ocupacion, precio_str = partes
                        precio = float(precio_str)

                        if precio < 0:
                            raise ValueError(
                                f"El precio no puede ser negativo en línea {numero_linea}"
                            )

                        empleados.append(
                            Empleado(nombre.strip(), ocupacion.strip(), precio)
                        )

                    except ValueError as e:
                        print(f"Error procesando empleado en línea {numero_linea}: {e}")
                        continue

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return []
        except Exception as e:
            print(f"Error inesperado leyendo empleados: {e}")
            return []

        return empleados

    def leer_clientes(self, ruta_archivo: str) -> List[Cliente]:
        """Lee clientes desde archivo de texto"""
        clientes = []

        try:
            if not os.path.exists(ruta_archivo):
                raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")

            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                for numero_linea, linea in enumerate(archivo, 1):
                    linea = linea.strip()
                    if not linea:  # Saltar líneas vacías
                        continue

                    try:
                        partes = linea.split(";")
                        if len(partes) != 3:
                            raise ValueError(
                                f"Formato incorrecto en línea {numero_linea}"
                            )

                        nombre, ocupacion_requerida, presupuesto_str = partes
                        presupuesto = float(presupuesto_str)

                        if presupuesto < 0:
                            raise ValueError(
                                f"El presupuesto no puede ser negativo en línea {numero_linea}"
                            )

                        clientes.append(
                            Cliente(
                                nombre.strip(), ocupacion_requerida.strip(), presupuesto
                            )
                        )

                    except ValueError as e:
                        print(f"Error procesando cliente en línea {numero_linea}: {e}")
                        continue

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return []
        except Exception as e:
            print(f"Error inesperado leyendo clientes: {e}")
            return []

        return clientes


class IAlgoritmoEmparejamiento(ABC):
    """Interfaz para algoritmos de emparejamiento (Principio Abierto/Cerrado)"""

    @abstractmethod
    def encontrar_emparejamientos_maximos(
        self, clientes: List[Cliente], empleados: List[Empleado]
    ) -> List[Emparejamiento]:
        pass


class AlgoritmoEmparejamientoBipartito(IAlgoritmoEmparejamiento):
    """
    Implementación del algoritmo de Maximum Bipartite Matching
    usando el enfoque de Ford-Fulkerson con DFS
    """

    def __init__(self):
        self._grafo_compatibilidad = {}
        self._emparejamiento_clientes = {}
        self._emparejamiento_empleados = {}

    def encontrar_emparejamientos_maximos(
        self, clientes: List[Cliente], empleados: List[Empleado]
    ) -> List[Emparejamiento]:
        """Encuentra el emparejamiento máximo usando algoritmo bipartito"""

        # Reiniciar estructuras
        self._grafo_compatibilidad = {}
        self._emparejamiento_clientes = {}
        self._emparejamiento_empleados = {}

        # Construir grafo de compatibilidad
        self._construir_grafo_compatibilidad(clientes, empleados)

        # Aplicar algoritmo de emparejamiento máximo
        for i, cliente in enumerate(clientes):
            visitados = set()
            self._buscar_camino_aumentante(i, visitados)

        # Construir lista de emparejamientos
        return self._construir_emparejamientos(clientes, empleados)

    def _construir_grafo_compatibilidad(
        self, clientes: List[Cliente], empleados: List[Empleado]
    ):
        """Construye el grafo de compatibilidad entre clientes y empleados"""
        for i, cliente in enumerate(clientes):
            self._grafo_compatibilidad[i] = []
            for j, empleado in enumerate(empleados):
                if cliente.puede_contratar(empleado):
                    self._grafo_compatibilidad[i].append(j)

    def _buscar_camino_aumentante(self, cliente_idx: int, visitados: set) -> bool:
        """
        Busca un camino aumentante usando DFS
        Retorna True si encuentra un emparejamiento para el cliente
        """
        for empleado_idx in self._grafo_compatibilidad.get(cliente_idx, []):
            if empleado_idx in visitados:
                continue

            visitados.add(empleado_idx)

            # Si el empleado no está emparejado o podemos encontrar
            # un emparejamiento alternativo para su cliente actual
            if (
                empleado_idx not in self._emparejamiento_empleados
                or self._buscar_camino_aumentante(
                    self._emparejamiento_empleados[empleado_idx], visitados
                )
            ):

                # Realizar emparejamiento
                self._emparejamiento_clientes[cliente_idx] = empleado_idx
                self._emparejamiento_empleados[empleado_idx] = cliente_idx
                return True

        return False

    def _construir_emparejamientos(
        self, clientes: List[Cliente], empleados: List[Empleado]
    ) -> List[Emparejamiento]:
        """Construye la lista final de emparejamientos"""
        emparejamientos = []

        for cliente_idx, empleado_idx in self._emparejamiento_clientes.items():
            cliente = clientes[cliente_idx]
            empleado = empleados[empleado_idx]
            emparejamientos.append(Emparejamiento(cliente, empleado))

        return emparejamientos


class IVisualizadorResultados(ABC):
    """Interfaz para mostrar resultados (Principio de Responsabilidad Única)"""

    @abstractmethod
    def mostrar_resultados(self, emparejamientos: List[Emparejamiento]):
        pass


class VisualizadorConsola(IVisualizadorResultados):
    """Implementación para mostrar resultados en consola"""

    def mostrar_resultados(self, emparejamientos: List[Emparejamiento]):
        """Muestra los resultados en la consola"""
        print("\n=== RESULTADOS DEL EMPAREJAMIENTO ===")
        print()

        if not emparejamientos:
            print("No se encontraron emparejamientos posibles.")
            return

        print("Emparejamientos encontrados:")
        for emparejamiento in emparejamientos:
            print(f"  {emparejamiento}")

        print()
        print(f"Cantidad total de emparejamientos: {len(emparejamientos)}")


class GestorEmparejamientos:
    """
    Clase principal que coordina todo el proceso de emparejamiento
    (Principio de Responsabilidad Única y Composición)
    """

    def __init__(
        self,
        lector_archivos: ILectorArchivos,
        algoritmo_emparejamiento: IAlgoritmoEmparejamiento,
        visualizador: IVisualizadorResultados,
    ):
        self._lector_archivos = lector_archivos
        self._algoritmo_emparejamiento = algoritmo_emparejamiento
        self._visualizador = visualizador

    def ejecutar_emparejamiento(self, ruta_empleados: str, ruta_clientes: str):
        """Ejecuta todo el proceso de emparejamiento"""
        try:
            print("\nCargando datos...")

            # Cargar empleados y clientes
            empleados = self._lector_archivos.leer_empleados(ruta_empleados)
            clientes = self._lector_archivos.leer_clientes(ruta_clientes)

            if not empleados:
                print("No se pudieron cargar empleados. Verificar archivo.")
                return

            if not clientes:
                print("No se pudieron cargar clientes. Verificar archivo.")
                return

            print(f"Cargados {len(empleados)} empleados y {len(clientes)} clientes.")

            # Ejecutar algoritmo de emparejamiento
            print("Ejecutando algoritmo de emparejamiento...")
            emparejamientos = (
                self._algoritmo_emparejamiento.encontrar_emparejamientos_maximos(
                    clientes, empleados
                )
            )

            # Mostrar resultados
            self._visualizador.mostrar_resultados(emparejamientos)

        except Exception as e:
            print(f"Error durante el proceso de emparejamiento: {e}")


class MenuInteractivo:
    """Clase para manejar la interfaz de usuario del menú interactivo"""

    def __init__(self, gestor: GestorEmparejamientos):
        self._gestor = gestor

    def mostrar_menu_principal(self):
        """Muestra el menú principal y maneja las opciones"""
        while True:
            self._imprimir_encabezado()
            self._imprimir_opciones_menu()

            try:
                opcion = input("Seleccione una opción (1-3): ").strip()

                if opcion == "1":
                    self._crear_archivos_ejemplo()
                elif opcion == "2":
                    self._usar_archivos_personalizados()
                elif opcion == "3":
                    print("\n¡Gracias por usar el sistema de emparejamiento!")
                    break
                else:
                    print("\n❌ Opción no válida. Por favor, seleccione 1, 2 o 3.")
                    input("Presione Enter para continuar...")

            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                input("Presione Enter para continuar...")

    def _imprimir_encabezado(self):
        """Imprime el encabezado del menú"""
        print("\n" + "=" * 60)
        print("    SISTEMA DE EMPAREJAMIENTO EMPLEADOS-CLIENTES")
        print("=" * 60)

    def _imprimir_opciones_menu(self):
        """Imprime las opciones del menú"""
        print("\nOpciones disponibles:")
        print("  1. 📁 Crear archivos de ejemplo y ejecutar emparejamiento")
        print("  2. 📂 Usar archivos personalizados (Ingresar rutas)")
        print("  3. 🚪 Salir")
        print("-" * 60)

    def _crear_archivos_ejemplo(self):
        """Opción 1: Crear archivos de ejemplo y ejecutar"""
        print("\n📁 Creando archivos de ejemplo...")

        try:
            self._generar_archivos_ejemplo()
            print("✅ Archivos de ejemplo creados exitosamente:")
            print(f"   • empleados.txt (en {os.getcwd()})")
            print(f"   • clientes.txt (en {os.getcwd()})")

            # Ejecutar emparejamiento automáticamente
            self._gestor.ejecutar_emparejamiento("empleados.txt", "clientes.txt")

        except Exception as e:
            print(f"❌ Error al crear archivos de ejemplo: {e}")

        input("\nPresione Enter para volver al menú principal...")

    def _usar_archivos_personalizados(self):
        """Opción 2: Usar archivos proporcionados por el usuario"""
        print("\n📂 Usando archivos personalizados")
        print("Por favor, proporcione las rutas absolutas de sus archivos:")

        try:
            # Solicitar ruta del archivo de empleados
            ruta_empleados = self._solicitar_ruta_archivo("empleados")
            if not ruta_empleados:
                return

            # Solicitar ruta del archivo de clientes
            ruta_clientes = self._solicitar_ruta_archivo("clientes")
            if not ruta_clientes:
                return

            # Ejecutar emparejamiento
            self._gestor.ejecutar_emparejamiento(ruta_empleados, ruta_clientes)

        except Exception as e:
            print(f"❌ Error al procesar archivos personalizados: {e}")

        input("\nPresione Enter para volver al menú principal...")

    def _solicitar_ruta_archivo(self, tipo_archivo: str) -> str:
        """Solicita y valida la ruta de un archivo"""
        while True:
            print(f"\n📄 Archivo de {tipo_archivo}:")
            print("  Formato esperado: nombre;ocupacion;precio_por_hora (empleados)")
            print(
                "  Formato esperado: nombre;ocupacion_requerida;presupuesto (clientes)"
            )

            ruta = input(
                f"Ingrese la ruta absoluta del archivo de {tipo_archivo} (o 'volver' para regresar): "
            ).strip()

            if ruta.lower() == "volver":
                return ""

            if not ruta:
                print("❌ Por favor, ingrese una ruta válida.")
                continue

            # Verificar si el archivo existe
            if not os.path.exists(ruta):
                print(f"❌ El archivo '{ruta}' no existe.")
                print("   Verifique que la ruta sea correcta y que el archivo exista.")
                continue

            # Verificar si es un archivo (no un directorio)
            if not os.path.isfile(ruta):
                print(f"❌ '{ruta}' no es un archivo válido.")
                continue

            print(f"✅ Archivo de {tipo_archivo} validado correctamente.")
            return ruta

    def _generar_archivos_ejemplo(self):
        """Genera archivos de ejemplo en el directorio actual"""
        # Crear archivo de empleados de ejemplo
        empleados_ejemplo = [
            "Juan;Programador;20",
            "Maria;Diseñador;25",
            "Carlos;Programador;30",
            "Ana;Diseñador;22",
            "Luis;Contador;18",
            "Sofia;Programador;35",
            "Pedro;Contador;20",
            "Laura;Diseñador;28",
        ]

        with open("empleados.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(empleados_ejemplo))

        # Crear archivo de clientes de ejemplo
        clientes_ejemplo = [
            "Cliente1;Programador;100",
            "Cliente2;Diseñador;50",
            "Cliente3;Programador;25",
            "Cliente4;Contador;20",
            "Cliente5;Diseñador;30",
            "Cliente6;Programador;40",
            "Cliente7;Contador;25",
        ]

        with open("clientes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(clientes_ejemplo))


def main():
    """Función principal del programa"""
    try:
        # Configurar dependencias (Inyección de Dependencias)
        lector_archivos = LectorArchivosTexto()
        algoritmo_emparejamiento = AlgoritmoEmparejamientoBipartito()
        visualizador = VisualizadorConsola()

        # Crear gestor principal
        gestor = GestorEmparejamientos(
            lector_archivos, algoritmo_emparejamiento, visualizador
        )

        # Crear y ejecutar menú interactivo
        menu = MenuInteractivo(gestor)
        menu.mostrar_menu_principal()

    except Exception as e:
        print(f"❌ Error crítico en el programa: {e}")
        input("Presione Enter para salir...")


if __name__ == "__main__":
    main()
