import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import flask

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

#Variables de movimiento entre paginas
select_cama = 0

## Importar la data
df = pd.read_csv('Pzero_dummies.csv', delimiter = ';',na_values=[""])

#Crear tablas dinámicas de trabajo
#pv = pd.pivot_table(df, index=['paciente'], columns=["NRL"], values=['Cr'], aggfunc=sum, fill_value=0)

app = dash.Dash()
 
app.layout = html.Div(
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
            html.Img(id='b1',n_clicks=0,src=app.get_asset_url(box1)),
            html.Img(id='b2',n_clicks=0,src=app.get_asset_url(box2)),
            html.Img(id='b3',n_clicks=0,src=app.get_asset_url(box3)),
            html.Img(id='b4',n_clicks=0,src=app.get_asset_url(box4)),
            html.Img(id='b5',n_clicks=0,src=app.get_asset_url(box5))
        ]),
    html.Div(id='div3',hidden=False,
        #style={''},
        children=[
            html.Img(id='b6',n_clicks=0,src=app.get_asset_url(box6)),
            html.Img(id='b7',n_clicks=0,src=app.get_asset_url(box7)),
            html.Img(id='b8',n_clicks=0,src=app.get_asset_url(box8)),
            html.Img(id='b9',n_clicks=0,src=app.get_asset_url(box9)),
            html.Img(id='b10',n_clicks=0,src=app.get_asset_url(box10))
        ]),
    #Divs de resumen de paciente, pantalla 2
    html.Div(id='div4',hidden=True,
        #style={''},
        children=[
            html.Img(id='supp_brain',src=app.get_asset_url(img_brain)),
            html.Img(id='supp_lung',src=app.get_asset_url(img_lung)),
            html.Img(id='supp_heart',src=app.get_asset_url(img_heart)),
            html.Img(id='supp_liver',src=app.get_asset_url(img_liver)),
            html.Img(id='supp_kidney',src=app.get_asset_url(img_kidney))
        ]),
    html.Div(id='div5',hidden=True,
        #style={''},
        children=[
            html.Img(id='bed',src=app.get_asset_url('busy.jpeg'))
        ]),
    html.Div(id='div6',hidden=True,
        #style={''},
        children=[
        html.Img(id='organos',src=app.get_asset_url('organos.svg'))
        ]),
    html.Div(id='div7',hidden=True,
        #style={''},
        children=[
        html.Button('Return',id='return',n_clicks=0)
        ])
    ])

#Llamada a servidor: Se aprieta sobre la cama 1
@app.callback(
    dash.dependencies.Output(component_id="div1",component_property="hidden"),
    dash.dependencies.Output(component_id="div2",component_property="hidden"),
    dash.dependencies.Output(component_id="div3",component_property="hidden"),
    dash.dependencies.Output(component_id="div4",component_property="hidden"),
    dash.dependencies.Output(component_id="div5",component_property="hidden"),
    dash.dependencies.Output(component_id="div6",component_property="hidden"),
    dash.dependencies.Output(component_id="div7",component_property="hidden"),
    [dash.dependencies.Input(component_id="b1",component_property="n_clicks")]
)

def select_cama1 (n_clicks):
    select_cama = 1
    return False, True, True, False, False, False, False
 

if __name__ == '__main__':
    app.run_server(debug=True)
