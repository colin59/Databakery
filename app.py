# Import libs
import dash
import base64
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize
from text_content import *

# region style definition
# Apply custom format to map figures


def formatMap(fignb):
    # Define margin for figure layout so the chart can fill as much space as possible
    fignb.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    # Define dims for layout
    fignb.layout.width = 800
    fignb.layout.height = 500

    # Set orientation of the modebar
    fignb.layout.modebar.orientation = 'h'

    # Set the colorbar to the left side of the cart
    #fignb.layout.coloraxis.colorbar.len = 0.8
    fignb.layout.coloraxis.colorbar.x = -0.2
    fignb.layout.coloraxis.colorbar.xanchor = 'left'

    # Set the position of updatemenus (play and stop buttons)
    # One above the other (direction = 'up')
    # Last config allow to set the duration of animation
    fignb.layout.updatemenus[0]['pad'] = {'t': -0.4}
    #fignb.layout.updatemenus[0].direction = 'up'
    fignb.layout.updatemenus[0].x = -0.18
    fignb.layout.updatemenus[0].xanchor = 'left'
    fignb.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2

    # Set the slider near the chart
    # fignb.layout.sliders[0]['pad']={'t':-0.3}
    fignb.layout.sliders[0]['pad'] = {'t': -0.2}
    fignb.layout.sliders[0]['y'] = 0.08
    fignb.layout.sliders[0]['len'] = 1
    fignb.layout.sliders[0].x = 0

# Apply custom format to scatter figures


def formatScatter(fignb):
     # Define margin for figure layout so the chart can fill as much space as possible
    fignb.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend=dict(
        yanchor="top", y=0.99, xanchor="left", x=0.01))
    # Define dims for layout
    fignb.layout.width = 800
    fignb.layout.height = 500


# Getting the color specifications and intervals for the different GHG:
rangecolor_co2 = getColorPal('YlOrRd', 0, 9)
rangecolor_ghg = getColorPal('YlOrBr', 1, 8)
rangecolor_meth = getColorPal('Reds', 1, 6)
rangecolor_no = getColorPal('OrRd', 2, 5)

# The style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '2%',
    # 'margin-left': '5%',
    'margin-right': '2%',
    'padding': '10px 5px 15px 20px'
}

# The style for the text
TEXT_STYLE = {
    'textAlign': 'left',
    'color': '#191970'
}
# endregion

# region dataframes & ML
df_ultimate_df = pd.read_csv("ultimate_df.csv")


def get_location(df, dict_d):
    # Filtering the df on price m2
    filtered_df = df[df['Prix du m2 bâti'] <= dict_d['prix_m2']]
    if filtered_df.shape[0] < 5000:
        return('Désolé, il va falloir revoir vos critères prix et/ou superficie')
    else:
        features_col = [key for key, value in dict_d.items() if value != 0]
        features_col.remove('prix_m2')
        list_input = [value for key, value in dict_d.items() if value != 0]
        # Define X:
        X = filtered_df[features_col]
        # Transform X
        scaler = MinMaxScaler().fit(X)
        X_scaled = scaler.transform(X)
        # Fit NN:
        nbrs = NearestNeighbors(
            n_neighbors=5000, algorithm='ball_tree').fit(X_scaled)
        distances, indices = nbrs.kneighbors([list_input[:-1]])
        return distances, indices


dict_dist = {'dist_maternelle': 0.000001, 'dist_primaire': 0.000001, 'dist_college': 0.000001,
             'dist_lycee': 0.000001, 'dist_hopital': 0.000001,
             'dist_bus': 0.000001, 'dist_magasins': 0.000001, 'prix_m2': 2001}
# def get_location(df, primaire, maternelle, college, lycee, hopital, bus, magasins, prix_m2):
#   # Filtering the df on price m2
#   filtered_df = df[df['Prix du m2 bâti'] <= prix_m2]
#   if filtered_df.shape[0] < 2000:
#     return('Désolé, il va falloir revoir vos critères prix et/ou superficie')
#   else:
#     features_col = ['dist_primaire', 'dist_maternelle', 'dist_college', 'dist_lycee', 'dist_hopital', 'dist_bus', 'dist_magasins']
#     list_input = [primaire, maternelle, college, lycee, hopital, bus, magasins]
#     # Define X:
#     X = filtered_df[features_col]
#     # Transform X
#     scaler = MinMaxScaler().fit(X)
#     X_scaled = scaler.transform(X)
#     # Fit NN:
#     nbrs = NearestNeighbors(n_neighbors=2000, algorithm='ball_tree').fit(X_scaled)
#     distances, indices = nbrs.kneighbors([list_input])
#     #nn = nbrs.kneighbors([list_input], 5, return_distance=False)
#     return distances, indices

