#Import libs
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from text_content import * 

#region style definition
#Apply custom format to map figures
def formatMap(fignb):
    #Define margin for figure layout so the chart can fill as much space as possible
    fignb.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    #Define dims for layout
    fignb.layout.width=800
    fignb.layout.height=500

    #Set orientation of the modebar 
    fignb.layout.modebar.orientation='h'

    #Set the colorbar to the left side of the cart
    #fignb.layout.coloraxis.colorbar.len = 0.8
    fignb.layout.coloraxis.colorbar.x = -0.2
    fignb.layout.coloraxis.colorbar.xanchor = 'left'

    #Set the position of updatemenus (play and stop buttons) 
    #One above the other (direction = 'up')
    #Last config allow to set the duration of animation
    fignb.layout.updatemenus[0]['pad']={'t':-0.4}
    #fignb.layout.updatemenus[0].direction = 'up'
    fignb.layout.updatemenus[0].x = -0.18
    fignb.layout.updatemenus[0].xanchor = 'left'
    fignb.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2

    #Set the slider near the chart 
    #fignb.layout.sliders[0]['pad']={'t':-0.3}
    fignb.layout.sliders[0]['pad']={'t':-0.2}
    fignb.layout.sliders[0]['y'] = 0.08
    fignb.layout.sliders[0]['len']= 1
    fignb.layout.sliders[0].x = 0

#Apply custom format to scatter figures
def formatScatter(fignb):
     #Define margin for figure layout so the chart can fill as much space as possible
    fignb.update_layout(margin=dict(l=0, r=0, t=0, b=0),legend=dict(yanchor="top",y=0.99, xanchor="left",x=0.01))
    #Define dims for layout
    fignb.layout.width=800
    fignb.layout.height=500

# Getting the color specifications and intervals for the different GHG:
rangecolor_co2 = getColorPal('YlOrRd', 0, 9)
rangecolor_ghg = getColorPal('YlOrBr', 1, 8)
rangecolor_meth = getColorPal('Reds', 1, 6)
rangecolor_no = getColorPal('OrRd', 2, 5)

#The style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '15%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

#The style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '18%',
    #'margin-left': '5%',
    'margin-right': '5%',
    'padding' : '10px 5px 15px 20px'
}

#The style for the text 
TEXT_STYLE = {
    'textAlign': 'left',
    'color': '#191970'
}
#endregion

#region dataframes

#Import ultimate_df dataframe 
ultimate_df = pd.read_csv('ultimate_df.csv')
#Import paleo_df dataframe
paleo_df=pd.read_csv('paleodf.csv',parse_dates=True)
#Import covid_df
Covid_df = pd.read_csv('confinementC02variation.csv')
Covid_df['CO2_variation'] = Covid_df['CO2_variation'].apply(lambda x : x.replace('%','')) 
Covid_df['CO2_variation'] = Covid_df['CO2_variation'].apply(lambda x : x.replace(',','.')) 
Covid_df['CO2_variation'] = Covid_df['CO2_variation'].astype('float64')
#Import Predicted Future Temperatures:
predictions_df = pd.read_csv('Future_temperature_predictions.csv')

#endregion

#region figure definitions 

#region figure 1
# Slicing the df to select only the World values:
world_df = ultimate_df.loc[ultimate_df['Country'] == 'World']

# Code for the Figure:
fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=world_df.Year, y=np.zeros(len(world_df.Year)),
                    mode='lines',
                    name='1961- 1990 mean',
                    line=dict(color="#000000")))
fig1.add_trace(go.Scatter(x=world_df.Year, y=world_df.temperature_variations,
                    mode='markers',
                    name='Global temperature (rolling mean)',
                    marker={'color':world_df.temperature_variations, 'colorscale':px.colors.cyclical.IceFire, 'size':13, 'cmid':0, 'cmin':-2, 'cmax':2},
                    hovertemplate="Year : %{x}<br>Variation : %{y}"))
fig1.update_layout(#title='Global temperature : Deviation from the mean',
                   xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)',
                   )
fig1.update_yaxes(range=[-1, 1])

formatScatter(fig1)
#endregion

