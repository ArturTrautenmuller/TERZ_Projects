import numpy as np
import pandas as pd
import variables
import terz
from os import walk


ano_ref = 2020
#GDP
GDP = pd.read_csv(variables.ExtractPath+'\\CSV\\GDP.csv')
GDP.rename(columns={'GDP':'Pais'}, inplace=True)


GDP = pd.melt(GDP,id_vars=['Pais'],var_name='Ano',value_name='GDP')
GDP = GDP[GDP['Pais'].notnull()]

GDP['GDP'] = np.where(GDP['GDP'] == 'no data', 0, GDP['GDP'])
GDP['GDP'] = np.where(GDP['GDP'].isnull(), 0, GDP['GDP'])
GDP['Ano'] = pd.to_numeric(GDP['Ano'], errors='coerce').astype('Int64')
GDP = GDP[GDP['Ano'] <= ano_ref]

#GDP-PPP

GDP_PPP = pd.read_csv(variables.ExtractPath+'\\CSV\\GDP-PPP.csv')
GDP_PPP.rename(columns={'GDP':'Pais'}, inplace=True)


GDP_PPP = pd.melt(GDP_PPP,id_vars=['Pais'],var_name='Ano',value_name='GDP_PPP')
GDP_PPP = GDP_PPP[GDP_PPP['Pais'].notnull()]

GDP_PPP['GDP_PPP'] = np.where(GDP_PPP['GDP_PPP'] == 'no data', 0, GDP_PPP['GDP_PPP'])
GDP_PPP['GDP_PPP'] = np.where(GDP_PPP['GDP_PPP'].isnull(), 0, GDP_PPP['GDP_PPP'])
GDP_PPP['Ano'] = pd.to_numeric(GDP_PPP['Ano'], errors='coerce').astype('Int64')
GDP_PPP = GDP_PPP[GDP_PPP['Ano'] <= ano_ref]

#GDP_PERCAPITA

GDP_PerCapita = pd.read_csv(variables.ExtractPath+'\\CSV\\GDP_PerCapita.csv')
GDP_PerCapita.rename(columns={'GDP per capita':'Pais'}, inplace=True)


GDP_PerCapita = pd.melt(GDP_PerCapita,id_vars=['Pais'],var_name='Ano',value_name='GDP_Percapita')
GDP_PerCapita = GDP_PerCapita[GDP_PerCapita['Pais'].notnull()]

GDP_PerCapita['GDP_Percapita'] = np.where(GDP_PerCapita['GDP_Percapita'] == 'no data', 0, GDP_PerCapita['GDP_Percapita'])
GDP_PerCapita['GDP_Percapita'] = np.where(GDP_PerCapita['GDP_Percapita'].isnull(), 0, GDP_PerCapita['GDP_Percapita'])
GDP_PerCapita['Ano'] = pd.to_numeric(GDP_PerCapita['Ano'], errors='coerce').astype('Int64')
GDP_PerCapita = GDP_PerCapita[GDP_PerCapita['Ano'] <= ano_ref]

#GDP_PPP_Percapita

GDP_PerCapita_PPP = pd.read_csv(variables.ExtractPath+'\\CSV\\GDP_PerCapita-PPP.csv')
GDP_PerCapita_PPP.rename(columns={'GDP per capita':'Pais'}, inplace=True)


GDP_PerCapita_PPP = pd.melt(GDP_PerCapita_PPP,id_vars=['Pais'],var_name='Ano',value_name='GDP_Percapita_PPP')
GDP_PerCapita_PPP = GDP_PerCapita_PPP[GDP_PerCapita_PPP['Pais'].notnull()]

GDP_PerCapita_PPP['GDP_Percapita_PPP'] = np.where(GDP_PerCapita_PPP['GDP_Percapita_PPP'] == 'no data', 0, GDP_PerCapita_PPP['GDP_Percapita_PPP'])
GDP_PerCapita_PPP['GDP_Percapita_PPP'] = np.where(GDP_PerCapita_PPP['GDP_Percapita_PPP'].isnull(), 0, GDP_PerCapita_PPP['GDP_Percapita_PPP'])
GDP_PerCapita_PPP['Ano'] = pd.to_numeric(GDP_PerCapita_PPP['Ano'], errors='coerce').astype('Int64')
GDP_PerCapita_PPP = GDP_PerCapita_PPP[GDP_PerCapita_PPP['Ano'] <= ano_ref]

#Fato

fato = pd.merge(GDP,GDP_PPP,how='outer',on=['Pais','Ano'])
fato = pd.merge(fato,GDP_PerCapita,how='outer',on=['Pais','Ano'])
fato = pd.merge(fato,GDP_PerCapita_PPP,how='outer',on=['Pais','Ano'])
fato = fato.fillna(0)





#Inflation

inflation = pd.read_csv(variables.ExtractPath+'\\CSV\\inflation_data.csv')
inflation.drop('inflation rate',axis=1,inplace=True)
inflation.rename(columns={'year':'Ano'}, inplace=True)
inflation = inflation[inflation['Ano'] >= 1980][inflation['Ano'] <= ano_ref]

