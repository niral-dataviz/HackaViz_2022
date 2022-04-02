import pandas as pd
import plotly.express as pt
import streamlit as st

df=pd.read_csv("actions_culturelles_soutenues.csv")

## extract only film
df_film=df[df['oeuvre']=='Film']
bar_chart=df_film.groupby(by=["collecteur","annee"]).sum().sort_values(by="montant", ascending=False).reset_index()
bar_chart["annee"]=bar_chart["annee"].round(0).astype('object')

## bar chart
fig = pt.bar(bar_chart, x='collecteur', y='montant',
             hover_data=['annee'], color='annee',
             labels={'collecteur':'Private copying levy'}, height=400,
             color_discrete_sequence=["#DAF7A6","#FFC300", "#BF7A31","#FF5733","#C70039"]
)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig)

st.dataframe(bar_chart.head())