# endregion


# region figure definitions
test = get_location(df_ultimate_df, dict_dist)
for i in reversed(test[1]):
    for j in reversed(test[0]):
        fig = px.scatter_mapbox(
            df_ultimate_df.loc[i], lat="lat",  lon="long", color=j, width=1500,height=700, zoom=10, opacity=0.3)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={'r':1, 't':0, 'l':0, 'b':0})
fig.update_coloraxes(colorbar_tickmode='array')
fig.update_coloraxes(colorbar_tickvals=[test[0].min(),test[0].max()])
fig.update_coloraxes(colorbar_title_text="Compatibilité")
fig.update_coloraxes(colorbar_ticktext=['100 %','0 %'])

# endregion


# region main
main_title = dbc.Row(children=[
    dbc.Col(align='left',width='auto',children=[
        html.H1('Data Where House (à Lille!)'),html.H6('by the team Data Bakery')]
        ,md=5),
        dbc.Col(width='auto',children=[
        ]
        ,md=7)
        ])

interest_title = html.Div(
    html.H5("Vos centres d'intérêt")
)


interest_menu = dbc.Row(align='left',children=[
    dbc.Col(children=[
        html.Div([
            html.Label('École maternelle'),
            dcc.Dropdown(
                id='ecole_maternelle_dd',
                options=[
                 {'label': 'Pas important', 'value': 0},
                 {'label': 'Moins de 500 m', 'value': 500/10000},
                 {'label': 'Moins de 1 km', 'value': 1000/10000},
                 {'label': 'Moins de 5 km', 'value': 5000/10000},
                 {'label': 'Moins de 10 km', 'value': 10000/10000},
                 ],
                value=0
            ),
            html.Label('École primaire'),
            dcc.Dropdown(
                id='ecole_primaire_dd',
                options=[
                    {'label': 'Pas important', 'value': 0/5000},
                    {'label': 'Moins de 500 m', 'value': 500/5000},
                    {'label': 'Moins de 1 km', 'value': 1000/5000},
                    {'label': 'Moins de 5 km', 'value': 5000/5000},
                ],
                value=0
            ),
            html.Label('Collège'),
            dcc.Dropdown(
                id='college_dd',
                options=[
                    {'label': 'Pas important', 'value': 0/10000},
                    {'label': 'Moins de 500 m', 'value': 500/10000},
                    {'label': 'Moins de 1 km', 'value': 1000/10000},
                    {'label': 'Moins de 5 km', 'value': 5000/10000},
                    {'label': 'Moins de 10 km', 'value': 10000/10000},
                ],
                value=0
            ),
            html.Label('Lycée'),
            dcc.Dropdown(
                id='lycee_dd',
                options=[
                    {'label': 'Pas important', 'value': 0/10000},
                    {'label': 'Moins de 500 m', 'value': 500/10000},
                    {'label': 'Moins de 1 km', 'value': 1000/10000},
                    {'label': 'Moins de 5 km', 'value': 5000/10000},
                    {'label': 'Moins de 10 km', 'value': 10000/10000},
                ],
                value=0
            ),
            html.Label('Hopitaux (CHR)'),
            dcc.Dropdown(
                id='chr_dd',
                options=[
                    {'label': 'Pas important', 'value': 0/20000},
                    {'label': 'Moins de 500 m', 'value': 500/20000},
                    {'label': 'Moins de 1 km', 'value': 1000/20000},
                    {'label': 'Moins de 5 km', 'value': 5000/20000},
                    {'label': 'Moins de 10 km', 'value': 10000/20000},
                    {'label': 'Moins de 10 km', 'value': 20000/20000},
                ],
                value=0
            ),
            html.Label('Grande surfaces'),
            dcc.Dropdown(
                id='gs_dd',
                options=[
                    {'label': 'Pas important', 'value': 0},
                    {'label': 'Moins de 500 m', 'value': 500/10000},
                    {'label': 'Moins de 1 km', 'value': 1000/10000},
                    {'label': 'Moins de 5 km', 'value': 5000/10000},
                    {'label': 'Moins de 10 km', 'value': 10000/10000},
                ],
                value=0
            ),
            html.Label('Transport en commun'),
            dcc.Dropdown(
                id='transport_dd',
                options=[
                    {'label': 'Pas important', 'value': 0/2000},
                    {'label': 'Moins de 500 m', 'value': 500/2000},
                    {'label': 'Moins de 1 km', 'value': 1000/2000},
                    {'label': 'Moins de 2 km', 'value': 2000/2000},
                ],
                value=0
            ),
            html.Div('Budget (prix au m²)'),
           # dbc.Row(justify='left',align='center',children=[
            dcc.Input(
                style= {'margin-top': 10},
                size='4',
                id="budget",
                type="number",
                placeholder="Prix au m²")
            #)])
        ])
],md=2),
dbc.Col([
        dcc.Graph(id='graph_map',
                  config={
                      'displayModeBar': False
                  },
                  figure=fig
                  ),
        html.Button("Update",id='button_val')

],md=10)
])

