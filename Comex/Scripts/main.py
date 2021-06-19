import pandas as pd
import variables
import terz
from os import walk

exportsObj = {'Ano':[],
              'Mes':[],
              'Países':[],
              'UF do Produto':[],
              'Descrição NCM':[],
              'Descrição SH4':[],
              'Descrição SH2':[],
              'Valor FOB (US$)':[]}
exports = pd.DataFrame(data=exportsObj)

for (dirpath, dirnames, filenamesE) in walk(variables.ExtractPath+'\\exports'):
    break
print(filenamesE)
for file in filenamesE:
    month = file.replace('.csv','').split('_')[0]
    year = file.replace('.csv','').split('_')[1]
    exportsMonth = pd.read_csv(variables.ExtractPath+'\\exports\\'+file)
    exportsMonth.drop('Código NCM',axis=1, inplace=True)
    exportsMonth.drop('Codigo SH4', axis=1, inplace=True)
    exportsMonth.drop('Codigo SH2', axis=1, inplace=True)
    exportsMonth['Ano'] = year
    exportsMonth['Mes'] = month
    exports = pd.concat([exports,exportsMonth])

exports.rename(columns={'Países':'Pais'}, inplace=True)
exports.rename(columns={'UF do Produto':'UF'}, inplace=True)
exports.rename(columns={'Descrição NCM':'NCM'}, inplace=True)
exports.rename(columns={'Descrição SH4':'SH4'}, inplace=True)
exports.rename(columns={'Descrição SH2':'SH2'}, inplace=True)
exports.rename(columns={'Valor FOB (US$)':'Valor_Exportacao'}, inplace=True)

exports.to_csv(variables.TransformPath+'\\ExportDetalhado.csv',index=False)

importsObj = {'Ano':[],
              'Mes':[],
              'Países':[],
              'UF do Produto':[],
              'Descrição NCM':[],
              'Descrição SH4':[],
              'Descrição SH2':[],
              'Valor FOB (US$)':[]}
imports = pd.DataFrame(data=importsObj)

for (dirpathI, dirnamesI, filenamesI) in walk(variables.ExtractPath+'\\imports'):
    break
print(filenamesI)
for file in filenamesI:
    month = file.replace('.csv','').split('_')[0]
    year = file.replace('.csv','').split('_')[1]

    importsMonth = pd.read_csv(variables.ExtractPath+'\\imports\\'+file)
    importsMonth.drop('Código NCM',axis=1, inplace=True)
    importsMonth.drop('Codigo SH4', axis=1, inplace=True)
    importsMonth.drop('Codigo SH2', axis=1, inplace=True)
    importsMonth['Ano'] = year
    importsMonth['Mes'] = month
    imports = pd.concat([imports,importsMonth])

imports.rename(columns={'Países':'Pais'}, inplace=True)
imports.rename(columns={'UF do Produto':'UF'}, inplace=True)
imports.rename(columns={'Descrição NCM':'NCM'}, inplace=True)
imports.rename(columns={'Descrição SH4':'SH4'}, inplace=True)
imports.rename(columns={'Descrição SH2':'SH2'}, inplace=True)
imports.rename(columns={'Valor FOB (US$)':'Valor_Importacao'}, inplace=True)


imports.to_csv(variables.TransformPath+'\\ImportDetalhado.csv',index=False)


#Resumida

exports.drop('NCM',axis=1,inplace=True)
exports.drop('SH4',axis=1,inplace=True)

eGrouper = exports.groupby(['Ano','Mes','Pais','UF','SH2'],dropna=False)
exports = eGrouper['Valor_Exportacao'].sum().to_frame(name = 'Valor_Exportacao').reset_index()

exports.to_csv(variables.TransformPath+'\\ExportSintetico.csv',index=False)


imports.drop('NCM',axis=1,inplace=True)
imports.drop('SH4',axis=1,inplace=True)

iGrouper = imports.groupby(['Ano','Mes','Pais','UF','SH2'],dropna=False)
imports = iGrouper['Valor_Importacao'].sum().to_frame(name = 'Valor_Importacao').reset_index()

imports.to_csv(variables.TransformPath+'\\ImportSintetico.csv',index=False)

#Fato

fato = pd.merge(exports,imports,how='outer',on=['Ano','Mes','Pais','UF','SH2'])
fato = fato.fillna(0)


countries = pd.read_csv(variables.ResourcesPath+'\\Paises.csv')
fato = pd.merge(fato,countries,how='left',on=['Pais'])
fato.fillna('None')

fato['Pais'] = fato['Pais'].str.replace(',','&')
fato['UF'] = fato['UF'].str.replace(',','&')
fato['SH2'] = fato['SH2'].str.replace(',','&')
#fato = fato.head(n=100)
print(fato)
fato.to_csv(variables.TransformPath+'\\Fato.csv',index=False)

terz.importDataFrame(dataframePath=variables.TransformPath+'\\Fato.csv',reportid='123480',user='arturtmuller13@gmail.com',password='Password190')