#region figure 2
# Generating the chloropleth Worldwide Map for Temperature variations by Year and By Country
fig2 = px.choropleth(ultimate_df[ultimate_df['Year']<2014], 
                    locations="Code", 
                    color="temperature_variations", 
                    hover_name="Country", 
                    color_continuous_scale=px.colors.cyclical.IceFire, 
                    color_continuous_midpoint=0, 
                    animation_frame="Year", 
                    range_color=[-2,2] 
                    #title='Worldwide temperatures variations'
                    )
fig2.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title="Temperature Variation"))

formatMap(fig2)
#endregion 

#region figure 3a
# Plotting temperature variations from 0 to nowdays:
df_recent = paleo_df[paleo_df.Start>0]

#pour utiliser les variations de l'utimate df, je calcule la valeur du premier point : la dernière valeur de df paleo - la premieère variation contemporaine
premierpoint=df_recent.loc[df_recent.index.max(), "Temperature"]-world_df.loc[world_df.index.min(), "temperature_variations"]
premierpoint
# Plotting Global temperature from -21ka to 1850:
fig3a = go.Figure()

fig3a.add_trace(go.Scatter(x=paleo_df.End, y=paleo_df.Temperature,
                    mode='markers',
                    name='Global land temperature (TraCE-21ka simulation)',
                    marker={'color':'grey', 'size':6, 'cmid':0, 'cmin':-2, 'cmax':10},
                    hovertemplate="Year : %{x}<br>Temp : %{y}"))
fig3a.add_trace(go.Scatter(x=world_df.Year, y=world_df.temperature_variations+premierpoint,
                    mode='markers',
                    name='Global land temperature (Berkeley Earth)',
                    marker={'color':world_df.temperature_variations+premierpoint, 'colorscale':px.colors.cyclical.IceFire, 'size':6, 'cmid':0, 'cmin':-2, 'cmax':10},
                    hovertemplate="Year : %{x}<br>Temp : %{y}"))
fig3a.update_layout(#title='Global temperature since -19 000 (TraCE-21ka simulation)',
                   xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)',
                   )
formatScatter(fig3a)
fig3a.layout.width=700
fig3a.layout.height=400
fig3a.layout.modebar.orientation='v'
#endregion

#region figure 3b
# Plotting temperature variations from 0 to nowdays:
#df_recent = paleo_df[paleo_df.Start>0]

#pour utiliser les variations de l'utimate df, je calcule la valeur du premier point : la dernière valeur de df paleo - la premieère variation contemporaine
#premierpoint=df_recent.loc[df_recent.index.max(), "Temperature"]-world_df.loc[world_df.index.min(), "temperature_variations"]
#premierpoint

fig3b = go.Figure()



fig3b.add_trace(go.Scatter(x=df_recent.End, y=df_recent.Temperature,
                    mode='markers',
                    name='Global land temperature (TraCE-21ka simulation)',
                    marker={'color':"grey"},
                    hovertemplate="Year : %{x}<br>Temp : %{y}"))

fig3b.add_trace(go.Scatter(x=world_df.Year, y=world_df.temperature_variations+premierpoint,
                    mode='markers',
                    name='Global land temperature (Berkeley Earth)',
                    marker={'color':"red", 'cmid':8, 'cmin':6, 'cmax':10},
                    hovertemplate="Year : %{x}<br>Temp : %{y}"))

fig3b.update_layout(#title='Global temperature since JC',
                   xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)',
                   )

formatScatter(fig3b)
fig3b.layout.width=700
fig3b.layout.height=400
fig3b.layout.modebar.orientation='v'
#endregion

#region figure 4
df_solar = ultimate_df[ultimate_df["Code"]=="OWID_WRL"][["Year", "temperature_values", "temperature_variations", "Solar_irradiation"]]

#je crée une colonne de variation de l'activité solaire, et je la calcule par rapport à la période de référence 1960-1991, comme pour les températures, en lissant la moyenne sur 10ans
df_solar["solar_variation"]=0
solar_mean=df_solar[df_solar.Year.between(1961,1990)]["Solar_irradiation"].mean()
for i in range(len(df_solar.Solar_irradiation)):
  df_solar.loc[i, "solar_variation"]=df_solar.loc[i, "Solar_irradiation"]-solar_mean

