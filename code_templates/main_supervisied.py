
# 选择特征
y =DF[TARGET]
X = DF[FEATURES]
# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# 模型训练,key为模型训练的时间,value为训练好的模型
fit_models = {}
for model in MODEL:
    start_time = time.time()
    fit_model = model.fit(X_train, y_train)
    end_time = time.time()
    spend_time = start_time - end_time
    fit_models[spend_time] = fit_model
# 模型评估



