import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px



st.title('Données des voitures')

st.write("Descriptions")

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df = pd.read_csv(link)
df


# boutons radio pour filtrer par région
region = st.radio("Sélectionnez une région :", ('Toutes les régions', 'US', 'Europe', 'Japan'))

if region == 'Toutes les régions':
    filtered_df = df
else:
    # Convertion de la région sélectionnée en majuscules pour correspondre à la casse des données
    region = region.upper()
    filtered_df = df[df['continent'].str.upper() == region]

# Suppession des colonnes non numériques du calcul de la corrélation
numeric_columns = filtered_df.select_dtypes(include=['number']).columns
corr = filtered_df[numeric_columns].corr()

#  heatmap de corrélation
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title("Corrélation entre les variables des voitures")
ax.tick_params(rotation=45)
st.pyplot(fig)

# Diagramme en secteurs (Pie chart)
continent_counts = filtered_df['continent'].value_counts()

fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(continent_counts, labels=continent_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
ax.set_title('Répartition des voitures par continent')
st.pyplot(fig)

# Diagramme en violon (Violin plot)
fig, ax = plt.subplots(figsize=(10, 8))
sns.violinplot(x='continent', y='hp', data=filtered_df, palette='pastel', ax=ax)
plt.xlabel('Continent')
plt.ylabel('Horsepower (hp)')
plt.title('Distribution de la variable Horsepower (hp) par continent')
st.pyplot(fig)

#  DataFrame pour le diagramme Sunburst
sunburst_df = filtered_df.groupby(['year', 'continent']).size().reset_index(name='count')

#  diagramme Sunburst avec Plotly Express
fig = px.sunburst(sunburst_df, path=['year', 'continent'], values='count', title='Répartition des voitures par année et continent')
st.plotly_chart(fig)