df_solar.solar_variation=df_solar.solar_variation.rolling(10).mean()

#Go pour le graphique
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4.add_trace(go.Scatter(x=df_solar.Year, y=df_solar.temperature_variations,
                    mode='markers',
                    name='Global temperature variation (rolling mean)',
                    marker={'color':df_solar.temperature_variations, 'colorscale':px.colors.cyclical.IceFire, 'size':13, 'cmid':0, 'cmin':-2, 'cmax':2}
                    ),secondary_y=False)
fig4.add_trace(go.Scatter(x=df_solar.Year, y=df_solar["solar_variation"],
                    mode='markers',
                    name='Solar irradiation variation (rolling mean)',
                    marker={'color':'rgb(166,54,3)', 'colorscale':px.colors.sequential.Oranges, 'size':7, 'cmid':0, 'cmin':-1, 'cmax':0.5}
                    ),secondary_y=True)

fig4.update_layout(#title='Temperature variations compared to solar activity variation (deviation from period 1961-1990)',
                   xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                    plot_bgcolor='rgba(0,0,0,0.05)')
fig4.update_yaxes(title_text="Temperature (degrees C)", secondary_y=False)
fig4.update_yaxes(title_text="Solar irradiation (W/m2)", secondary_y=True)
fig4.update_yaxes(range=[-1, 1])
formatScatter(fig4)
#endregion

#region figure 5
# Line plot for global greenhouse gas emissions (using world_df)
world_1990_df = world_df[world_df['Year']>1989]

fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=world_1990_df['Year'], y=world_1990_df['Annual CO2 emissions'],
    mode='lines',
    name='Carbon Dioxide',
    text='Carbon Dioxide',
    #hoverinfo='text+Year+Annual CO2 emissions',
    line=dict(color='rgb(252,78,42)'),
    stackgroup='one'
))
fig5.add_trace(go.Scatter(
    x=world_1990_df['Year'], y=world_1990_df['Methane'],
    mode='lines',
    name='Methane',
    text='Methane',
    line=dict(color='rgb(165,15,21)'),
    stackgroup='one'
))
fig5.add_trace(go.Scatter(
    x=world_1990_df['Year'], y=world_1990_df['Nitrous_oxide'],
    mode='lines',
    name='Nitrous Oxide',
    text='Nitrous Oxide',
    line=dict(color='rgb(127,0,0)'),
    stackgroup='one'
))
fig5.update_layout(title='Global Greenhouse Gas Emissions',
                   xaxis_title='Years',
                   yaxis_title='Greenhouse gas emissions (tonnes of CO2 equivalent)', 
                    plot_bgcolor='rgba(0,0,0,0.05)')
formatScatter(fig5)
#endregion

#region figure 6
# Slicing the df to remove the World value:
df_count = ultimate_df[~(ultimate_df['Country'] == 'World')]
df_count_1990 = df_count[df_count['Year']>1989]

# Creating list & dictionary to iterate over for value names and colors:
GHG_name = ['Carbone Dioxide', 'Methane', 'Nitrous Oxide', 'Total Greenhouse Gas']
GHG_color = [rangecolor_co2, rangecolor_meth, rangecolor_no, rangecolor_ghg]
GHG_cat_list = ['C02_cat', 'methane_cat', 'n_oxide_cat', 'GHG_cat']
GHG_label_list = ['C02_lbl', 'methane_lbl', 'n_oxide_lbl', 'GHG_lbl']

GHG_color_dict = dict(zip(GHG_cat_list, GHG_color))#
GHG_cat_name_dict = dict(zip(GHG_cat_list, GHG_name))
GHG_label_dict = dict(zip(GHG_cat_list, GHG_label_list))

#endregion

#region figure 7 
# Code for the correlation plots between temperature variation and Greenhouse Gas Emission for Dash

