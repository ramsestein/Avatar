import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

## Importar la data
df = pd.read_csv('Pzero_dummies.csv', delimiter = ';')

#Crear una tabla dinámica
pv = pd.pivot_table(df, index=['paciente'], columns=["NRL"], values=['Cr'], aggfunc=sum, fill_value=0)

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hola Mundo'),
    html.Div(children='<p>Prueba proyecto AVATAR</p>')
])


if __name__ == '__main__':
    app.run_server(debug=True)
