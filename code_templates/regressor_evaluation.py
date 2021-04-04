
# 模型性能评估
def model_performance_evaluation(model_name, test, pred, spend_time):
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import mean_absolute_error
    from sklearn.metrics import r2_score
    mse = mean_squared_error(test, pred)
    mae = mean_absolute_error(test, pred)
    r2 = r2_score(test, pred)
    print(model_name, "| 均方误差: %.4f" % mse)
    print(model_name, "| 平均绝对误差: %.4f" % mae)
    print(model_name, "| 决定系数: %.4f" % r2)
    print(model_name, "| 训练时长(秒): %.4f" % spend_time)
    return mse, mae, r2


# 使用模型预测并评估
evaluation_dimensions = ["模型名称", "均方误差", "平均绝对误差", "决定系数", "训练时长(秒)"]
compare_result = {dimension: [] for dimension in evaluation_dimensions}
for spend_time, fit_model in fit_models.items():
    y_pred = fit_model.predict(X_test)
    print("====================")
    model_name = str(fit_model).split("(")[0]
    mse, mae, r2 = model_performance_evaluation(model_name, y_test, y_pred, spend_time)
    compare_result["模型名称"].append(model_name)
    compare_result["均方误差"].append(mse)
    compare_result["平均绝对误差"].append(mae)
    compare_result["决定系数"].append(r2)
    compare_result["训练时长(秒)"].append(spend_time)
res_df = pd.DataFrame(compare_result)
print(res_df)