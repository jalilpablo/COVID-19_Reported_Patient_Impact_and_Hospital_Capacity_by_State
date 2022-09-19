import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly_express as px
import datetime as dt




#datos
df = pd.read_csv('covid_limpio.csv',index_col=0)
df['date']=pd.to_datetime(df['date'])
#diccionario de estados
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))
# population
population_data = pd.read_csv('population_limpio.csv',index_col=0)

#funciones



#funcion para ICU POR ESTADO
def icu_por_estado():

    appointment = st.slider(
    "Seleccione Fechas a Considerar:",
    value=(dt.date(2020,1,1), dt.date(2022,8,1)))

    st.header(f'Cantidad de Camas de Unidades de Cuidados Intensivos Utilizadas por COVID -19 ({appointment[0]} - {appointment[1]})')

    icu_por_estado = df[(df.date.dt.date>=appointment[0]) & (df.date.dt.date<appointment[1])].groupby('state').sum()[['staffed_icu_adult_patients_confirmed_covid','staffed_icu_pediatric_patients_confirmed_covid']]
    icu_por_estado = icu_por_estado.join(pd.DataFrame.from_dict(abbrev_to_us_state,orient='index',columns=['state_name']))
    icu_por_estado['total_icu'] = icu_por_estado.staffed_icu_adult_patients_confirmed_covid + icu_por_estado.staffed_icu_pediatric_patients_confirmed_covid

    fig = px.choropleth(
                    locations=icu_por_estado.index, 
                    locationmode="USA-states", 
                    scope="usa",
                    color=icu_por_estado.total_icu,
                    color_continuous_scale="balance",
                    hover_name=icu_por_estado.state_name,
                    labels={ "color": "Camas de Cuidados Intensivos Utilizadas","locations": "Estado"})
    st.plotly_chart(fig)

#funcion OCUPACION HOSPITALARIA DICIEMBRE 2020
def ocupacion_hospitalaria_top_10_barplot():

    appointment = st.slider(
    "Seleccione Fechas a Considerar:",
    value=(dt.date(2020,1,1), dt.date(2022,8,1)))

    st.header(f'Porcentaje de Ocupacion Hospitalaria Promedio entre los dias {appointment[0]} y {appointment[1]}')
    
    bed_utilization_december_2020_mean = df[(df.date.dt.date>=appointment[0]) & (df.date.dt.date<appointment[1])].groupby('state').mean()[['inpatient_bed_covid_utilization']]
    bed_utilization_december_2020_mean.sort_values('inpatient_bed_covid_utilization',ascending=False,inplace=True)
    bed_utilization_december_2020_mean= bed_utilization_december_2020_mean.join(pd.DataFrame.from_dict(abbrev_to_us_state,orient='index',columns=['state_name']))
    fig = px.bar(bed_utilization_december_2020_mean.head(10), 
        x="inpatient_bed_covid_utilization",
        y="state_name",
        orientation='h',
        labels={ "state_name": "Estado","inpatient_bed_covid_utilization": "Porcentaje de Utilización"})   
    
    st.plotly_chart(fig)

#funcion para mapa HOSPITALIZADOS POR ESTADO    
def selector():
    appointment = st.slider(
    "Seleccione Fechas a Considerar:",
    value=(dt.date(2020,1,1), dt.date(2022,8,1)))


    #pd.DataFrame.from_dict(abbrev_to_us_state,orient='index',columns=['state_name'])

    st.header(f'Cantidad de Personas Hospitalizadas por COVID -19 ({appointment[0]} - {appointment[1]})')
    internados_por_estado = df[(df.date.dt.date>=appointment[0]) & (df.date.dt.date<appointment[1])].groupby('state').sum()[['inpatient_beds_used_covid']]

    internados_por_estado = internados_por_estado.join(pd.DataFrame.from_dict(abbrev_to_us_state,orient='index',columns=['state_name']))

    label={ "color": "Personas Hospitalizadas","locations": "Estado"}
    fig = px.choropleth(
                    locations=internados_por_estado.index, 
                    locationmode="USA-states", 
                    scope="usa",
                    color=internados_por_estado.inpatient_beds_used_covid,
                    color_continuous_scale="balance",
                    hover_name=internados_por_estado.state_name,
                    labels=label)
    st.plotly_chart(fig)

