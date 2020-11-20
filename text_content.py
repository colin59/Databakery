import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px

#region Text elements


#region Graph color

#Get custom color Pal based on defined var above
def getColorPal(pal, pal_start_range, max_cat):
  '''This function return a list of tuples with the interval range and its associated color to display the side color bar.
  The function takes in 3 arguments:
  pal =  Palette name, 
  pal_start_range = index of the first color wanted from the palette,
  max_cat = number of categories needed'''
  #Get custom color Pal based on defined var above
# Function to get the color scale for the different maps:
  continous_color_scales = px.colors.sequential.swatches()
  color_dict = {}
  for i in range(len(continous_color_scales['data'])):
    color_dict[continous_color_scales['data'][i]['y'][0]]=i

  customColor = []
  intervalMap = np.linspace(0,1,max_cat+1)
  i = pal_start_range
  j = 0
  while j+1 <= max_cat:
    customColor.append((intervalMap[j],continous_color_scales['data'][color_dict[pal]]['marker']['color'][i]))
    j += 1
    customColor.append((intervalMap[j],continous_color_scales['data'][color_dict[pal]]['marker']['color'][i]))
    i += 1
  return customColor

#endregion