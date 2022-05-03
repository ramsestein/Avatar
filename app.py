import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from flask import Flask, render_template

## Imagenes de ocupacion de las camas
box1 = 'busy.jpeg'
box2 = 'busy.jpeg'
box3 = 'busy.jpeg'
box4 = 'busy.jpeg'
box5 = 'busy.jpeg'
box6 = 'busy.jpeg'
box7 = 'busy.jpeg'
box8 = 'busy.jpeg'
box9 = 'busy.jpeg'
box10 = 'busy.jpeg'

## Imagenes de soportes vitales
img_brain = 'image001.png'
img_lung = 'image001.png'
img_heart = 'image001.png'
img_liver = 'image001.png'
img_kidney = 'image001.png'

select_cama = 0
#Variables de movimiento entre paginas

## Importar la data
df = pd.read_csv('Pzero_dummies.csv', delimiter = ';',na_values=[""])

#Crear tablas dinamicas de trabajo
#pv = pd.pivot_table(df, index=['paciente'], columns=["NRL"], values=['Cr'], aggfunc=sum, fill_value=0)

app = dash.Dash(__name__, suppress_callback_exceptions=True)
 
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#html pagina de inicio
inicio = html.Div(
    style={'background-color': 'rgba(208,228,245,0.78)','background-repeat': 'repeat','background-attachment': 'scroll','background-position': '0px 0px'},
    children=[
    #Div del cabecero
    html.Div(id='div1',hidden=False,
        #style={''},
        children=[
            html.H1('UCIQ - E043')
        ]),
    #Divs del selector de camas de la UCI, pantalla 1
    html.Div(id='div2',hidden=False,
        #style={''},
        children=[
            html.A(html.Img(id='b1', src=app.get_asset_url(box1)), href='/resumen_1'),
            html.A(html.Img(id='b2', src=app.get_asset_url(box2)), href='/resumen_2'),
            html.A(html.Img(id='b3', src=app.get_asset_url(box3)), href='/resumen_3'),
            html.A(html.Img(id='b4', src=app.get_asset_url(box4)), href='/resumen_4'),
            html.A(html.Img(id='b5', src=app.get_asset_url(box5)), href='/resumen_5')
        ]),
    html.Div(id='div3',hidden=False,
        #style={''},
        children=[
            html.A(html.Img(id='b6', src=app.get_asset_url(box6)), href='/resumen_6'),
            html.A(html.Img(id='b7', src=app.get_asset_url(box7)), href='/resumen_7'),
            html.A(html.Img(id='b8', src=app.get_asset_url(box8)), href='/resumen_8'),
            html.A(html.Img(id='b9', src=app.get_asset_url(box9)), href='/resumen_9'),
            html.A(html.Img(id='b10', src=app.get_asset_url(box10)), href='/resumen_10')
        ])
    ])

#html pagina de resumen para paciente
resumen = html.Div(
    style={'background-color': 'rgba(208,228,245,0.78)','background-repeat': 'repeat','background-attachment': 'scroll','background-position': '0px 0px'},
    children=[
    #Div del cabecero
    html.Div(id='div1',hidden=False,
        #style={''},
        children=[
            html.H1('UCIQ - E043')
        ]),
    #Divs de resumen de paciente, pantalla 2
    html.Div(id='div4',hidden=False,
        #style={''},
        children=[
            html.Img(id='supp_brain',src=app.get_asset_url(img_brain)),
            html.Img(id='supp_lung',src=app.get_asset_url(img_lung)),
            html.Img(id='supp_heart',src=app.get_asset_url(img_heart)),
            html.Img(id='supp_liver',src=app.get_asset_url(img_liver)),
            html.Img(id='supp_kidney',src=app.get_asset_url(img_kidney))
        ]),
    html.Div(id='div5',hidden=False,
        #style={''},
        children=[
            html.Img(id='bed',src=app.get_asset_url('busy.jpeg'))
        ]),
    html.Div(id='div6',hidden=False,
        #style={''},
        children=[
        html.Img(id='organos',src=app.get_asset_url('organos.svg'))
        ]),
    html.Div(id='div7',hidden=False,
        #style={''},
        children=[
        html.A(html.Button('Return',id='return',n_clicks=0), href='/')
        ])
    ])


#callback para cambio de paginas
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def display_page (pathname):
    if (pathname == '/resumen_1'):
        select_cama = 1
        return resumen
    elif (pathname == '/resumen_2'):
        select_cama = 2
        return resumen
    elif (pathname == '/resumen_3'):
        select_cama = 3
        return resumen
    elif (pathname == '/resumen_4'):
        select_cama = 4
        return resumen
    elif (pathname == '/resumen_5'):
        select_cama = 5
        return resumen
    elif (pathname == '/resumen_6'):
        select_cama = 6
        return resumen
    elif (pathname == '/resumen_7'):
        select_cama = 7
        return resumen
    elif (pathname == '/resumen_8'):
        select_cama = 8
        return resumen
    elif (pathname == '/resumen_9'):
        select_cama = 9
        return resumen
    elif (pathname == '/resumen_10'):
        select_cama = 10
        return resumen
    else:
        select_cama = 0
        return inicio

if __name__ == '__main__':
    app.run_server(debug=True)
