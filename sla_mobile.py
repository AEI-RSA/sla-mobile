import pandas as pd
import re
from datetime import datetime, timedelta

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

SLA_TABLA = {1:6, 2:8, 3:10, 4:12, 5:24, 6:48, 7:96}

excel_path = "perimetro_mayo.xlsx"

def obtener_datos_site(site):
    df = pd.read_excel(PERIMETRO, header=None)
    site = site.strip().upper()

    for i in range(len(df)):
        if str(df.iloc[i,0]).strip().upper() == site:

            texto_cluster = str(df.iloc[i,11]).upper()
            match = re.search(r"\d+", texto_cluster)
            cluster = int(match.group()) if match else None

            return {
                "cluster": cluster,
                "departamento": df.iloc[i,1],
                "provincia": df.iloc[i,2],
                "distrito": df.iloc[i,3],
                "centro": df.iloc[i,4],
                "nodo": df.iloc[i,5],
                "latitud": df.iloc[i,9],
                "longitud": df.iloc[i,10],
                "concesionaria": df.iloc[i,34],
                "suministro": df.iloc[i,35]
            }
    return None

def extraer_datos(texto):
    partes = texto.strip().split("\t")
    return partes[0], partes[3], datetime.strptime(partes[-1], "%d/%m/%Y %I:%M %p")

class SLAApp(App):

    def build(self):
        self.title = "SLA Tickets Mobile"

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.entrada = TextInput(
            hint_text="Pega aquí la línea del ticket",
            size_hint_y=None,
            height=100
        )

        btn = Button(
            text="CALCULAR SLA",
            size_hint_y=None,
            height=60
        )
        btn.bind(on_press=self.calcular)

        self.resultado_label = Label(
            text="Resultado aparecerá aquí",
            size_hint_y=None,
            halign="left",
            valign="top"
        )
        self.resultado_label.bind(texture_size=self.resultado_label.setter('size'))

        scroll = ScrollView()
        scroll.add_widget(self.resultado_label)

        layout.add_widget(self.entrada)
        layout.add_widget(btn)
        layout.add_widget(scroll)

        return layout

    def calcular(self, instance):
        try:
            ticket, site, fecha = extraer_datos(self.entrada.text)
            info = obtener_datos_site(site)

            if not info:
                self.resultado_label.text = f"SITE {site} no encontrado"
                return

            cluster = info["cluster"]
            sla = SLA_TABLA[cluster]
            vence = fecha + timedelta(hours=sla)
            ahora = datetime.now()

            trans = (ahora - fecha).total_seconds()/3600
            rest = sla - trans
            estado = "EN TIEMPO" if rest > 0 else "VENCIDO"

            texto = f"""
TICKET: {ticket}
SITE: {site} | CLUSTER: {cluster} | SLA: {sla}h

UBICACIÓN
{info['departamento']} / {info['provincia']} / {info['distrito']}
Centro: {info['centro']}
Nodo: {info['nodo']}

ELÉCTRICO
Concesionaria: {info['concesionaria']}
Suministro: {info['suministro']}

COORDENADAS
Lat: {info['latitud']}
Lon: {info['longitud']}

TIEMPOS
Salida: {fecha.strftime('%d/%m/%Y %I:%M %p')}
Vence: {vence.strftime('%d/%m/%Y %I:%M %p')}
Transcurridas: {trans:.2f} h
Restantes: {rest:.2f} h

ESTADO: {estado}
"""
            self.resultado_label.text = texto

        except Exception as e:
            self.resultado_label.text = str(e)

if __name__ == "__main__":
    SLAApp().run()
