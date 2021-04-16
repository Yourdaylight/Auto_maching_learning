import time
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import *
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

FILE_PATH = '%s'
# 读取数据
if FILE_PATH.split('.')[-1] == 'xls' or FILE_PATH.split('.')[-1] == 'xlsx':
    DF=pd.read_excel(FILE_PATH)
else:
    DF=pd.read_csv(FILE_PATH)