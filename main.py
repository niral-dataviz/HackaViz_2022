import pandas as pd
import plotly.express as pt
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Hackaiz-2022",page_icon="🇺🇦", layout="wide", initial_sidebar_state="expanded",
     menu_items={
         'About': "The app is created by [Kalairani](https://kalairani.github.io/) and [Murugesh](https://murugeshmanthiramoorthi.github.io/). This is a project created as a part of HackaViz2022 organised by Toulouse Data Viz."
     })

df=pd.read_csv("actions_culturelles_soutenues.csv")

#Filter
with st.sidebar:
    selected_ouevre=st.radio("Chosir l'oeuvre ici: ", list(df["oeuvre"].unique()))



## extract only film
df_filter=df[df['oeuvre']==selected_ouevre]
bar_chart=df_filter.groupby(by=["collecteur","aide","annee"]).sum().sort_values(by="montant", ascending=False).reset_index()
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
m1.metric(label ='💸 Montant total',value = str(round(df_filter["montant"].sum()/1000000,2)) + ' M €',
          delta=str(round(((1 - (542000000 - df_filter["montant"].sum()) / 542000000)) * 100, 2)) + ' % de entier',
          delta_color='normal')
m2.metric(label ='❤️ Nombre total des beneficiaires',value = str(df_filter["beneficiaire"].nunique()),
          delta=str(round(((1 - (22000 - df_filter["beneficiaire"].nunique()) / 22000)) * 100, 2)) + ' % de entier',
          delta_color='normal')
m3.metric(label ='🧮 Nombre total des projets',value = str(df_filter.shape[0]),
          delta=str(round(((1 - (53003- df_filter.shape[0])/53003))*100, 2)) + ' % de entier',
              delta_color='normal')

a_covid = df_filter[df_filter["annee"]==2020]["montant"].mean()
b_covid = df_filter[df_filter["annee"]<2020]["montant"].mean()

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



lottie_url_up = "https://assets10.lottiefiles.com/packages/lf20_4dl0zamm.json"
lottie_json_up = load_lottieurl(lottie_url_up)

lottie_url_down = "https://assets10.lottiefiles.com/packages/lf20_pmtefjhf.json"
lottie_json_down = load_lottieurl(lottie_url_down)
if a_covid > b_covid:
    new_col1, new_col2 = st.columns([1,1])
    with new_col1:
        st_lottie(lottie_json_up, height=300)
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    new_col2.markdown("""<p class="big-font">Le montant moyen a <span style="color: #ff0000">augmenté</span> pour l'oeuvre <span style="color: #ff0000">""" + selected_ouevre + """</span> après la Covid-19 </p>""", unsafe_allow_html=True)
else:
    new_col1, new_col2 = st.columns([1, 1])
    with new_col1:
        st_lottie(lottie_json_down, height=300)
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.text("")
    new_col2.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    new_col2.markdown("""<p class="big-font">Le montant moyen a <span style="color: #ff0000">diminué</span> pour l'oeuvre <span style="color: #ff0000">""" + selected_ouevre + """</span> après la Covid-19 </p>""", unsafe_allow_html=True)
df_matrix=pd.crosstab(df_filter['aide'], df_filter['annee'],values=df_filter['montant'],aggfunc=sum).fillna(0)
label=list(df_matrix.index) + list(df_matrix.columns)
source=[]
for i in range(len(df_matrix.index)):
    source.extend([i] * len(df_matrix.columns))



target = list(np.arange(label.index(list(df_matrix.columns)[0]),label.index(list(df_matrix.columns)[-1])+1))*len(df_matrix.columns)

value=[]
for i in df_matrix.iterrows():
    value.extend(list(i[1]))

link = dict(source = source, target = target, value = value,color="#fcba03")
node=dict(label=label , pad=35, thickness=10, color=["#fc4e03","#fc6f03","#fc8c03","#fcc203","#fcf403","#dffc03","#cefc03","#b1fc03","#90fc03"])
data = go.Sankey(link = link, node=node)

fig_sankey = go.Figure(data)

st.subheader("Contribution pour les aides")
st.plotly_chart(fig_sankey, use_container_width=True)


col1, col2 = st.columns ([4,4])
## bar chart

fig = pt.bar(bar_chart, x='collecteur', y='montant',
             hover_data=['aide'], color='aide',
             labels={'collecteur':'Collecteur', 'aide':'Aide', 'montant': 'Montant', 'annee':'Année'}, animation_frame="annee",
             color_discrete_sequence=["#DAF7A6","#FFC300", "#BF7A31","#FF5733","#C70039"]
)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',transition = {'duration': 2000}
)

col1.subheader("Le montant distribué par collecteur")
col1.plotly_chart(fig, use_container_width=True)




fig_2=pt.scatter(df_filter, x="montant", y="aide", animation_frame="annee",color="collecteur",size="montant"
                 ,labels={'collecteur':'Collecteur', 'annee':'Année', 'montant': 'Montant','aide':'Aide'})

fig_2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',transition = {'duration': 2000}
)

col2.subheader("Le montant distribué par aide")
col2.plotly_chart(fig_2, use_container_width=True)