# Setting a dictionnary for the colors:
GHG_disc_color = ['rgb(252,78,42)', 'rgb(165,15,21)', 'rgb(127,0,0)', 'rgb(204,76,2)']
GHG_list = ['Annual CO2 emissions', 'Methane', 'Nitrous_oxide', 'Total GHG']
GHG_disc_color_dict = dict(zip(GHG_list, GHG_disc_color))
GHG_name_dict = dict(zip(GHG_list, GHG_name))
#endregion

#region figure 8
fig8 = px.choropleth(Covid_df, locations="Code", color="CO2_variation", range_color=[-20.0,0.0], 
                    color_continuous_scale=px.colors.sequential.YlOrRd, animation_frame="DATE")
fig8.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title="CO2 Variation (%)"))

formatMap(fig8)
#endregion

#region figure 9a
# Plotting Glaciers mass variations:
world_1966_2001_df = world_df.loc[(world_df['Year']>1966) & (world_df['Year']<2001)]

fig9a = make_subplots(specs=[[{"secondary_y": True}]])

fig9a.add_trace(go.Scatter(x=world_1966_2001_df.Year, y=world_1966_2001_df.Glacier_mass_value,
                    mode='markers',
                    marker={'color':world_1966_2001_df.Glacier_mass_value, 'colorscale':px.colors.sequential.Blues, 'size':13, 'cmid':0, 'cmin':-400000, 'cmax':0}
                    ),secondary_y=False)

fig9a.update_layout(#title='Variation of glaciers mass',
                   xaxis_title='Years',
                   plot_bgcolor='rgba(0,0,0,0.05)')
fig9a.update_yaxes(title_text="Glaciers mass variation (compared to 1966)", secondary_y=False)

formatScatter(fig9a)

fig9a.layout.width=700
fig9a.layout.height=400
fig9a.layout.modebar.orientation='v'

#endregion

#region figure 9b
# Slicing the df to select only the World values:
world_1900_df = world_df[world_df['Year']>1900]

# Plotting sea leval variations:
fig9b = make_subplots(specs=[[{"secondary_y": True}]])

fig9b.add_trace(go.Scatter(x=world_1900_df.Year, y=world_1900_df.Sea_level,
                    mode='markers',
                    marker={'color':world_1900_df.Sea_level, 'colorscale':px.colors.sequential.Blues, 'size':13, 'cmid':0, 'cmin':-200, 'cmax':100}
                    ),secondary_y=False)

fig9b.update_layout(title='Variation of sea-level',
                   xaxis_title='Years',
                   plot_bgcolor='rgba(0,0,0,0.05)')
fig9b.update_yaxes(title_text="Global sea_level variation (cm, compared to 1990)", secondary_y=False)

formatScatter(fig9b)

fig9b.layout.width=700
fig9b.layout.height=400
fig9b.layout.modebar.orientation = 'v'
#endregion

#region figure 10
# Slicing the df to avoid Nan values
df_count_2000 = df_count[df_count['Year']>1999]

# Cloropeth map using values from the biodiversity column
fig10 = px.choropleth(df_count_2000, 
                    locations="Code", 
                    color="biodiversity", 
                    hover_name="Country", 
                    color_continuous_scale=px.colors.sequential.Greens, 
                    animation_frame="Year", 
                    range_color=[0,100] 
                    #title='Worldwide biodiversity evolution'
                    )
fig10.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title="Share of important terrerstrial biodiversity sites that are protected"))
formatMap(fig10)
#endregion

#region figure 11
fig11 = go.Figure()

fig11.add_trace(go.Scatter(x=world_df['Year'], y=world_df['temperature_variations'],
                    mode='markers',
                    name='Past Temperature Variation',
                    marker={'color':'grey',
                            'size':7, 'cmid':0, 'cmin':-1, 'cmax':0.5}
                    ))
fig11.add_trace(go.Scatter(x=predictions_df.Year, y=predictions_df.temp_mod1,
                    mode='markers',
                    marker={'color':'#820000'},
                    name='Predictive Model 1'))
fig11.add_trace(go.Scatter(x=predictions_df.Year, y=predictions_df.temp_mod2,
                    mode='markers',
                    marker={'color':'#da8200'},
                    name='Predictive Model 2'))
