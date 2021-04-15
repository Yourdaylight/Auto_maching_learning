import pandas as pd

FILE_PATH = '%s'
df = None
# 读取数据
if FILE_PATH.split('.')[-1] == 'xls' or FILE_PATH.split('.')[-1] == 'xlsx':
    df = pd.read_excel(FILE_PATH)
else:
    df = pd.read_csv(FILE_PATH)
