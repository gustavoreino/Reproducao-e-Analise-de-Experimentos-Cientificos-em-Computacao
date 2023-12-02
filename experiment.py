import os
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Reads file names
mypath = './APKs/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Executes the QARK commands

first_part = 'qark --apk ./APKs/'
second_part = ' --report-type html --report-path '
results = './results/'

resultsExist = os.path.exists(results)
if not resultsExist:
    os.makedirs(results)

for x in range(len(files)):
    direcComponents = [results, files[x].removesuffix('.apk')]
    resultPath = "".join(direcComponents)
    isExist = os.path.exists(resultPath)
    if not isExist:
        os.makedirs(resultPath)
    list = [first_part, files[x], second_part, resultPath]
    cmd = "".join(list)
    os.system(cmd)

# Gathers the results

vulnsNumber = np.zeros(len(files), dtype=int)

for x in range(len(files)):
    aux = files[x].removesuffix('.apk')
    pathList = [results, aux, '/report.html']
    reportPath = "".join(pathList)
    with open(reportPath, 'r') as f:
        file = f.read()
    soup = BeautifulSoup(file, features='lxml')
    names = soup.find_all('h2')
    setNames = set(names)
    vulnsNumber[x] = len(setNames)
    f.close()

# Writes results on a graph

columnName = "Values"
dataFrame = pd.DataFrame({columnName:vulnsNumber})
sns.displot(data=dataFrame, x="Values", kind="ecdf")
plt.savefig('graph.png')