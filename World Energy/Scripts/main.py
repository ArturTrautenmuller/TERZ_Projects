import numpy as np
import pandas as pd
import variables
import terz
import Primary
import Eletricity
import Geral

Primary.TransformPrimary()
Eletricity.TransformEletricity()
Geral.Geral()

terz.importDataFrame(dataframePath=variables.TransformPath+'\\Fato.csv',reportid='123489',user='arturtmuller13@gmail.com',password='Password190')
terz.importDataFrame(dataframePath=variables.TransformPath+'\\Primary.csv',reportid='123489',user='arturtmuller13@gmail.com',password='Password190')
terz.importDataFrame(dataframePath=variables.TransformPath+'\\Eletricity.csv',reportid='123489',user='arturtmuller13@gmail.com',password='Password190')







