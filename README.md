# Benchmark Criptográfico: AEGIS-128L vs. AES-128-GCM

Este proyecto consiste en un script de benchmarking desarrollado en Python para comparar el rendimiento real del algoritmo de cifrado autenticado **AEGIS-128L** frente al estándar de la industria **AES-128-GCM**.

## 📋 Requisitos Previos

El script requiere tener instalado Python 3 y dos dependencias criptográficas:
1. `pynacl`: Interfaz de Python para `libsodium`, que provee la primitiva de AEGIS-128L.
2. `cryptography`: Librería estándar de producción que interactúa con OpenSSL para ejecutar AES-GCM por hardware.

## 🚀 Instalación y Ejecucion

pip3 install pynacl cryptography
python3 benchmark.py

Que decir en la presentacion:
1. En los papers teóricos, AEGIS-128L destruye a AES-GCM en velocidad. Sin embargo, en nuestro benchmark real corriendo bajo Python en una Mac ARM64, AES-GCM gana por más de 60 veces.

2. Mientras que AES-GCM está respaldado por OpenSSL con ensamblador nativo para el chip Apple Silicon, la librería actual de AEGIS en Python no tiene mapeadas las extensiones criptográficas vectoriales para arquitecturas ARM, obligando al procesador a resolverlo por software.
3. Esto valida empíricamente la sección de 'Vulnerabilidades y consideraciones' de nuestro TP escrito: la asombrosa velocidad de AEGIS-128L es altamente dependiente del hardware y de que el entorno de software implemente correctamente. Sin esa alineación perfecta, el estándar de la industria (AES-GCM) sigue siendo la opción más robusta y veloz en entornos de producción diversos.