map_and_insights = dbc.Row(children=[
    # dbc.Col(id='map', width="auto", children=[
    #     dcc.Graph(id='graph_map',
    #               config={
    #                   'displayModeBar': False
    #               },
    #               figure=fig
    #               )
    # ]),
    dbc.Col(id='insights', width="auto", children=[
        html.Div(id='dict1', style={'display': 'none'}),
        html.Div(id='dict2', style={'display': 'none'}),
        html.Div(id='dict3', style={'display': 'none'}),
        html.Div(id='dict4', style={'display': 'none'}),
        html.Div(id='dict5', style={'display': 'none'}),
        html.Div(id='dict6', style={'display': 'none'}),
        html.Div(id='dict7', style={'display': 'none'}),
        html.Div(id='dict8', style={'display': 'none'}),
    ]
    )])
# endregion

# Main content
content = html.Div(
    [
        main_title,
        html.Hr(),
        html.Br(),
        interest_title,
        interest_menu,
        html.Br(),
        map_and_insights
    ],
    style=CONTENT_STYLE
)
# endregion

# use bootstrap stylesheet
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# define page layout, which contains sidebar and content
app.layout = html.Div([content],style={
'background-image': 'url("/assets/back2.jpg")',
'background-repeat': 'no-repeat',
'background-position': 'right top',
'background-size': '150px 100px'})
# region callbacks


@app.callback(
    Output('dict1', 'value'),
    [Input('ecole_maternelle_dd', 'value')])
def update_var_maternelle(col_value):
    dict_dist['dist_maternelle'] = col_value


@app.callback(
    Output('dict2', 'value'),
    [Input('ecole_primaire_dd', 'value')]
)
def update_var_primaire(col_value):
    dict_dist['dist_primaire'] = col_value


@app.callback(
    Output('dict3', 'value'),
    [Input('college_dd', 'value')]
)
def update_var_college(col_value):
    dict_dist['dist_college'] = col_value


@app.callback(
    Output('dict4', 'value'),
    [Input('lycee_dd', 'value')])
def update_var_lycee(col_value):
    dict_dist['dist_lycee'] = col_value


@app.callback(
    Output('dict5', 'value'),
    [Input('chr_dd', 'value')])
def update_var_hopital(col_value):
    dict_dist['dist_hopital'] = col_value


@app.callback(
    Output('dict6', 'value'),
    [Input('gs_dd', 'value')])
def update_var_magasin(col_value):
    dict_dist['dist_magasins'] = col_value


@app.callback(
    Output('dict7', 'value'),
    [Input('transport_dd', 'value')])
def update_var_bus(col_value):
    dict_dist['dist_bus'] = col_value


@app.callback(
    Output('dict8', 'value'),
    [Input('budget', 'value')])
def update_var_budget(col_value):
    dict_dist['prix_m2'] = col_value


# Validation button
@app.callback(
    Output('graph_map', 'figure'),
    [Input('button_val', 'n_clicks')]
)
def update_graph(n_clicks):
    test = get_location(df_ultimate_df, dict_dist)
    for i in reversed(test[1]):
        for j in reversed(test[0]):
            fig = px.scatter_mapbox(
                df_ultimate_df.loc[i], lat="lat",  lon="long",color=j, size_max=10,width=1500,height=700, zoom=10, opacity=0.3)
    fig.update_layout()
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={'r':1, 't':0, 'l':0, 'b':0})
    fig.update_coloraxes(colorbar_tickmode='array')
    fig.update_coloraxes(colorbar_tickvals=[0,1])
    fig.update_coloraxes(colorbar_title_text="Compatibilité")
    fig.update_coloraxes(colorbar_ticktext=['100 %','0 %'])
    # fig.update_coloraxes(colorbar_xpad=0)
    # fig.update_coloraxes(colorbar_x=1)
    return fig

# Validation button
@app.callback(
    Output('dict', 'value'),
    [Input('button_val', 'value')])
def print_dict(col_value):
    return str(dict_dist.items())


# endregion
# Run the server at port 8085
# Accessible through : http://localhost:8085
if __name__ == '__main__':
    app.run_server(port='8085')
