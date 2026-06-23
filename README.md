# Benchmark Criptográfico: AEGIS-128L vs. AES-128-GCM

Este proyecto consiste en un script de benchmarking desarrollado en Python para comparar el rendimiento real del algoritmo de cifrado autenticado **AEGIS-128L** frente al estándar de la industria **AES-128-GCM**.

## 📋 Requisitos Previos

El script requiere tener instalado Python 3 y dos dependencias criptográficas:
1. `pynacl`: Interfaz de Python para `libsodium`, que provee la primitiva de AEGIS-128L.
2. `cryptography`: Librería estándar de producción que interactúa con OpenSSL para ejecutar AES-GCM por hardware.

## 🚀 Instalación y Ejecucion

pip3 install pynacl cryptography
python3 benchmark.py
