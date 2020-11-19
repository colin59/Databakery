import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px

#region Text elements

#region introduction
tc_introduction = '''
As defined by the Intergovernmental Panel on Climate Change (IPCC), climate in a narrow sense is usually defined as the average weather, or more rigorously, as the statistical description in terms of mean and variability of relevant quantities over a period of time ranging from months to thousands or millions of years. The relevant quantities are most often surface variables such as temperature, precipitations and wind.
The history of climate change science began in the early 19th century when the natural greenhouse effect was discovered by the french physicist Joseph Fourier. During the 1990s, technology evolution allowed better models to be developed, and a consensus began to form : greenhouse gases are deeply involved in most climate changes and human-induced emissions cause perceptible global warming.

Since then, research has continued and the issue of climate change and its impact on the environment is increasingly at the heart of current concerns, however, public opinion is divided on the subject. In this report, we will address some of the arguments highlighted by “climate sceptics” to minimize climate change or even deny it, such as:
Cold periods in weather still exist, there is no such thing as a warming.
Solar irradiation has an influence on climate that can explain the increasing trend.
Weather forecasting is regularly wrong for tomorrow, how could we predict long term variation ? 
Ice and glaciers melting doesn’t affect sea-level. It’s just as an ice cube in a glass, when it’s melted the volume is still the same.
Even if the Earth is warming, the impact is not so dramatic and we will adapt.'''
#endregion

#region part 1 (fig 1, 2, 3a, 3b)
tc_txt1 = '''To get a general idea of temperature evolution over time, we analyzed data obtained from the Berkeley Earth project (http://berkeleyearth.org/). The so-called historical period, which ranges from 1961 to 1990, was chosen as the reference period to calculate temperature evolution over time. As shown in Fig. 1, the deviation from the reference period of the rolling mean over a period of 10 years, indicates that overall the global temperature has risen of about 1.33°C within a 115 years’ period (from 8.50°C in 1900 to 9.83°C in 2015). The trend of increase was not linear and displayed a plateau between 1950 and 1970.'''

tc_txt2 = '''We next studied temperature variations by country. Overall, temperatures have risen in all countries for which data were available as shown in the maps displayed in Fig. 2. '''

tc_txt3a = '''While these data clearly demonstrate an increase of global temperature, which is particularly rapid since 1975, climate sceptics often argue that “climate’s changed before”. 
As displayed in Fig. 3A, we can see that for the past 21000 years, temperatures have mainly increased, from about 0°C to nearly 7°C. But the evolution was clearly slower than nowadays, changes of a full degree taking several thousand years. The most important change over a period of 100 years was 0.22°C.
As shown in Fig. 3B, temperature elevation for the contemporary period is very rapid as compared to this previous trend.'''
#endregion

#region part 2 (fig 4, 5, 6, 7, 8)
tc_txt4 = [html.Br(),html.Br(),html.Br(),'''“It’s the sun”... This is one of the arguments put forward by climate sceptics to explain global warming. Indeed, solar irradiance fluctuations due to solar cycles have an impact on natural climate variability. As we can see in Fig. 4, solar irradiation is fluctuating according to the decadal solar cycle (which takes approximately 11 years). Data on solar irradiation were gathered from the NOAA Climate Data Record (CDR). While solar irradiation and temperature variation on earth seemed to follow a similar trend at the beginning, the largest solar fluctuation happened around 1960. In contrast, the fastest global warming started in 1980, whereas solar activity entered a period of lower intensity, leading us to refute the “sun” argument and to explore alternative hypotheses to explain this rapid recent global warming. ''']

tc_txt5 = '''Beside solar radiation, temperature on earth is regulated by greenhouse gas (GHG). The atmosphere and the earth’s surface emit infrared radiation in response to the energy received by the sun. Clouds and GHG (that include water vapor, carbon dioxide, methane, nitrous oxide and ozone) absorb and largely re-emit this radiation towards the ground. This phenomenon is called the ‘greenhouse effect”.
It is therefore interesting to take a closer look at these GHG emissions. To do so we collected data from “Our world in data”.
As shown in Fig. 5, global GHG emissions have increased steadily since 1990. Over a 25 years period, we observed an increase in GHG emissions (Carbon Dioxide, Methane, Nitrous Oxide) of around 50%.
'''

tc_txt6 = ''' Fig. 6 display the differences in GHG emissions by country across the world. The world’s largest GHG emitters are among the most populous countries: i.e. the United States, China, and Russia. Of note, there can be large differences in emissions, even between countries with similar living standards. '''

tc_txt7 = ''' The correlation between GHG emissions and the temperature variation is displayed in Fig. 7. It shows a correlation between temperature and total GHG emissions. The points fall close to the line, which indicates a strong linear relationship between the two variables. When the emissions of GHG increase, the temperature also increases. '''

tc_txt8 = ''' These GHG (Carbon Dioxide, Methane, Nitrous Oxide) can be produced by natural processes such as volcanic eruptions and forest fires (CO2), but also by human activities with the use of fossil carbon or the manufacture of cement. Methane production is linked to fermentation processes as well as intensive agriculture. While it is evident that these gases emissions have considerably increased since the beginning of the industrial era, the most striking proof that human activities are mainly responsible for these emissions come from the study of GHG emissions during the lockdown period due to the COVID-19 epidemic, in the course of which many activities have been stopped.  '''
#endregion