amount_2010 = inflation[inflation['Ano'] == 2010]['amount'].values[0]

fato = pd.merge(fato,inflation,how='outer',on=['Ano'])

fato['GDP'] = fato['GDP'].astype(float)
fato['GDP_PPP'] = fato['GDP_PPP'].astype(float)
fato['GDP_Percapita'] = fato['GDP_Percapita'].astype(float)
fato['GDP_Percapita_PPP'] = fato['GDP_Percapita_PPP'].astype(float)

fato['GDP'] = np.where(fato['GDP_Percapita'] < 0.1, 0, fato['GDP'])
fato['GDP_PPP'] = np.where(fato['GDP_Percapita_PPP'] < 0.1, 0, fato['GDP_PPP'])


fato['GDP'] = fato['GDP'] * 1000000000
fato['GDP_2010_dolar'] = fato['GDP'] * (amount_2010 / fato['amount'])
#fato['GDP_2010_dolar'] = fato['GDP_2010_dolar'].astype(int)


fato['GDP_PPP'] = fato['GDP_PPP'] * 1000000000
fato['GDP_PPP_2010_dolar'] = fato['GDP_PPP'] * (amount_2010 / fato['amount'])
#fato['GDP_PPP_2010_dolar'] = fato['GDP_PPP_2010_dolar'].astype(int)


fato['GDP_Percapita_2010_dolar'] = fato['GDP_Percapita'] * (amount_2010 / fato['amount'])
#fato['GDP_Percapita_2010_dolar'] = fato['GDP_Percapita_2010_dolar'].astype(int)


fato['GDP_Percapita_PPP_2010_dolar'] = fato['GDP_Percapita_PPP'] * (amount_2010 / fato['amount'])
#fato['GDP_Percapita_PPP_2010_dolar'] = fato['GDP_Percapita_PPP_2010_dolar'].astype(int)

fato.drop('amount',axis=1,inplace=True)

fato['Pais'] = fato['Pais'].str.replace(',','-')

#correct wrong contries names
countries = pd.read_csv(variables.ResourcesPath+'\\MapPaises.csv')
fato = pd.merge(fato,countries,how='left',on=['Pais'])

fato['Pais_Rel'] = np.where(fato['Pais_Rel'].isnull(), fato['Pais'], fato['Pais_Rel'])
fato.drop('Pais',axis=1,inplace=True)
fato.rename(columns={'Pais_Rel':'Pais'}, inplace=True)

fato['Populacao'] = np.where(fato['GDP'].isnull(),0,fato['GDP']/fato['GDP_Percapita'])
fato['Populacao'] = np.where(fato['Populacao'].isnull(), 0, fato['Populacao'])

anoGrouper = fato.groupby(['Ano'],dropna=False)
total_ano = anoGrouper['Populacao'].sum().to_frame(name = 'Populacao').reset_index()
total_ano = pd.merge(total_ano,anoGrouper['GDP'].sum().to_frame(name = 'GDP_Ano').reset_index(),how='left',on=['Ano'])
total_ano = pd.merge(total_ano,anoGrouper['GDP_2010_dolar'].sum().to_frame(name = 'GDP_2010_dolar_Ano').reset_index(),how='left',on=['Ano'])
total_ano = pd.merge(total_ano,anoGrouper['GDP_PPP'].sum().to_frame(name = 'GDP_PPP_Ano').reset_index(),how='left',on=['Ano'])
total_ano = pd.merge(total_ano,anoGrouper['GDP_PPP_2010_dolar'].sum().to_frame(name = 'GDP_PPP_2010_dolar_Ano').reset_index(),how='left',on=['Ano'])

total_ano['GDP_Percapita_Ano'] = total_ano['GDP_Ano']/total_ano['Populacao']
total_ano['GDP_Percapita_2010_dolar_Ano'] = total_ano['GDP_2010_dolar_Ano']/total_ano['Populacao']
total_ano['GDP_Percapita_PPP_Ano'] = total_ano['GDP_PPP_Ano']/total_ano['Populacao']
total_ano['GDP_Percapita_PPP_2010_dolar_Ano'] = total_ano['GDP_PPP_2010_dolar_Ano']/total_ano['Populacao']

fato.to_csv(variables.TransformPath+'\\Fato.csv',index=False)
total_ano.to_csv(variables.TransformPath+'\\TotalAno.csv',index=False)

# print whole sheet data

print(GDP)
print(GDP_PPP)
print(GDP_PerCapita)
print(GDP_PerCapita_PPP)
print(fato)

terz.importDataFrame(dataframePath=variables.TransformPath+'\\Fato.csv',reportid='123488',user='arturtmuller13@gmail.com',password='Password190')
terz.importDataFrame(dataframePath=variables.TransformPath+'\\TotalAno.csv',reportid='123488',user='arturtmuller13@gmail.com',password='Password190')

#print(inflation)
#print(amount_2010)


