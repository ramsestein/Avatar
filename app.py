import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
from flask import Flask, render_template
import numpy as np
import datetime as dt

## Imagenes de ocupacion de las camas
box1 = box2 = box3 = box4 = box5 = box6 = box7 = box8 = box9 = box10 = 'freebed.png'

## Imagenes de soportes vitales
img_supp_brain = img_supp_lung = img_supp_heart = img_supp_liver = img_supp_kidney ='image001.png' #vacio

# Imagenes de organos
brain = 'greybrain.svg'
lung = 'greylung.svg'
heart = 'greyheart.svg'
liver = 'greyliver.svg'
kidney = 'greykidney.svg'

# Links activos para las camas
link1 = link2 = link3 = link4 = link5 = link6 = link7 = link8 = link9 = link10 ='/'

#Datos de seleccion
select_cama = 1

año_prev = 2022
mes_prev = 1
dia_prev = 2
hora_prev = 00
min_prev = 00
seg_prev = 00

año_post = 2022
mes_post = 1
dia_post = 5
hora_post = 23
min_post = 59
seg_post = 59

# Con un selector en pantalla se escogen los dias a trabajar, por defecto toma el valor de hoy
if (dia_post == 0 and dia_prev != 0):
    fecha_inicio = dt.datetime(año_prev,mes_prev,dia_prev)
    fecha_fin = dt.datetime.now()
elif (dia_post != 0 and dia_prev != 0):
    fecha_inicio = dt.datetime(año_prev,mes_prev,dia_prev)
    fecha_fin = dt.datetime(año_post,mes_post,dia_post)
else:
    fecha_inicio = dt.datetime.now()
    fecha_fin = dt.datetime.now()

## Importar la data
df = pd.read_csv('Pzero_dummies.csv', delimiter = ';',na_values=[""])

# Seleccionamos datos para la fecha a mostrar
# Primero definimos la columna que representa la fecha
df.fecha = pd.to_datetime(df.fecha)
########################################################################################
#Valores de gravedad de organo durante el tiempo determinado para el paciente determinado
########################################################################################
array_RASS = df.RASS.to_numpy()
array_TAM = df.TAM.to_numpy()
array_PaFi = df.PaFi.to_numpy()
array_Plq = df.Plq.to_numpy()
array_Cr = df.Cr.to_numpy()

#Incluimos la columna que define la gravedad del organo
#Aqui tocaría crear un nuevo array con los valores de gravedad conseguidos de un calculo a definir
#Por el momento igualamos a una variable

grave_brain = array_RASS
grave_heart = array_TAM
grave_lung = array_PaFi
grave_liver = array_Plq
grave_kidney = array_Cr

# Y los metemos dentro de la dataframe original
df.insert(df.shape[1], "grave_brain", grave_brain,True)
df.insert(df.shape[1], "grave_heart", grave_heart,True)
df.insert(df.shape[1], "grave_lung", grave_lung,True)
df.insert(df.shape[1], "grave_kidney", grave_kidney,True)
df.insert(df.shape[1], "grave_liver", grave_liver,True)

#######################################################################################
# Luego cogemos los valores entre la fecha inicio y fin
#df = df.loc[(df.fecha >= fecha_inicio) & (df.fecha <= fecha_fin)]
df_hoy = df[df.fecha == fecha_fin] 

# Seleccionamos datos del paciente en concreto y quitamos el extra de filas
datos_trabajo = df[df.paciente == select_cama]
datos_trabajo_hoy = df_hoy[df_hoy.paciente == select_cama]

#Ultima linea de datos
#tail_datos_trabajo_hoy = datos_trabajo_hoy.tail(n=1)
tail_datos_trabajo = datos_trabajo_hoy.tail(n=1)

################################################################################
#Definición de variables que modifican los colores de las pantallas del paciente
################################################################################

#Valor ultimo actualizado de los soportes
#Los valores NAN deben ser eliminados para poder realizar la media por no ser números
#Tomamos solo la columna que nos  interesa estudiar con todas sus filas
#Eliminamos los valores NAN, no convertimos en 0 porque romperian la media
#valorador = tail_datos_trabajo_hoy.loc[:,'NRL']
valorador = tail_datos_trabajo.loc[:,'NRL']
valorador = valorador.dropna()
value_NRL = valorador.mean()

#valorador = tail_datos_trabajo_hoy.loc[:,'CCV']
valorador = tail_datos_trabajo.loc[:,'NRL']
valorador = valorador.dropna()
value_CCV = valorador.mean()

#valorador = tail_datos_trabajo_hoy.loc[:,'RESP']
valorador = tail_datos_trabajo.loc[:,'RESP']
valorador = valorador.dropna()
value_RESP = valorador.mean()

