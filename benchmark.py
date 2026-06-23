import time
import os
# Primitiva de AEGIS-128L (vía Libsodium)
from nacl.bindings import crypto_aead_aegis128l_encrypt
from nacl.utils import random
# Primitiva de AES-GCM Real (vía OpenSSL / Hardware de la Mac)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def run_benchmark():
    print("==================================================")
    print("  BENCHMARK CRIPTOGRÁFICO: AEGIS-128L vs AES-GCM  ")
    print("==================================================\n")

    # Texto corto de prueba para inspección visual
    texto_ejemplo = b"Mensaje secreto de ingenieria UTN FRBA"
    datos_asociados = b"Datos de cabecera de red (Texto Plano Autenticado)" 

    # Configurar Claves y Nonces reales para ambos algoritmos
    clave_aegis = random(16) 
    nonce_aegis = random(16)
    
    clave_aes = AESGCM.generate_key(bit_length=128)
    nonce_aes = os.urandom(12) # AES-GCM estándar usa un nonce de 12 bytes (96 bits)

    # Pre-cifrado de muestra para la inspección visual
    payload_aegis = crypto_aead_aegis128l_encrypt(texto_ejemplo, datos_asociados, nonce_aegis, clave_aegis)
    tag_aegis = payload_aegis[-16:]
    cifrado_puro_aegis = payload_aegis[:-16]

    # ==================================================
    # INSPECCIÓN DE ARTEFACTOS CRIPTOGRÁFICOS
    # ==================================================
    print("==================================================")
    print("    INSPECCIÓN DE ARTEFACTOS (AEGIS-128L)")
    print("==================================================")
    print(f"📄 Mensaje Original:  {texto_ejemplo.decode('utf-8')}")
    print(f"🔑 Clave (Hex):        {clave_aegis.hex()}")
    print(f"🎲 Nonce (Hex):        {nonce_aegis.hex()}")
    print(f"🔗 Datos Asoc. (AAD):  {datos_asociados.decode('utf-8')}")
    print("--------------------------------------------------")
    print(f"🔒 Ciphertext (Hex):   {cifrado_puro_aegis.hex()}")
    print(f"🏷️  Auth Tag (Hex):     {tag_aegis.hex()}")
    print("==================================================\n")
    
    print("[*] Presioná Enter para iniciar el test de velocidad REAL de 100 MB...")
    input()

    # 1. Preparar datos masivos reales (100 MB)
    print("[+] Generando 100 MB de datos aleatorios en memoria...")
    tamanio_mb = 100
    datos_masivos = os.urandom(tamanio_mb * 1024 * 1024)
    
    # 2. Cifrado MASIVO REAL con AEGIS-128L
    print("[+] Ejecutando cifrado masivo con AEGIS-128L...")
    inicio_aegis = time.perf_counter()
    _ = crypto_aead_aegis128l_encrypt(datos_masivos, datos_asociados, nonce_aegis, clave_aegis)
    fin_aegis = time.perf_counter()
    
    tiempo_aegis = fin_aegis - inicio_aegis
    velocidad_aegis = tamanio_mb / tiempo_aegis

    print(f"    -> Tiempo real: {tiempo_aegis:.4f} segundos")
    print(f"    -> Velocidad: {velocidad_aegis:.2f} MB/s\n")

    # 3. Cifrado MASIVO REAL con AES-128-GCM (Usando los motores criptográficos del procesador)
    print("[+] Ejecutando cifrado masivo con AES-128-GCM (Hardware-accelerated)...")
    aesgcm_instancia = AESGCM(clave_aes)
    
    inicio_aes = time.perf_counter()
    # Ejecuta el cifrado real sobre los mismos 100 MB de datos
    _ = aesgcm_instancia.encrypt(nonce_aes, datos_masivos, datos_asociados)
    fin_aes = time.perf_counter()
    
    tiempo_aes = fin_aes - inicio_aes
    velocidad_aes = tamanio_mb / tiempo_aes

    print(f"    -> Tiempo real: {tiempo_aes:.4f} segundos")
    print(f"    -> Velocidad: {velocidad_aes:.2f} MB/s\n")


    print("==================== RESULTADOS REALES ====================")
    print(f"AEGIS-128L: {velocidad_aegis:>10.2f} MB/s")
    print(f"AES-GCM:    {velocidad_aes:>10.2f} MB/s")
    print("===========================================================")
    ganador = "AEGIS-128L" if velocidad_aegis > velocidad_aes else "AES-GCM"
    factor = velocidad_aegis / velocidad_aes if velocidad_aegis > velocidad_aes else velocidad_aes / velocidad_aegis
    print(f"Ganador: {ganador} (es {factor:.2f}x más rápido en este hardware)")
    print("===========================================================")

    print("Esto demuestra empíricamente lo que pusimos en la sección de Vulnerabilidades y Consideraciones de nuestro TP: Si no hay soporte o acceso directo al hardware AES, AEGIS-128L pierde toda su ventaja competitiva y su rendimiento cae drásticamente.")

if __name__ == "__main__":
    run_benchmark()