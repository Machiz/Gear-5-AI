import os
import json
import shutil

# Cambia esto si tus rutas son distintas
LOGS_DIR = "assets/JSON/Battle_log"
DESTINO_VALIDOS = "logs_validos"

os.makedirs(DESTINO_VALIDOS, exist_ok=True)

def log_es_valido(log):
    estados_encontrados = {"Hand state": False, "Board state": False, "Life state": False, "Trash state": False}
    
    for key in sorted(log.keys()):
        paso = log[key]
        accion = paso.get("action", "")
        
        if accion == "Hand state" and "cards" in paso:
            estados_encontrados["Hand state"] = True
        elif accion == "Board state" and "cards" in paso:
            estados_encontrados["Board state"] = True
        elif accion == "Life state" and "life" in paso:
            estados_encontrados["Life state"] = True
        elif accion == "Trash state" and "cards" in paso:
            estados_encontrados["Trash state"] = True

        if all(estados_encontrados.values()):
            return True  # ✅ es válido
    
    return False  # ❌ incompleto

def filtrar_logs():
    archivos = [f for f in os.listdir(LOGS_DIR) if f.endswith(".json")]
    validos = 0
    total = len(archivos)

    for archivo in archivos:
        ruta = os.path.join(LOGS_DIR, archivo)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                log = json.load(f)
                if isinstance(log, dict) and log_es_valido(log):
                    shutil.copy(ruta, os.path.join(DESTINO_VALIDOS, archivo))
                    validos += 1
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")
    
    print(f"✅ Filtrado completo: {validos}/{total} logs válidos copiados a '{DESTINO_VALIDOS}'.")

if __name__ == "__main__":
    filtrar_logs()
