import pandas as pd
import plotly.express as pt
import streamlit as st
st.set_page_config(page_title="Hackaiz-2022",page_icon=":flag-ua:", layout="wide", initial_sidebar_state="expanded",
     menu_items={
         'About': "The app is created by [Kalairani](https://kalairani.github.io/) and [Murugesh](https://murugeshmanthiramoorthi.github.io/). This is a project created as a part of HackaViz2022 organised by Toulouse Data Viz."
     })

df=pd.read_csv("actions_culturelles_soutenues.csv")

#Filter
with st.sidebar:
    selected_ouevre=st.radio("Chosir l'oeuvre ici: ", list(df["oeuvre"].unique()))
    # st.snow()


## extract only film
df_film=df[df['oeuvre']==selected_ouevre]
bar_chart=df_film.groupby(by=["collecteur","annee"]).sum().sort_values(by="montant", ascending=False).reset_index()
bar_chart["annee"]=bar_chart["annee"].round(0).astype('object')


st.header("Hackaviz 2022 : Financement par la copie privée en France")

# Metrics
m1, m2, m3= st.columns((1,1,1))
st.markdown("""
<style>
.big-font {
    font-size:300px !important;
}
</style>
""", unsafe_allow_html=True)
st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
m1.metric(label =':money_with_wings: Montant total',value = str(round(df_film["montant"].sum()/1000000,2)) + ' M €',
          delta=str(round(((1 - (542000000 - df_film["montant"].sum()) / 542000000)) * 100, 2)) + ' % de entier',
          delta_color='normal')
m2.metric(label =':heart: Nombre total des beneficiaires',value = str(df_film["beneficiaire"].nunique()),
          delta=str(round(((1 - (22000 - df_film["beneficiaire"].nunique()) / 22000)) * 100, 2)) + ' % de entier',
          delta_color='normal')
m3.metric(label ='🧮 Nombre total des projets',value = str(df_film.shape[0]),
          delta=str(round(((1 - (53003- df_film.shape[0])/53003))*100, 2)) + ' % de entier',
              delta_color='normal')

a_covid = df_film[df_film["annee"]==2020]["montant"].mean()
b_covid = df_film[df_film["annee"]<2020]["montant"].mean()

if a_covid > b_covid:
    new_col1, new_col2 = st.columns([1,1])
    new_col1.image('https://cdn.pixabay.com/photo/2016/11/21/13/58/ball-1845546_960_720.jpg')
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.markdown("""Le montant moyen a <span style="color: #ff0000">augmenté</span> pour l'oeuvre <span style="color: #ff0000">""" + selected_ouevre + """"</span> après la Covid-19""",unsafe_allow_html=True)
else:
    new_col1, new_col2 = st.columns([1, 1])
    new_col1.image('https://cdn.pixabay.com/photo/2018/03/27/17/25/cat-3266673_960_720.jpg')
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.markdown("""Le montant moyen a <span style="color: #ff0000">diminué</span> pour l'oeuvre <span style="color: #ff0000">"""+ selected_ouevre + """</span> après la Covid-19""", unsafe_allow_html=True)


col1, col2 = st.columns ([4,4])
## bar chart

fig = pt.bar(bar_chart, x='collecteur', y='montant',
             hover_data=['annee'], color='annee',
             labels={'collecteur':'Collecteur', 'annee':'Annee', 'montant': 'Montant'},
             color_discrete_sequence=["#DAF7A6","#FFC300", "#BF7A31","#FF5733","#C70039"]
)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

col1.subheader("Le montant distribué par collecteur")
col1.plotly_chart(fig, use_container_width=True)


fig_scatter = pt.scatter(df_film, x="annee", y="montant", color="aide",
                labels={'aide':'Aide', 'annee':'Annee', 'montant': 'Montant', 'collecteur':'Collecteur'},
                color_discrete_sequence=["#FFC300", "#BF7A31","#FF5733","#C70039"],
                 size='montant', hover_data=['collecteur'], size_max=20)

fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
col2.subheader("Le montant distribué par aide")
col2.plotly_chart(fig_scatter, use_container_width=True)