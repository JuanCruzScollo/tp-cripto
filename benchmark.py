import time
import os
# Primitiva de AEGIS-128L (vía Libsodium)
from nacl.bindings import crypto_aead_aegis128l_encrypt
from nacl.utils import random as nacl_random
#primtiva de ChaCha20-Poly1305 (vía cryptography)
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def run_benchmark():
    print("===========================================================")
    print("  BENCHMARK CRIPTOGRÁFICO: AEGIS-128L vs ChaCha20-Poly1305. ")
    print("===========================================================\n")

    # Texto corto de prueba para inspección visual
    texto_ejemplo = b"Mensaje secreto de ingenieria UTN FRBA"
    datos_asociados = b"Datos de cabecera de red (Texto Plano Autenticado)" 

    # Configurar Claves y Nonces reales para ambos algoritmos
    clave_aegis = nacl_random(16)
    nonce_aegis = nacl_random(16)

    clave_chacha = ChaCha20Poly1305.generate_key()
    nonce_chacha = os.urandom(12) # ChaCha20-Poly1305 usa un nonce de 12 bytes (96 bits)

    # Pre-cifrado de muestra para la inspección visual
    payload_aegis = crypto_aead_aegis128l_encrypt(texto_ejemplo, datos_asociados, nonce_aegis, clave_aegis)
    tag_aegis = payload_aegis[-16:]
    cifrado_puro_aegis = payload_aegis[:-16]


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

    # 3. Cifrado MASIVO REAL con ChaCha20
    print("[+] Ejecutando cifrado masivo con ChaCha20-Poly1305 (Software puro)...")
    chacha_instancia = ChaCha20Poly1305(clave_chacha)
    
    inicio_chacha = time.perf_counter()
    # Ejecuta el cifrado real sobre los mismos 100 MB de datos
    _ = chacha_instancia.encrypt(nonce_chacha, datos_masivos, datos_asociados)
    fin_chacha = time.perf_counter()
    
    tiempo_chacha = fin_chacha - inicio_chacha
    velocidad_chacha = tamanio_mb / tiempo_chacha

    print(f"    -> Tiempo real: {tiempo_chacha:.4f} segundos")
    print(f"    -> Velocidad: {velocidad_chacha:.2f} MB/s\n")


    print("==================== RESULTADOS REALES ====================")
    print(f"AEGIS-128L: {velocidad_aegis:>10.2f} MB/s")
    print(f"ChaCha20:    {velocidad_chacha:>10.2f} MB/s")
    print("===========================================================")
    ganador = "AEGIS-128L" if velocidad_aegis > velocidad_chacha else "ChaCha20"
    factor = velocidad_aegis / velocidad_chacha if velocidad_aegis > velocidad_chacha else velocidad_chacha / velocidad_aegis
    print(f"Ganador: {ganador} (es {factor:.2f}x más rápido en este hardware)")
    print("===========================================================")

if __name__ == "__main__":
    run_benchmark()