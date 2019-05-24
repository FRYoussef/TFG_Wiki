import pandas as pd

acido = pd.DataFrame(pd.read_csv('ADN/ADN.csv'),index = None)
"""
airbus = pd.DataFrame(pd.read_csv('Airbus_A380/airbus_A380.csv'),index = None)
angkor = pd.DataFrame(pd.read_csv('Angkor_Wat/angkor_wat.csv'),index = None)
bifaz = pd.DataFrame(pd.read_csv('Bifaz/bifaz.csv'),index = None)
homer = pd.DataFrame(pd.read_csv('Homer_Simpson/homer_simpson.csv'),index = None)
leche = pd.DataFrame(pd.read_csv('Leche/leche.csv'),index = None)
odin = pd.DataFrame(pd.read_csv('Odin/odin.csv'),index = None)
tierra = pd.DataFrame(pd.read_csv('Tierra/tierra.csv'),index = None)
"""

acido = acido.drop('intentionality',axis=1)
"""
airbus = airbus.drop('intentionality',axis=1)
angkor = angkor.drop('intentionality',axis=1)
bifaz = bifaz.drop('intentionality',axis=1)
homer = homer.drop('intentionality',axis=1)
leche = leche.drop('intentionality',axis=1)
odin = odin.drop('intentionality',axis=1)
tierra = tierra.drop('intentionality',axis=1)
"""


acido.to_csv('acido.csv',index = False)
"""
airbus.to_csv('airbus.csv',index = False)
angkor.to_csv('angkor.csv',index = False)
bifaz.to_csv('bifaz.csv',index = False)
homer.to_csv('homer.csv',index = False)
leche.to_csv('leche.csv',index = False)
odin.to_csv('odin.csv',index = False)
tierra.to_csv('tierra.csv',index = False)
"""
    
