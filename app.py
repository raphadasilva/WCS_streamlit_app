import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Une application bien carrossée")

df = pd.read_csv("https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv")
df["continent"] = df["continent"].str.strip()
df["continent"] = df["continent"].str.replace(".","")
blocs = {"US":"#A35029","Europe":"#374D8D","Japan":"#C4B743"}

st.write("Un premier tour d'horizon laisse apparaître une large domination des Etats-Unis dans le jeu de données.")

df["decompte"]=1
total = df.groupby(by="continent").agg({"decompte":"sum"}).reset_index()

fig1, ax1 = plt.subplots()
sns.set(rc={'axes.facecolor':'#0E1117', 'figure.facecolor':'#0E1117',"text.color":"#fff","xtick.color":"#fff","ytick.color":"#fff","axes.labelcolor":"#fff"})
fig1 = sns.barplot(data=total, x="continent", y="decompte", hue="continent", palette=blocs)
ax1.spines['bottom'].set_color('white')
ax1.spines['top'].set_color('white')
ax1.spines['left'].set_color('white')
ax1.spines['right'].set_color('white')
ax1.xaxis.label.set_color('white')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')
ax1.set_xlabel("")
ax1.set_ylabel("Voitures présentes dans les données", color="#fff")
ax1.get_legend().remove()

st.pyplot(fig1.figure)

st.write("Il s'avère que cette dominance a des répercussions sur de nombreuses représentations de ces données. Exemple avec le graphe ci-dessous :")

fig2, ax2= plt.subplots()
fig2 = sns.jointplot(x=df["cubicinches"],y=df["hp"], hue=df["continent"], palette=blocs, kind="kde",legend=False)
fig2.ax_joint.set_xlabel('Capacité du moteur (pouces au cube)')
fig2.ax_joint.set_ylabel('Puissance (chevaux)')

st.pyplot(fig2.fig)

st.write("On observe **une nette distorsion des valeurs états-uniennes**, tandis que les données européennes et japonnaises sont plutôt superposées, pour une colonne comme pour l'autre.")

st.write("Nous allons parer à cela **en filtrant les données** par continent à l'aide de boutons qui permettront de varier les échelles.")

tampon = df

v_eu = st.button("Etats-Unis")
v_europe = st.button("Europe")
v_japon = st.button("Japon")
v_ensemble = st.button("Tous les pays")

if v_eu:
	tampon = df[df["continent"]=="US"]
	print(tampon["continent"].unique())
elif v_europe:
	tampon = df[df["continent"]=="Europe"]
	print(tampon["continent"].unique())
elif v_japon:
	tampon = df[df["continent"]=="Japan"]
	print(tampon["continent"].unique())
elif v_ensemble:
	tampon = df
	print(tampon["continent"].unique())


fig3, ax3= plt.subplots()
if not v_ensemble:
	fig3 = sns.scatterplot(data=tampon,y="weightlbs", x="hp", color=blocs[tampon["continent"].unique()[0]], label=tampon["continent"].unique()[0])
else:
	fig3 = sns.scatterplot(data=tampon,y="weightlbs", x="hp", hue="continent", palette=blocs)
ax3.set_title("La puissance corrélée au poids quel que soit le continent")
ax3.set_xlabel("Puissance (chevaux)")
ax3.set_ylabel("Poids (livres)")

st.pyplot(fig3.figure)

st.write("Parmi les corrélations positives, une des plus marquées concerne la relation entre le poids d'un véhicule (en livres) et la puissance (en chevaux). Autrement dit : **plus une voiture est lourde**(peut-être à cause du poids du moteur)**, plus elle puissante**. Cela vaut pour n'importe quelle origine.")

st.write("La tentation est grande de vérifier si les voitures les plus anciennes étaient aussi les moins performantes. Pour cela, on va comparer les années de commercialisation à la consommation d'un véhicule.")

fig4, ax4= plt.subplots()
if not v_ensemble:
	fig4 = sns.scatterplot(data=tampon,y="mpg", x="year", color=blocs[tampon["continent"].unique()[0]], label=tampon["continent"].unique()[0])
else:
	fig4 = sns.scatterplot(data=tampon,y="mpg", x="year", hue="continent", palette=blocs)
ax4.set_title("Les voitures européennes et japonnaises les plus récentes consomment le plus")
ax4.set_xlabel("")
ax4.set_ylabel("Consommation (miles/gallon)")

st.pyplot(fig4.figure)

st.write("On l'a dit, les effectifs sont très inégaux selon les continents. Un autre point intéressant peut être de **comparer le nombre de véhicules sortis chaque année**.")

fig5, ax5= plt.subplots()
if not v_ensemble:
	fig5 = sns.histplot(data=tampon,x="year", color=blocs[tampon["continent"].unique()[0]], label=tampon["continent"].unique()[0])
	ax5.set_title(tampon["continent"].unique()[0])
else:
	fig5 = sns.histplot(data=tampon,x="year", color="#cecece", label="Tous les continents")
	ax5.set_title("Les années 1980 tirées vers le haut par les véhicules japonais")

ax5.set_xlabel("")
ax5.set_ylabel("Nombre de véhicules")

st.pyplot(fig5.figure)

st.write("Notre segmentation a permis de mettre en lumière l'importance des années 1980 pour les véhicules japonais. Un autre nuage de points intéressant à dresser est celui mettant en relation **la puissance au temps mis pour atteindre 60 miles/h**.")

fig6, ax6= plt.subplots()
if not v_ensemble:
	fig6 = sns.scatterplot(data=tampon,y="hp", x="time-to-60", color=blocs[tampon["continent"].unique()[0]], label=tampon["continent"].unique()[0])
else:
	fig6 = sns.scatterplot(data=tampon,y="hp", x="time-to-60", hue="continent", palette=blocs)
ax6.set_title("Les voitures européennes cumulent manquent de puissance et moindres performances")
ax6.set_xlabel("Temps mis pour atteindre 60 miles/h (en secondes)")
ax6.set_ylabel("Puissance (chevaux)")

st.pyplot(fig6.figure)

st.write("Paradoxe notable du côté des Européennes : les **véhicules ne sont ni les plus performants, ni les plus puissants, mais pourtant... les plus gourmands !**")