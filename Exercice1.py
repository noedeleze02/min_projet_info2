##  étape 1

import pandas as pd
#importation des widgets
from ipywidgets import widgets
from ipywidgets import interact
#création des widgets
import pygal
# affichage pygal dans notebook
from IPython.display import display, HTML
base_html = """
  <!DOCTYPE html><html><head><script type="text/javascript" src="https://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js""></script></head>
  <body><figure>{rendered_chart}</figure></body></html>
"""


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

#remplacer les codes POP1564
df_pop1564 = df_chomage['POP1564']
pop = {'1':'Pop. résid. perm. de 15 à 64 ans'}
df_pop1564 = df_pop1564.replace(pop)
df_chomage['POP1564']=df_pop1564

#remplacer les codes ERWL
df_erwl = df_chomage['ERWL']
erwl = {'0':'Autres personnes','1': 'Personnes au chômage'}
df_erwl = df_erwl.replace(erwl)
df_chomage['ERWL']=df_erwl

#remplacer les codes ERWP dans le dataframe
df_erwp = df_chomage['ERWP']
erwp = {'0':'Autres personnes','1':'Personnes actives'}
df_erwp = df_erwp.replace(erwp)
df_chomage['ERWP'] = df_erwp


###   étape 2

#traitement données canton de Vaud
df_vaud = df_chomage.query("GEO=='Vaud'")

chomeurs_num= df_vaud.query("ERWL=='Personnes au chômage' and UNIT_MEA =='Nombre de personnes'")
liste_chomeurs = chomeurs_num['OBS_VALUE'].tolist()

Population = df_vaud.query("POP1564=='Total' and ERWP =='Total' and UNIT_MEA=='Nombre de personnes'")

Population['chomeurs']= liste_chomeurs

Population['reste_popu'] = Population['OBS_VALUE']-Population['chomeurs']

reste_popu = Population['reste_popu']
annees = Population['TIME_PERIOD']

#création graphique 1                      
import matplotlib.pyplot as plt

plt.title('Chômeurs vs Population Vaudoise', fontsize = 18)
plt.xlabel('Années')
plt.ylabel('Nombre de personnes')
plt.bar(annees, liste_chomeurs, label='personnes au chomage', color ='r')
plt.bar(annees, reste_popu, bottom=liste_chomeurs, label ='reste de la population', color = 'b')
plt.legend()
plt.show()


## Création graphique 2
plt.title('Evolution du chômage dans le canton de Vaud', fontsize = 18)
plt.xlabel('Années')
plt.ylabel('Nombre de personnes')
plt.plot(annees, liste_chomeurs, color = 'r')
plt.show()


###   étape 3

## a partir de cette étape, les données sur la population active ne sont plus utiles
df_chomage = df_chomage.drop(columns=['ERWP'])



# ajout de données à afficher (un dictionnaire contenant comme key le code du canton : la valeur)


cantons_dict = {'Zoug': 'kt-zg', 'Vaud': 'kt-vd', 'Valais': 'kt-vs', 'Genève': 'kt-ge', 'Berne': 'kt-be',
                'Fribourg': 'kt-fr', 'Soleure': 'kt-so', 'Neuchâtel': 'kt-ne', 'Jura': 'kt-ju', 'Bâle-Ville': 'kt-bs',
                'Bâle-Campagne': 'kt-bl', 'Argovie': 'kt-ag', 'Zurich': 'kt-zh', 'Glaris': 'kt-gl', 'Schaffhouse': 'kt-sh',
                'Appenzell Rhodes-Extérieures': 'kt-ar', 'Appenzell Rhodes-Intérieures': 'kt-ai', 'Saint-Gall': 'kt-sg', 'Grisons': 'kt-gr', 'Thurgovie': 'kt-tg',
                'Lucerne': 'kt-lu', 'Uri': 'kt-ur', 'Schwyz': 'kt-sz', 'Obwald': 'kt-ow', 'Nidwald': 'kt-nw',
                'Tessin': 'kt-ti'}


def f(a, b, c, d, e):
    display(a)
    display(b)
    display(c)
    display(d)
    display(e)

   # recherche des données correspondantes aux en-têtes choisies
    df_chomage_precis = df_chomage.query("TIME_PERIOD==@b and UNIT_MEA == @c and POP1564 == @d and ERWL == @e")
    df_chomage_fin = df_chomage_precis[['GEO','OBS_VALUE']].replace(cantons_dict)


    liste_code = df_chomage_fin['GEO']
    liste_valeur = df_chomage_fin['OBS_VALUE']



    dicto = dict(zip(liste_code, liste_valeur))

    #création de la carte
    ch_chart = pygal.maps.ch.Cantons()
    ch_chart.title = 'Chomage des cantons en ' + str(b)
    ch_chart.add('chomeurs', dicto)

    carte_suisse=ch_chart.render(is_unicode=True)

    display(HTML(base_html.format(rendered_chart=carte_suisse)))
#mise en interaction des widgets avec la carte
interact(f,a = widgets.RadioButtons(options = ['FR', 'EN', 'DE','IT'] , description = 'Langue:', disabled = False), b=widgets.IntSlider(min = 2010, max = 2020, step = 1, description = 'time', disabled = False, orientation = 'horizontal'), c = widgets.Dropdown(options = ['Nombre de personnes', 'Nombre de ménages','Pourcentage de personnes'], description = 'unit', disabled = False), d = widgets.Dropdown(options = ['Pop. résid. perm. de 15 à 64 ans', 'Total'], description = 'population'), e = widgets.Dropdown(options = ['Autres personnes', 'Personnes au chômage', 'Total'], description = 'chomage'))
