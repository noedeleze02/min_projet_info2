import pandas as pd
#importation du fichier csv pour convertir en dataframe et traiter les données
df_chomage = pd.read_csv("https://www.bfs.admin.ch/bfsstatic/dam/assets/20964153/master", sep = ';')
#remplacer les codes géographiques dans le dataframe
geo = {'CH':'Suisse','CH011':'Vaud','CH012':'Valais','CH013':'Genève','CH021':'Berne','CH022':'Fribourg','CH023':'Soleure','CH024':'Neuchâtel','CH025':'Jura','CH031':'Bâle-Ville','CH032':'Bâle-Campagne','CH033':'Argovie','CH040':'Zurich','CH051':'Glaris','CH052':'Schaffhouse','CH053':'Appenzell Rhodes-Extérieures','CH054':'Appenzell Rhodes-Intérieures','CH055':'Saint-Gall','CH056':'Grisons','CH057':'Thurgovie','CH061':'Lucerne','CH062':'Uri','CH063':'Schwyz','CH064':'Obwald','CH065':'Nidwald','CH066':'Zoug','CH070':'Tessin'}
df_chomage = df_chomage.replace(geo)
#remplacer les codes unité dans le dataframe
unit = {'pers':'Nombre de personnes','HH':'Nombre de ménages', 'pers in %':'Pourcentage de personnes'}
df_chomage = df_chomage.replace(unit)
#remplacer les codes Obs_Status dans le dataframe
obs_status = {'A':'Valeur normales','L':'Valeur confidentielle','U':'Faible fiabilité'}
df_chomage = df_chomage.replace(obs_status)
#remplacer les codes POP1564 dans le dataframe
##pop = {'1':'Pop. résid. perm. de 15 à 64 ans'}
##df_chomage = df_chomage['POP1564'].replace(pop)
#remplacer les codes POP1564 dans le dataframe
##erwp = {'0':'Autres personnes','1':'Personnes actives'}
##df_chomage['ERWP'] = df_chomage.replace(erwp)
print(df_chomage)
#verfier s'il y a des données pour toutes les années (2010 à 2020)
for i in range(2010, 2021):
    if any(df_chomage.TIME_PERIOD == i):
        print("Il y a des données pour l'année", i)
    else:
        print("Attention ! Les données de l'année", i, "ne sont pas complètes.")
