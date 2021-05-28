# ==============roc曲线绘制================
def plot_ROC_curve(y_test, y_predict, save_name="roc"):
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_predict)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    plt.title('ROC')
    plt.plot(false_positive_rate, true_positive_rate, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.ylabel('TPR')
    plt.xlabel('FPR')
    plt.savefig(save_name+".jpg")
    plt.show()
    return plt

plt_roc = plot_ROC_curve(y_test, y_pred)