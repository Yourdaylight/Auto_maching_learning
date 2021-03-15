

if FILE_PATH.split('.')[-1]=='xls' or FILE_PATH.split('.')[-1]=='xlsx':
    DF=pd.read_excel(FILE_PATH)
else:
    DF=pd.read_csv(FILE_PATH)

y =DF[TARGET]
X = DF[FEATURES]
# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


# 模型训练
model = MODEL.fit(X_train, y_train)
#预测
y_pred = model.predict(X_test)
# 模型评估



