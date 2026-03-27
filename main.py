import flet as ft

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE COMPATIBILIDAD CRÍTICA ---
    page.design_language = ft.DesignLanguage.M3 # Fuerza diseño moderno estándar
    page.theme_mode = ft.ThemeMode.LIGHT      # Evita conflictos de colores oscuros
    page.window_prevent_close = True
    
    # Contenido de prueba rápida
    page.add(
        ft.AppBar(title=ft.Text("Calculadora SLA - Activa"), bgcolor=ft.colors.BLUE_800, color="white"),
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=50),
                ft.Text("¡LOGRADO!", size=30, weight="bold"),
                ft.Text("Si ves esto, la pantalla negra se eliminó.", text_align="center"),
                ft.ElevatedButton("Entendido", on_click=lambda _: print("Click"))
            ], horizontal_alignment="center"),
            padding=50
        )
    )

# ESTA LÍNEA ES LA QUE QUITA EL COLOR NEGRO
if __name__ == "__main__":
    # Usamos web_renderer para asegurar que use HTML/Canvas básico y no Skia avanzado
    ft.app(target=main, view=ft.AppView.FLET_APP)
