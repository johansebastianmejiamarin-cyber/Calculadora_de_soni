import flet as ft
from datetime import datetime, timedelta, time
import holidays

# --- LÓGICA DE CÁLCULO (EL MOTOR) ---
def calcular_sla_detalle(inicio_dt, fin_dt, pais_code, h_ent, h_sal):
    minutos_totales = 0
    exclusiones = []
    años = list(range(inicio_dt.year, fin_dt.year + 1))
    festivos = holidays.country_holidays(pais_code, years=años)

    curr = inicio_dt.date()
    while curr <= fin_dt.date():
        # Identificar si es día no laboral
        es_finde = curr.weekday() >= 5
        es_festivo = curr in festivos
        
        if es_finde or es_festivo:
            motivo = "Fin de Semana" if es_finde else f"Festivo: {festivos.get(curr)}"
            exclusiones.append((curr.strftime("%d/%m/%Y"), motivo))
        else:
            # Calcular horas efectivas en este día
            dia_inicio = max(inicio_dt.time(), h_ent) if curr == inicio_dt.date() else h_ent
            dia_fin = min(fin_dt.time(), h_sal) if curr == fin_dt.date() else h_sal
            
            if dia_fin > dia_inicio:
                diff = datetime.combine(curr, dia_fin) - datetime.combine(curr, dia_inicio)
                minutos_totales += diff.total_seconds() / 60
        
        curr += timedelta(days=1)
    
    return round(minutos_totales, 2), exclusiones

# --- INTERFAZ GRÁFICA (LA APP) ---
def main(page: ft.Page):
    page.title = "SLA Global Expert"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "adaptive"

    # Inputs
    drop_pais = ft.Dropdown(
        label="País",
        value="CO",
        options=[
            ft.dropdown.Option("CO", "Colombia"),
            ft.dropdown.Option("MX", "México"),
            ft.dropdown.Option("ES", "España"),
            ft.dropdown.Option("AR", "Argentina"),
            ft.dropdown.Option("CL", "Chile"),
            ft.dropdown.Option("US", "Estados Unidos"),
            ft.dropdown.Option("BR", "Brasil"),
        ]
    )

    f_inicio = ft.TextField(label="Inicio (AAAA-MM-DD HH:MM)", value=datetime.now().strftime("%Y-%m-%d 08:00"))
    f_fin = ft.TextField(label="Fin (AAAA-MM-DD HH:MM)", value=datetime.now().strftime("%Y-%m-%d 17:00"))
    h_lab_i = ft.TextField(label="Entrada (HH:MM)", value="08:00", weight="bold")
    h_lab_f = ft.TextField(label="Salida (HH:MM)", value="17:00", weight="bold")

    # Outputs
    res_h = ft.Text("0.00 Horas", size=30, weight="bold", color="blue")
    res_m = ft.Text("0 Minutos", size=18, color="grey")
    
    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Fecha")), ft.DataColumn(ft.Text("Motivo"))],
        rows=[]
    )
    
    view_tabla = ft.Column([ft.Divider(), ft.Text("Días Excluidos:", weight="bold"), tabla], visible=False)

    def procesar(e):
        try:
            # Parsear datos
            inicio = datetime.strptime(f_inicio.value, "%Y-%m-%d %H:%M")
            fin = datetime.strptime(f_fin.value, "%Y-%m-%d %H:%M")
            ent = datetime.strptime(h_lab_i.value, "%H:%M").time()
            sal = datetime.strptime(h_lab_f.value, "%H:%M").time()

            # Calcular
            mins, exc = calcular_sla_detalle(inicio, fin, drop_pais.value, ent, sal)

            # Actualizar UI
            res_h.value = f"{mins/60:.2f} Horas"
            res_m.value = f"{int(mins)} Minutos"
            
            tabla.rows.clear()
            for fecha, motivo in exc:
                tabla.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(fecha)), ft.DataCell(ft.Text(motivo))]))
            
            view_tabla.visible = len(exc) > 0
            page.update()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text("Error: Revisa el formato de fecha/hora"))
            page.snack_bar.open = True
            page.update()

    # Layout Final
    page.add(
        ft.Text("Calculadora de SLA Laboral", size=24, weight="bold"),
        drop_pais,
        ft.Row([f_inicio, f_fin]),
        ft.Row([h_lab_i, h_lab_f]),
        ft.ElevatedButton("Calcular Tiempos", on_click=procesar, icon=ft.Icons.PLAY_ARROW, width=400),
        ft.Container(content=ft.Column([res_h, res_m], horizontal_alignment="center"), padding=20),
        view_tabla
    )

ft.app(target=main)
