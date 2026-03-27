import flet as ft
from datetime import datetime, timedelta, time
import holidays

# Función de cálculo movida dentro para asegurar alcance
def calcular_sla_motor(inicio_dt, fin_dt, pais_code, h_ent, h_sal):
    minutos_totales = 0
    exclusiones = []
    try:
        años = [inicio_dt.year, fin_dt.year]
        festivos = holidays.country_holidays(pais_code, years=años)
    except:
        festivos = {} # Evita que la app se cierre si falla la carga de festivos

    curr = inicio_dt.date()
    while curr <= fin_dt.date():
        es_finde = curr.weekday() >= 5
        es_festivo = curr in festivos
        if es_finde or es_festivo:
            motivo = "Fin de Semana" if es_finde else f"Festivo: {festivos.get(curr)}"
            exclusiones.append((curr.strftime("%d/%m/%Y"), motivo))
        else:
            dia_inicio = max(inicio_dt.time(), h_ent) if curr == inicio_dt.date() else h_ent
            dia_fin = min(fin_dt.time(), h_sal) if curr == fin_dt.date() else h_sal
            if dia_fin > dia_inicio:
                diff = datetime.combine(curr, dia_fin) - datetime.combine(curr, dia_inicio)
                minutos_totales += diff.total_seconds() / 60
        curr += timedelta(days=1)
    return round(minutos_totales, 2), exclusiones

def main(page: ft.Page):
    # Esto fuerza a la app a renderizar correctamente en Android
    page.adaptive = True 
    page.title = "SLA Global Expert"
    
    # --- Interfaz simplificada para asegurar carga ---
    txt_h = ft.Text("0.00 h", size=30, weight="bold")
    
    def on_click_calc(e):
        # Aquí iría la lógica de captura de datos (puedes usar la anterior)
        # Por ahora, solo para probar que no sale en blanco:
        txt_h.value = "Calculando..."
        page.update()

    page.add(
        ft.AppBar(title=ft.Text("Calculadora SLA"), bgcolor=ft.colors.AMBER),
        ft.Column([
            ft.Text("Si ves esto, la app cargó correctamente", color="green"),
            txt_h,
            ft.ElevatedButton("Probar", on_click=on_click_calc)
        ], horizontal_alignment="center")
    )

# ESTA LÍNEA ES VITAL PARA ANDROID
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