#region part 3 (fig 9, 10)
tc_txt9 = ''' The impacts of global warming are numerous and observed throughout the world : weather anomalies, intensification of storms, mass extinction of wildlife, desertification. We have chosen to plot two striking trends that are easily observed : melting of glaciers and rise of sea-level, the first phenomenon contributing to the second. In the US, the NOAA considers that 40% of the population lives in a coastal area, susceptible to be affected by sea-level rise. Developing countries are over exposed to this risk. Islands are particularly threatened, Cuba or Bahamas for example, could see their superficy dramatically reduced in the scenarios of a rise of several meters. '''


tc_txt10 = ['Another aspect that can be linked to global warming is the quickly increasing part of wildlife facing risk of extinction.','This is illustrated in Fig. 10, which shows the increasing part of protected areas throughout the world from 2000 to 2015.',html.Br(),html.Br(), 'The beginning of a 6th “mass extinction” is a growing hypothesis. This trend can be explained by climate change, leading to the acidification of oceans, and major changes in ecosystems, but also by direct pollution caused by human activity.']
#endregion

#region part 4 (fig 11)
tc_txt11 = '''As we found a strong correlation between GHG emissions and temperature rise, we tried to build a model to predict future temperature according to different scenarios. What if nothing changes? What if technology, and/or radical changes in consumption and production modes enabled us to stabilize or reduce gas emissions ? Some research focus on technological ways to achieve that goal.
Future temperature was predicted based on GHG emissions. We used linear regression models to predict GHG emissions in the future based on several assumptions :'''

tc_txt11_list = [          
 html.Ul(className="list-unstyled", children=
        [
            html.Li(
                html.Div('''- Model 1: If nothing changes and emissions continue to follow the same trend. In this scenario, our model of regression brings us to a rise of temperatures up to 3,5°C compared to the mean of the period 1960-1990 (Fig. 11). A trend never observed in history, with potential disastrous effects.
''')
            ),     
            html.Li(
                html.Div('''- Model 2: If we could stabilize GHG emissions to current levels. We imputed the latest value from GHG from year 2016 up to 2100. Our regression model shows a stabilization of temperatures at the current level (Fig. 11). To be more accurate, we could turn to climatology to find more complex models...
''')
            ),   
            html.Li(
                html.Div('''- Model 3: If we could lockdown the population for the next 80 years.... Given that we observed that during the lockdown period due to the COVID-19 epidemics, a reduction of about 17% of CO2 emissions was observed, we decided to remove 17% of Carbon dioxide emissions from the 2015 values. Given that we observed above that CO2 emissions were highly correlated with Methane and Nitrous_oxide emissions, we will apply the same strategy to those variables. Our predictions in this case indicated a stabilization of the temperatures around 0.65°C over the reference mean. (Fig. 11)
''')
            ),   
            html.Li(
                html.Div('''- Model 4: What would happen if we could reduce GHG emissions by 1% every year thanks to science or technology ? In this case, our model predicted a slow decrease of temperature, bringing us back close to the reference mean in 2100.
''' )
            )
                
        ])
        ]
#endregion

#region conclusion
tc_conclusion = '''The objective of this study was to answer the following 4 questions with a data-driven approach : Is global warming a myth?  Is it due to human activities?  Is it important? Is it definitive?
To answer these questions, we collected data to assess the evolution of temperature over time, its variations by country, and historical temperature evolution since -19500BC. We also looked at correlations between temperature variation on earth and solar irradiation, GHG emissions since 1990. 
We also explored a study about a temporary reduction in daily global CO2 emissions during the COVID-19 lock-down period, and the impact of global warming on nature.
Since 1850 humans have emitted large quantities of GHG which have caused an increase of temperature. The consequences could be dramatic: intensification of extreme phenomenons, displacement of animal species, weather anomalies, intensification of storms, mass extinction of wildlife, desertification… 

Hence, the threat is present and can be a real menace for the survival of species including homo sapiens. Thus, we can say that man represents a threat for the climate, because of his overproduction of GHG, and conversely, global warming represents a threat, both for man and for our planet.
'''
#endregion

#region Title fig 
tc_title_fig1 = 'Fig 1. Global temperature : Deviation from the mean'
tc_title_fig2 = 'Fig 2. Worldwide temperatures variations'
tc_title_fig3a = 'Fig 3a. Global temperature since -19 000 (TraCE-21ka simulation)'
tc_title_fig3b = 'Fig 3b. Global temperature since JC'
tc_title_fig4 = 'Fig 4. Temperature variations compared to solar activity variation (deviation from period 1961-1990)'
tc_title_fig5 = 'Fig 5. Global Greenhouse Gas Emissions'
tc_title_fig6 = 'Fig 6. Worldwide Carbone Dioxide emissions (tonnes of CO2 equivalent)'
tc_title_fig7 = 'Fig 7. Correlation between Temperature variation and Carbone Dioxide emissions'
tc_title_fig8 = 'Fig 8. CO2 emissions during COVID period (%)'
tc_title_fig9a = 'Fig 9a. Glaciers mass variation (compared to 1966)'
tc_title_fig9b = 'Fig 9b. Global sea level variation (cm, compared to 1990)'
tc_title_fig10 = 'Fig 10. Worldwide biodiversity evolution'
tc_title_fig11 = 'Fig 11. Projected temperature evolution'
#endregion

#endregion

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