fig11.add_trace(go.Scatter(x=predictions_df.Year, y=predictions_df.temp_mod3,
                    mode='markers',
                    marker={'color':'#e7b000'},
                    name='Predictive Model 3'))
fig11.add_trace(go.Scatter(x=predictions_df.Year, y=predictions_df.temp_mod4,
                    mode='markers',
                    marker={'color':'#30a4ca'},
                    name='Predictive Model 4'))
formatScatter(fig11)
#endregion

#endregion

#region sidebar
#sidebar components, contains all the link of the
#different paragraphs 
controls = dbc.FormGroup(
    [
        html.Ul(className="list-unstyled", children=
        [
            html.Li(
                html.A('Part 1 - Global Warming',href='#part1', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
            html.Li(
                html.A('Fig 1. Global temperature : Deviation from the mean',href='#title_graph_1',style={'font-size':'11px','color': '#191970'}),
            ),
            html.Li(
                html.A('Fig 2. Worldwide temperatures variations',href='#title_graph_2',style={'font-size':'11px','color': '#191970'}),
            ),
            html.Li(
                html.A('Fig 3a. Global temperature since -19 000 (TraCE-21ka simulation)',href='#title_graph_3a',style={'font-size':'11px','color': '#191970'}),
            ),
            html.Li(
                html.A('Fig 3b. Global temperature since JC',href='#title_graph_3b',style={'font-size':'11px','color': '#191970'}),
            ),
            html.Br(),
            html.Li(
                html.A('Part 2 - Impact of humans’ activities on global warming',href='#part2', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
            html.Li(
                html.A('Fig 4. Temperature variations compared to solar activity variation (deviation from period 1961-1990)',href='#title_graph_4', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Fig 5. Global Greenhouse Gas Emissions',href='#title_graph_5', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Fig 6. Worldwide Carbone Dioxide emissions (tonnes of CO2 equivalent)',href='#title_graph_6', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Fig 7. Correlation between Temperature variation and Carbone Dioxide emissions',href='#title_graph_7', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Fig 8. CO2 emissions during COVID period (%)',href='#title_graph_8', style={'font-size':'11px','color': '#191970'})
            ),
            html.Br(),
            html.Li(
                html.A('Part 3 - Impact of Global Warming on Life on Earth',href='#part3', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
            html.Li(
                html.A('Figure 9a. Glaciers mass variation (compared to 1966)',href='#title_graph_9a', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Figure 9b. Global sea level variation (cm, compared to 1990)',href='#title_graph_9b', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Fig 10. Worldwide biodiversity evolution',href='#title_graph_10', style={'font-size':'11px','color': '#191970'})
            ),
            html.Br(),
             html.Li(
                html.A('Part 4 - Projections: Forecasting the evolution of variables in play in the years to come ',href='#part4', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
             html.Li(
                html.A('Fig 11. Projected temperature evolution', href='#title_graph_11', style={'font-size':'11px','color': '#191970'})
            ),
            html.Br(),
             html.Li(
                html.A('Conclusion',href='#conclusion', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            )
        ]
        ),
    ]
)

#Create the sidebar
sidebar = html.Div( 
    [
        html.H2('Index', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)
#endregion

#region main content784

#Main title
main_title = html.Div(
    [ 
        html.H1('A data centered view on Global Warming', style=TEXT_STYLE),
        "by Christophe Duruisseau, Esperence Moussa, Colin Verhille, Valérie Vingtdeux © TV-Freedom",
    ]
)

introduction = dbc.Row([
    tc_introduction
])

#region part1
#part1 title 
part1_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2(id='part1',children=['Part 1 - Global warming'])
        ] 
        )
    ]
)

#region fig1
#fig1 title 
fig1_title = dbc.Row([
    html.H4(id='title_graph_1',children=[tc_title_fig1]),
    html.Div()]
)

#row fig1-txt1 content : 
fig1_txt1 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_1',
            config = {
            'displayModeBar' : False
                    },
            figure = fig1
            )],md=7),
        dbc.Col(
            html.Div(tc_txt1)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion

#region fig2
#fig2 title 
fig2_title = dbc.Row([
    html.H4(id='title_graph_2',children=[tc_title_fig2]),
    html.Div()]
)

#row fig2-txt2 content : 
fig2_txt2 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_2',
            config = {
            'displayModeBar' : True
                    },
            figure = fig2
            )],md=7),
        dbc.Col(
            html.Div(tc_txt2)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion

#region txt3
txt_3 = dbc.Row(align='left',children=[
    html.Div(tc_txt3a)
    ])    
#endregion

#region fig3a-3b
test_fig3 = dbc.Row(align="right",children=
[
    dbc.Col(align='left',children=[
        html.H4(id='title_graph_3a',children=[tc_title_fig3a]),
        dcc.Graph(id='graph_3a',
        config = {'displayModeBar' : False,
            },
        figure = fig3a
        )]
    ),
    dbc.Col(align='right',children=[
        html.H4(id='title_graph_3b',children=[tc_title_fig3b]),
        dcc.Graph(id='graph_3b',
        config = {'displayModeBar' : False},
        figure = fig3b
        )]
    )

])

#endregion

#region fig3
#fig3a title 
fig3a_title = dbc.Row([
    html.H4(tc_title_fig3a),
    html.Div()]
)

#row fig3a-txt3a content : 
fig3a_txt3a = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_3a',
            config = {
            'displayModeBar' : True
                    },
            figure = fig3a
            )],md=7),
        dbc.Col(
            html.Div(tc_txt3a)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

#fig3b title 
fig3b_title = dbc.Row([
    html.H4(tc_title_fig3b),
    html.Div()]
)

#row fig3b-txt3b content : 
fig3b_txt3b = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_3b',
            config = {
            'displayModeBar' : True
                    },
            figure = fig3b
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion
#endregion

#region part2 
part2_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2(id='part2',children=['Part 2 - Impact of humans’ activities on global warming'])
        ] 
        )
    ]
)