#valorador = tail_datos_trabajo_hoy.loc[:,'RENAL']
valorador = tail_datos_trabajo.loc[:,'RENAL']
valorador = valorador.dropna()
value_RENAL = valorador.mean()

#valorador = tail_datos_trabajo_hoy.loc[:,'HEPT']
valorador = tail_datos_trabajo.loc[:,'HEPT']
valorador = valorador.dropna()
value_HEPT = valorador.mean()



#Valor medio de los soportes
#valorador = datos_trabajo_hoy.loc[:,'grave_brain']
valorador = datos_trabajo.loc[:,'grave_brain']
valorador = valorador.dropna()
mean_brain = valorador.mean()

#valorador = datos_trabajo_hoy.loc[:,'grave_heart']
valorador = datos_trabajo.loc[:,'grave_heart']
valorador = valorador.dropna()
mean_heart = valorador.mean()

#valorador = datos_trabajo_hoy.loc[:,'grave_lung']
valorador = datos_trabajo.loc[:,'grave_lung']
valorador = valorador.dropna()
mean_lung = valorador.mean()

#valorador = datos_trabajo_hoy.loc[:,'grave_kidney']
valorador = datos_trabajo.loc[:,'grave_kidney']
valorador = valorador.dropna()
#Como cogemos la Cr decimales con un punto, lo reconoce como string, quitamos el , para convertirlo en int
#ASUMIENDO SIEMPRE 2 DECIMALES
valorador = valorador.apply(lambda x: x.replace(',',''))
mean_kidney = valorador.mean()

#valorador = datos_trabajo_hoy.loc[:,'grave_liver']
valorador = datos_trabajo.loc[:,'grave_liver']
valorador = valorador.dropna()
mean_liver = valorador.mean()


#Vemos si los box tiene paciente en ella o no
cama1 = 1 in df.paciente.values
cama2 = 2 in df.paciente.values
cama3 = 3 in df.paciente.values
cama4 = 4 in df.paciente.values
cama5 = 5 in df.paciente.values
cama6 = 6 in df.paciente.values
cama7 = 7 in df.paciente.values
cama8 = 8 in df.paciente.values
cama9 = 9 in df.paciente.values
cama10 = 10 in df.paciente.values


##############################################################################
# Color de los organos en la pantalla resumen (Normas para definir la gravedad)
##############################################################################

#Cerebro
if (mean_brain >= 4 or mean_brain <= -4):
    brain = "redbrain.svg"
elif (mean_brain >= 3  or mean_brain <= -3):
    brain = "yellowbrain.svg"
else:
    brain = "greenbrain.svg"

#Corazon
if (mean_heart <= 55):
    heart = "redheart.svg"
elif (mean_heart <= 65 and mean_heart >= 56):
    heart = "yellowheart.svg"
elif (mean_heart >=66):
    heart = "greenheart.svg"

#Pulmon
if (mean_lung <= 200):
    lung = "redlung.svg"
elif (mean_lung <= 300 and mean_lung >= 201):
    lung = "yellowlung.svg"
elif (mean_lung >=301):
    lung = "greenlung.svg"

#Rinon
## CUIDADO. Le hemos quitado los puntos, hay que revisar que pille siempre un x100 o no, depende de como lea la base
if (mean_kidney <= 100):
    kidney = "greenkidney.svg"
elif (mean_kidney <= 170 and mean_kidney >= 101):
    kidney = "yellowkidney.svg"
elif (mean_kidney >= 171):
    kidney = "redkidney.svg"

#Higado
if (mean_liver <= 50000):
    liver = "redliver.svg"
elif (mean_liver <= 120000 and mean_liver >= 50001):
    liver = "yellowliver.svg"
elif (mean_liver >=120001):
    liver = "greenliver.svg"

###################################################################################
# Imagen de soporte aplicado en la pantalla resumen (Normas para definir el soporte)
###################################################################################

#Metemos las columnas en un array para trabajar con ellas para el diagrama de Gantt

#Valores de soporte durante el tiempo determinado para el paciente determinado
array_NRL = datos_trabajo.NRL.to_numpy()
array_CCV = datos_trabajo.CCV.to_numpy()
array_RESP = datos_trabajo.RESP.to_numpy()
array_HEPT = datos_trabajo.HEPT.to_numpy()
array_RENAL = datos_trabajo.RENAL.to_numpy()

#Cerebro
if (value_NRL >= 3):
    img_supp_brain = "image017.png" #perfusor
elif (value_NRL >= 2):
    img_supp_brain = "image011.png" # medicamentos

