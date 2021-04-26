
# 选择特征
X = DF[FEATURES]
# 模型训练,key为模型训练的时间,value为训练好的模型
fit_models = {}
for model in MODEL:
    start_time = time.time()
    fit_model= model.fit(X)
    end_time = time.time()
    spend_time = end_time - start_time
    fit_models[spend_time] = fit_model