#region fig4
#fig4 title 
fig4_title = dbc.Row([
    html.H4(id='title_graph_4',children=[tc_title_fig4]),
    html.Div()]
)

#row fig4-txt4 content : 
fig4_txt4 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_4',
            config = {
            'displayModeBar' : False
                    },
            figure = fig4
            )],md=7),
        dbc.Col(
            html.Div(tc_txt4)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion

#region fig5
#fig5 title 
fig5_title = dbc.Row([
    html.H4(id='title_graph_5',children=[tc_title_fig5]),
    html.Div()]
)
#row fig5-txt5 content : 
fig5_txt5 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_5',
            config = {
            'displayModeBar' : False
                    },
            figure = fig5
            )],md=7),
        dbc.Col(
            html.Div(tc_txt5)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion

#region fig6
#fig6 title 
fig6_title = dbc.Row([
    html.H4(id='title_graph_6',children=[tc_title_fig6]),
    html.Div()]
)

#row fig6-txt6 content : 
fig6_txt6 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_6',
            config = {
            'displayModeBar' : True
                    }
            )],md=7),
        dbc.Col(
            html.Div(tc_txt6)
        ,md=5),  
        html.Div(
           #row 4 content : radio button for fig6
            dcc.RadioItems(inputStyle={"margin-right": "10px","margin-left":"20px"},
                id='radio_button_fig6',
                options=[{'label': j, 'value': i} for i,j in GHG_cat_name_dict.items()],
                value='GHG_cat'
            
)
        )
    ]
)
#endregion

#region fig7
#fig7 title 
fig7_title = dbc.Row([
    html.H4(id='title_graph_7',children=[tc_title_fig7]),
    html.Div()]
)

#row fig7-txt7 content : 
fig7_txt7 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_7',
            config = {
            'displayModeBar' : False
                    }
            )],md=7),
        dbc.Col(
            html.Div(tc_txt7)
        ,md=5),  
    
        #row 4 content : radio button for fig6
       html.Div(
        dcc.RadioItems(inputStyle={"margin-right": "10px","margin-left":"20px"},
                id='radio_button_fig7',
                options=[{'label': j, 'value': i} for i,j in GHG_name_dict.items()],
                value='Total GHG',
            )) 


       
    ]
)
#endregion