#Corazon
if (value_CCV >= 3):
    img_supp_heart = "image017.png" #perfusor
elif (value_CCV >= 2):
    img_supp_heart = "image011.png" # medicamentos

#Pulmon
if (value_RESP >= 4):
    img_supp_lung = "image005.png" #TET
elif (value_RESP >= 3):
    img_supp_lung = "image007.png" #VNI
elif (value_RESP >= 2):
    img_supp_lung = "image002.png" #LAF
elif (value_RESP >= 1):
    img_supp_lung = "image009.png" #LN

#Rinon
if (value_RENAL >= 4):
    img_supp_kidney = "image019.png" #Shalldon
elif (value_RENAL >= 3):
    img_supp_kidney = "image017.png" #perfusor
elif (value_RENAL >= 2):
    img_supp_kidney = "image011.png" #medicamentos

#Higado
if (value_HEPT >= 3):
    img_supp_liver = "image015.png" #jeringuilla
elif (value_HEPT >= 2):
    img_supp_liver = "image011.png" #medicamentos

#################################################################################

#Ocupacion de la cama para los pacientes de la uci y grado de soporte que necesitan
if (cama1 == True):
    link1 = "/resumen_1"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box1 = "busyred.png"
    else:
        box1 = "busygreen.png"
if (cama2 == True):
    link2 = "/resumen_2"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box2 = "busyred.png"
    else:
        box2 = "busygreen.png"
if (cama3 == True):
    link3 = "/resumen_3"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box3 = "busyred.png"
    else:
        box3 = "busygreen.png"
if (cama4 == True):
    link4 = "/resumen_4"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box4 = "busyred.png"
    else:
        box4 = "busygreen.png"
if (cama5 == True):
    link5 = "/resumen_5"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box5 = "busyred.png"
    else:
        box5 = "busygreen.png"
if (cama6 == True):
    link6 = "/resumen_6"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box6 = "busyred.png"
    else:
        box6 = "busygreen.png"
if (cama7 == True):
    link7 = "/resumen_7"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box7 = "busyred.png"
    else:
        box7 = "busygreen.png"
if (cama8 == True):
    link8 = "/resumen_8"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box8 = "busyred.png"
    else:
        box8 = "busygreen.png"
if (cama9 == True):
    link9 = "/resumen_9"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box9 = "busyred.png"
    else:
        box9 = "busygreen.png"
if (cama10 == True):
    link10 = "/resumen_10"
    if (value_NRL > 2 or value_CCV > 2 or value_RESP > 2 or value_RENAL > 2 or value_HEPT > 2):
        box10 = "busyred.png"
    else:
        box10 = "busygreen.png"


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
            html.A(html.Img(id='b1', src=app.get_asset_url(box1)), href=link1),
            html.A(html.Img(id='b2', src=app.get_asset_url(box2)), href=link2),
            html.A(html.Img(id='b3', src=app.get_asset_url(box3)), href=link3),
            html.A(html.Img(id='b4', src=app.get_asset_url(box4)), href=link4),
            html.A(html.Img(id='b5', src=app.get_asset_url(box5)), href=link5)
        ]),
    html.Div(id='div3',hidden=False,
        #style={''},
        children=[
            html.A(html.Img(id='b6', src=app.get_asset_url(box6)), href=link6),
            html.A(html.Img(id='b7', src=app.get_asset_url(box7)), href=link7),
            html.A(html.Img(id='b8', src=app.get_asset_url(box8)), href=link8),
            html.A(html.Img(id='b9', src=app.get_asset_url(box9)), href=link9),
            html.A(html.Img(id='b10', src=app.get_asset_url(box10)), href=link10)
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
            html.Img(id='supp_brain',src=app.get_asset_url(img_supp_brain)),
            html.Img(id='supp_lung',src=app.get_asset_url(img_supp_lung)),
            html.Img(id='supp_heart',src=app.get_asset_url(img_supp_heart)),
            html.Img(id='supp_liver',src=app.get_asset_url(img_supp_liver)),
            html.Img(id='supp_kidney',src=app.get_asset_url(img_supp_kidney))
        ]),
    html.Div(id='div5',hidden=False,
        #style={''},
        children=[
            html.Img(id='bed',src=app.get_asset_url('busy.jpeg'))
        ]),
    html.Div(id='div6',hidden=False,
        #style={''},
        children=[
        html.Img(id='brain',src=app.get_asset_url(brain)),
        html.Img(id='lung',src=app.get_asset_url(lung)),
        html.Img(id='heart',src=app.get_asset_url(heart)),
        html.Img(id='liver',src=app.get_asset_url(liver)),
        html.Img(id='kidney',src=app.get_asset_url(kidney))
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
