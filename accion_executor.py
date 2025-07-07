# accion_executor.py
import pyautogui

def ejecutar_accion(accion):
    tipo = accion["tipo"]

    if tipo == "atacar":
        print(f"Atacando con {accion['atacante']} a {accion['objetivo']}")
        # Ejemplo de clics simulados
        pyautogui.click(accion['coords_atacante'])  # coord x, y
        pyautogui.click(accion['coords_objetivo'])

    elif tipo == "invocar":
        print(f"Invocando {accion['carta']}")
        pyautogui.click(accion['coords'])  # coord carta en mano

    elif tipo == "pasar_turno":
        print("Pasando turno")
        pyautogui.press("enter")

    else:
        print(f"Acción no definida: {tipo}")