#region fig 8 
#fig8 title 
fig8_title = dbc.Row([
    html.H4(id='title_graph_8',children=[tc_title_fig8]),
    html.Div()]
)

#row fig8-txt8 content : 
fig8_txt8 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_8',
            config = {
            'displayModeBar' : True
                    },
            figure = fig8
            )],md=7),
        dbc.Col(
            html.Div(tc_txt8)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion

#endregion

#region part3
part3_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2(id='part3',children=['Part 3 - Impact of Global Warming on Life on Earth'])
        ] 
        )
    ]
)

#region txt_9
txt_9 = dbc.Row(align='left',children=[
    tc_txt9,
    html.Br(),
    html.Br()
    ])    

#endregion

#region fig9a-fig9b
test_fig9 = dbc.Row(align="right",children=
[
    dbc.Col(align='left',children=[
        html.H4(id='title_graph_9a',children=[tc_title_fig9a]),
        dcc.Graph(id='graph_9a',
        config = {'displayModeBar' : True,
            },
        figure = fig9a
        )]
    ),
    dbc.Col(align='right',children=[
        html.H4(id='title_graph_9b',children=[tc_title_fig9b]),
        dcc.Graph(id='graph_9b',
        config = {'displayModeBar' : True},
        figure = fig9b
        )]
    )

])
#endregion

#region fig9
#fig9a title 
fig9a_title = dbc.Row([
    html.H4(tc_title_fig9a),
    html.Div()]
)

#row fig9a-txt9a content : 
fig9a_txt9a = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_9a',
            config = {
            'displayModeBar' : True
                    },
            figure = fig9a
            )],md=7),
        dbc.Col(
            html.Div(tc_txt9)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)


#fig9b title 
fig9b_title = dbc.Row([
    html.H4(tc_title_fig9b),
    html.Div()]
)

#row fig9b-txt9b content : 
fig9b_txt9b = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_9b',
            config = {
            'displayModeBar' : True
                    },
            figure = fig9b
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion

#region fig10
#fig10 title 
fig10_title = dbc.Row([
    html.H4(id='title_graph_10',children=[tc_title_fig10]),
    html.Div()]
)

#row fig10-txt10 content : 
fig10_txt10 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_10',
            config = {
            'displayModeBar' : True
                    },
            figure = fig10
            )],md=7),
        dbc.Col(
            html.Div(tc_txt10)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion
#endregion

#region part4
part4_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2(id='part4',children=['Part 4 - Projections : Forecasting the evolution of variables in play in the years to come '])
        ] 
        )
    ]
)

#region fig11
#fig11 title 
fig11_title = dbc.Row([
    tc_txt11,
    html.Br(),
    html.Br(),
    html.Br(),
    html.H4(id='title_graph_11',children=[html.Br(),tc_title_fig11])]
)

#row fig11-txt11 content : 
fig11_txt11 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_11',
            config = {
            'displayModeBar' : False
                    },
            figure = fig11
            )],md=7),
        dbc.Col(
            html.Div(tc_txt11_list)
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)
#endregion
#endregion

#region conclusion and sources
conclusion_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2(id='conclusion',children=['Conclusion'])
        ] 
        )
    ]
)

conclusion = dbc.Row(align="center",justify="center",children=
    [   
        html.Div(tc_conclusion)
    ]
)

#endregion