# HOSPITALIZADOS POR HABITANTE
def hospitalizados_por_habitante():
    appointment2 = st.slider(
    "Seleccione Fechas a Considerar:",
    value=(dt.date(2020,1,1), dt.date(2022,8,1)))


    #pd.DataFrame.from_dict(abbrev_to_us_state,orient='index',columns=['state_name'])

    st.header(f'Cantidad de Personas Hospitalizadas por COVID -19, por Habitante ({appointment2[0]} - {appointment2[1]})')
    internados_por_estado = df[(df.date.dt.date>=appointment2[0]) & (df.date.dt.date<appointment2[1])].groupby('state').sum()[['inpatient_beds_used_covid']]

    internados_por_estado = internados_por_estado.join(pd.DataFrame.from_dict(abbrev_to_us_state,orient='index',columns=['state_name']))
    internados_por_estado_por_habitante = internados_por_estado.merge(population_data,left_on=internados_por_estado.index,right_on='abb')

    label={ "color": "Personas Hospitalizadas","locations": "Estado"}
    fig = px.choropleth(                    
                  locations=internados_por_estado_por_habitante.abb,  
                  locationmode="USA-states", 
                  scope="usa",
                  color=internados_por_estado_por_habitante.inpatient_beds_used_covid / internados_por_estado_por_habitante.Pop,
                  color_continuous_scale="balance",
                  hover_name=internados_por_estado_por_habitante.state_name,
                  labels=label)

    st.plotly_chart(fig)



#ICU por estado por habitante
def icu_por_estado_por_habitante():

    appointment2 = st.slider(
    "Seleccione Fechas a Considerar:",
    value=(dt.date(2020,1,1), dt.date(2022,8,1)))

    st.header(f'Cantidad de Camas de Unidades de Cuidados Intensivos Utilizadas por COVID -19, por Habitante({appointment2[0]} - {appointment2[1]})')

    icu_por_estado = df[(df.date.dt.date>=appointment2[0]) & (df.date.dt.date<appointment2[1])].groupby('state').sum()[['staffed_icu_adult_patients_confirmed_covid','staffed_icu_pediatric_patients_confirmed_covid']]
    icu_por_estado = icu_por_estado.join(pd.DataFrame.from_dict(abbrev_to_us_state,orient='index',columns=['state_name']))
    

    icu_por_estado['total_icu'] = icu_por_estado.staffed_icu_adult_patients_confirmed_covid + icu_por_estado.staffed_icu_pediatric_patients_confirmed_covid

    icu_por_estado_por_habitante = icu_por_estado.merge(population_data,left_on=icu_por_estado.index,right_on='abb')
    fig = px.choropleth(
                    locations=icu_por_estado_por_habitante.abb, 
                    locationmode="USA-states", 
                    scope="usa",
                    color=icu_por_estado_por_habitante.total_icu / icu_por_estado_por_habitante.Pop,
                    color_continuous_scale="balance",
                    hover_name=icu_por_estado_por_habitante.state_name,
                    labels={ "color": "Camas de Cuidados Intensivos Utilizadas","locations": "Estado"})
    st.plotly_chart(fig)


#Cuarentena Nueva York
def cuarentena_nuevayork():
    st.text('La cuarentena en el Estado de New York estuvo establecida desde 2020-03-22 hasta 2020-06-13')
    ny = df[df.state=='NY']
    ny_cuarentena = ny[('2020-03-22'<=ny.date) & (ny.date<'2020-06-13')]
    ny_cuarentena = ny_cuarentena[['date','inpatient_beds_used_covid']]
    ny_cuarentena.set_index(ny_cuarentena.date,inplace=True,drop=True)
    ny_cuarentena.sort_index(inplace=True)
    f = px.line(x=ny_cuarentena.index,y=ny_cuarentena.inpatient_beds_used_covid,labels={
                     "x": "Fecha",
                     "y": "Cantidad de Camas Ocupadas"},title='Camas Hospitalarias Ocupadas durante la Cuarentena en el Estado de New York')
    st.plotly_chart(f)




#barra lateral
st.sidebar.title('Navegación')
options = st.sidebar.radio('Graficos',options=['Inicio','Hospitalizados por Estado','Uso de Camas de Cuidados Intensivos','Ocupacion Hospitalaria',
'Hospitalizados por Habitante','Uso de Camas de Cuidados Intensivos por Habitante','Cuarentena New York'])



#titulo de la Pagina
#st.title('COVID - 19 en Estados Unidos')
#st.text('Esta es la primer prueba')
col1, col2, col3 = st.columns(3)

st.image('covid_portada.png')
st.image('logo-henry-white-lg.png')




# if con las opciones del seleccionador
if options == 'Inicio':
    st.text('Brebe Análisis del Sistema Hospitalario Estadounidense durante la Pandemia')
if options == 'Hospitalizados por Estado':
    selector()
elif options == 'Uso de Camas de Cuidados Intensivos':
    icu_por_estado()
elif options == 'Ocupacion Hospitalaria':
    ocupacion_hospitalaria_top_10_barplot()
elif options == 'Hospitalizados por Habitante':
    hospitalizados_por_habitante()
elif options == 'Uso de Camas de Cuidados Intensivos por Habitante':
    icu_por_estado_por_habitante()
elif options == 'Cuarentena New York':
    cuarentena_nuevayork()
