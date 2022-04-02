import pandas as pd
import plotly.express as pt
import streamlit as st
st.set_page_config(page_title="HackaViz_2022",page_icon="⌛", layout="wide")

df=pd.read_csv("actions_culturelles_soutenues.csv")

#Filter
with st.sidebar:
    selected_ouevre=st.radio("Choose a value here: ", list(df["oeuvre"].unique()))


## extract only film
df_film=df[df['oeuvre']==selected_ouevre]
bar_chart=df_film.groupby(by=["collecteur","annee"]).sum().sort_values(by="montant", ascending=False).reset_index()
bar_chart["annee"]=bar_chart["annee"].round(0).astype('object')


st.header("Collecteur History")
col1, col2 = st.columns ([4,4])
## bar chart

fig = pt.bar(bar_chart, x='collecteur', y='montant',
             hover_data=['annee'], color='annee',
             labels={'collecteur':'Private copying levy'},
             color_discrete_sequence=["#DAF7A6","#FFC300", "#BF7A31","#FF5733","#C70039"]
)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

col1.subheader("Amount collected per year")
col1.plotly_chart(fig, use_container_width=True)


fig_scatter = pt.scatter(df_film, x="annee", y="montant", color="aide",
                 size='montant', hover_data=['collecteur'], size_max=20)

fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
col2.subheader("Aide per year")
col2.plotly_chart(fig_scatter, use_container_width=True)

