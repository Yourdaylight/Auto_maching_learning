# 模型性能评估
def model_performance_evaluation(model_name, X, labels, spend_time):
    from sklearn.metrics import calinski_harabaz_score
    from sklearn.metrics import silhouette_score
    sc = silhouette_score(X,labels)
    chs = calinski_harabaz_score(X,labels)
    print(model_name, "| 轮廓系数: %.4f" % sc)
    print(model_name, "|  Calinski-Harabaz index: %.4f" % chs)
    print(model_name, "| 训练时长(秒): %.4f" % spend_time)
    return sc,chs


# 使用模型预测并评估
evaluation_dimensions = ["模型名称", "轮廓系数", "Calinski-Harabaz-index", "训练时长(秒)"]
compare_result = {dimension: [] for dimension in evaluation_dimensions}

for spend_time, fit_model in fit_models.items():
    print("====================")
    model_name = str(fit_model).split("(")[0]
    labels = fit_model.labels_
    sc, chs = model_performance_evaluation(model_name, X, labels, spend_time)
    compare_result["模型名称"].append(model_name)
    compare_result["轮廓系数"].append(sc)
    compare_result["Calinski-Harabaz-index"].append(chs)
    compare_result["训练时长(秒)"].append(spend_time)
res_df = pd.DataFrame(compare_result)
print(res_df)