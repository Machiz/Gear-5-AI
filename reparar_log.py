import os
import json
import shutil

# 🛠 Configura rutas
CARPETA_ORIGEN = "assets/JSON/Battle_log"
CARPETA_SALIDA = "logs_reparados"
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# 📌 Requisitos mínimos para considerar un estado válido
ESTADOS_REQUERIDOS = {"Hand state", "Board state", "Trash state", "Life state"}

def es_log_valido(log):
    """
    Devuelve True si el log contiene al menos un conjunto completo de estado.
    """
    estados_encontrados = set()
    for key in sorted(log.keys()):
        paso = log[key]
        accion = paso.get("action", "")
        if accion in ESTADOS_REQUERIDOS:
            if accion == "Life state" and "life" in paso:
                estados_encontrados.add("Life state")
            elif accion in {"Hand state", "Board state", "Trash state"} and "cards" in paso:
                estados_encontrados.add(accion)

        if estados_encontrados == ESTADOS_REQUERIDOS:
            return True
    return False

def reparar_logs():
    archivos = [f for f in os.listdir(CARPETA_ORIGEN) if f.endswith(".json")]
    total = len(archivos)
    reparados = 0

    for nombre_archivo in archivos:
        ruta = os.path.join(CARPETA_ORIGEN, nombre_archivo)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict) and es_log_valido(data):
                shutil.copy(ruta, os.path.join(CARPETA_SALIDA, nombre_archivo))
                reparados += 1
            else:
                print(f"⚠️ Ignorado: {nombre_archivo} (incompleto o corrupto)")

        except Exception as e:
            print(f"❌ Error al leer {nombre_archivo}: {e}")

    print(f"\n✅ Reparación completa: {reparados}/{total} logs válidos copiados a '{CARPETA_SALIDA}'.")

if __name__ == "__main__":
    reparar_logs()