#Main content
content = html.Div(
    [
        main_title,
        html.Br(),
        introduction,
        html.Br(),
        html.Br(),
        html.Hr(),
        part1_title,
        html.Hr(),
        html.Br(),
        html.Br(),
        fig1_title,
        fig1_txt1,
        html.Br(),
        html.Br(),
        fig2_title,
        fig2_txt2,
        html.Br(),
        html.Br(),
        txt_3,
        html.Br(),
        html.Br(),
        test_fig3,
        #fig3a_title,
        #fig3a_txt3a,
        #fig3b_title,
        #fig3b_txt3b,
        html.Br(),
        html.Br(),
        html.Hr(),
        part2_title,
        html.Hr(),
        html.Br(),
        html.Br(),
        fig4_title,
        fig4_txt4,
        html.Br(),
        fig5_title,
        fig5_txt5,
        html.Br(),
        fig6_title,
        fig6_txt6,
        html.Br(),
        fig7_title,
        fig7_txt7,
        html.Br(),
        fig8_title,
        fig8_txt8,
        html.Br(),
        html.Br(),
        html.Hr(),
        part3_title,
        html.Hr(),
        html.Br(),
        html.Br(),
        txt_9,
        html.Br(),
        test_fig9,
        html.Br(),
        html.Br(),
        #fig9a_title,
        #fig9a_txt9a,
        #fig9b_title,
        #fig9b_txt9b,
        fig10_title,
        fig10_txt10,
        html.Br(),
        html.Br(),
        html.Hr(),
        part4_title,
        html.Hr(),
        html.Br(),
        html.Br(),
        fig11_title,
        fig11_txt11,
        html.Br(),
        html.Br(),
        html.Hr(),
        conclusion_title,
        html.Hr(),
        html.Br(),
        html.Br(),
        conclusion
    ],
    style=CONTENT_STYLE
)
#endregion

#use bootstrap stylesheet
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#define page layout, which contains sidebar and content
app.layout = html.Div([sidebar, content])
#app.layout = html.Div([content])
#region callbacks

# Code for the clorepleth maps for Worldwide Greenhouse Gas Emissions:
@app.callback(
    Output('graph_6', 'figure'),
    [Input('radio_button_fig6', 'value')])
def update_graph_6(col_value):
  fig6 = px.choropleth(df_count_1990, 
                    locations="Code", 
                    color=col_value, 
                    hover_name="Country", 
                    color_continuous_scale=GHG_color_dict[col_value],
                    animation_frame="Year", 
                    range_color=[df_count_1990[col_value].min(),df_count_1990[col_value].max()]
                    #title=f'Worldwide {GHG_cat_name_dict[col_value]} emissions (tonnes of CO2 equivalent)'
                    )
  fig6.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title=f"{GHG_cat_name_dict[col_value]} emissions"))
  fig6.layout.coloraxis.colorbar = dict(
        title=f"{GHG_cat_name_dict[col_value]} emissions",
        tickvals=list(df_count_1990[col_value].unique()),
        ticktext=list(df_count_1990[GHG_label_dict[col_value]].unique()))
  # Disable auto for coloraxis setup:
  fig6.layout.coloraxis.cauto=False
  # Center the labels on the colorbar:
  fig6.layout.coloraxis.cmin = 0.5
  fig6.layout.coloraxis.cmax = (len(GHG_color_dict[col_value])/2)+0.5
  formatMap(fig6)
  return fig6

#Callback for title graph 6
@app.callback(
    Output('title_graph_6', 'children'),
    [Input('radio_button_fig6', 'value')])
def update_title6(col_value):
  return "Fig 6. Worldwide " + GHG_cat_name_dict[col_value] + " emissions (tonnes of CO2 equivalent)"

#Callback for fig7
@app.callback(
    Output('graph_7', 'figure'),
    [Input('radio_button_fig7', 'value')])
def update_graph(col_value):
  fig7 = px.scatter(world_1990_df, x=col_value, y='temperature_variations', trendline='ols')
  fig7.update_traces(marker={'color':GHG_disc_color_dict[col_value], 'size':7})
  fig7.update_layout(#title=f'Correlation between Temperature variation and {GHG_name_dict[col_value]} emissions',
                   xaxis_title=f'{GHG_name_dict[col_value]} emissions (tonnes)',
                   yaxis_title='Temperature Variation (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)')
  formatScatter(fig7)
  return fig7

#Callback for title graph 6
@app.callback(
    Output('title_graph_7', 'children'),
    [Input('radio_button_fig7', 'value')])
def update_title7(col_value):
  return "Fig 7. Correlation between Temperature variation and " + GHG_name_dict[col_value] + " emissions"


#endregion

#Run the server at port 8085
#Accessible through : http://localhost:8085
if __name__ == '__main__':
    app.run_server(port='8085')
