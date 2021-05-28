# 模型性能评估
def model_performance_evaluation(model_name, test, pred, spend_time):
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.metrics import roc_curve, auc
    acc = accuracy_score(test, pred)
    print(model_name, '| 准确率: %.4f' % acc)
    pred = pred.astype('float64')
    # auc曲线使用于二分类问题
    roc_auc = "auc曲线适用于二分类问题"
    if len(set(pred))==2 and len(set(test))==2:
        false_positive_rate, true_positive_rate, thresholds = roc_curve(test, pred)
        roc_auc = auc(false_positive_rate, true_positive_rate)
        print(model_name, '| AUC: %.4f' % roc_auc)
    cm = confusion_matrix(test, pred)
    miss_report = cm[0][1] / (1.0 * cm[0][1] + cm[1][1])
    false_report = cm[1][0] / (1.0 * cm[0][0] + cm[1][0])
    print(model_name, "| 漏报率为：%.4f" % miss_report)
    print(model_name, "| 误报率为：%.4f" % false_report)
    print(model_name, "| 训练时长（秒）：%.4f" % spend_time)
    return acc, roc_auc, miss_report, false_report


# 使用模型预测并评估
evaluation_dimensions = ["模型名称", "准确率", "AUC", "漏报率", "误报率", "训练时长(秒)"]
compare_result = {dimension: [] for dimension in evaluation_dimensions}
for spend_time, fit_model in fit_models.items():
    y_pred = fit_model.predict(X_test)
    print("====================")
    model_name = str(fit_model).split("(")[0]
    acc, roc_auc, miss_report, false_report = model_performance_evaluation(model_name, y_test, y_pred, spend_time)
    compare_result["模型名称"].append(model_name)
    compare_result["准确率"].append(acc)
    compare_result["AUC"].append(roc_auc)
    compare_result["漏报率"].append(miss_report)
    compare_result["误报率"].append(false_report)
    compare_result["训练时长(秒)"].append(spend_time)

res_df = pd.DataFrame(compare_result)
print(res_df)
