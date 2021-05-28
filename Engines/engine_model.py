import os, re
import uuid
import platform
import base64
from io import BytesIO
from lxml import etree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Auto_maching_learning.settings import LOG_DIR
from utils.MODEL_DICT import CLEAN_DICT
from utils.mongodb_util import MongoUtil
from utils.logutil import set_log

logger = set_log(os.path.join(LOG_DIR, os.path.split(__file__)[1].split(".")[0]))


class DataCleaningEngine:
    def __init__(self):
        self.db = MongoUtil()

    def check_clean_condition(self, user_name, dataset_name, conditions):
        """
        传入数据集，清洗条件
        :param user_name:
        :param dataset_name:
        :param conditions:
        :return: dataframe 清洗完成后的数据
        """
        try:
            dataset = self.db.find_dataset(user_name, dataset_name)
            df = pd.DataFrame(dataset) if dataset else {}
            if isinstance(df, pd.core.frame.DataFrame):
                for condition in conditions:
                    # cols用于后续的表达式执行
                    try:
                        cols = condition.get("columns", [])
                        clean_method = condition.get("clean_method", "")
                        clean_expression = CLEAN_DICT.get(clean_method, "")

                        # 清洗方法为字符串，说明并没有子方法，可直接执行该方法
                        if clean_expression and isinstance(clean_expression, str):
                            exec(clean_expression)

                        # 清洗方法为字典，说明含有子方法，从映射表中取出对应表达式后执行语句
                        elif clean_expression and isinstance(clean_expression, dict):
                            sub_method = condition.get("sub_method", "")
                            clean_expression = CLEAN_DICT.get(clean_method, {}).get(sub_method)
                            exec(clean_expression)
                    except Exception as e:
                        message = "对{}列进行{}失败！失败原因:{}".format(",".join(cols), clean_method, str(e))
                        raise Exception(message)
            return df
        except Exception as e:
            raise e

    def save_clean_data(self, user_name, dataset_name, new_data):
        """
        将清洗完成的数据集入库
        :param user_name:
        :param dataset_name: 原始数据集名称
        :param new_data: DataFrame
        :return:
        """
        try:
            new_name = "clean_{}".format(dataset_name)
            self.db.upload_dataset(user_name, new_name, new_data)
            return True
        except Exception as e:
            logger.exception(e)
            raise e


class DataMiningEngine:
    def __init__(self):
        self.db = MongoUtil()

    def check_model_conditions(self, username, conditions):
        try:
            dataset_name = conditions.get("dataset_name", "")
            target = conditions.get("target", "")
            metrics = conditions.get("metrics", [])
            dataset = self.db.find_dataset(username, dataset_name)
            df = pd.DataFrame(dataset) if dataset else {}
            model_type = conditions.get("model_type", "")
            if len(df) < 50:
                raise Exception("数据集数量至少需要50条！")
            if model_type == "分类":
                unique_class = len(df[target].unique())
                if unique_class > 50:
                    raise Exception("分类数量过多，暂不支持分类数量大于50的数据集")
                if unique_class != 2 and "ROC曲线" in metrics:
                    raise Exception("ROC曲线仅适用于二分类问题")
        except Exception as e:
            logger.exception(e)
            raise e
        return True

    def run_code(self, username, conditions):
        """
        运行生成的代码
        :param username:
        :param conditions:
                    {"name": "", "dataset_name": "jd_Test_csv",
                    "model_type": "分类", "features": [], "target": "评论",
                    "models": [], "metrics": [],"desc": ""}
        :return:
        """
        try:
            self.check_model_conditions(username, conditions)
            code_filename = "generate_{}_{}.py".format(username, conditions.get("name", ""))
            code_path = os.path.join(os.getcwd(), "temp", code_filename)
            # 替换数据源，读取待运行的代码，将pandas读取部分修改为数据库获取
            with open(code_path, "r", encoding="utf-8") as f:
                code = f.read()
                output_html = "{}{}{}".format(uuid.uuid4(), username, ".html")
                database_source_code = """
from utils.mongodb_util import MongoUtil
DF = pd.DataFrame(MongoUtil().find_dataset("%s","%s"))
OUTPUT_HTML = "%s"
# 将可视化的图片直接插入到结果html中
def insert_png2html(_plt,OUTPUT_HTML=OUTPUT_HTML):
    figfile = BytesIO()
    _plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())  # 将图片转为base64
    figdata_str = str(figdata_png, "utf-8")  # 提取base64的字符串，不然是b'xxx'
    # 保存为.html
    html = '<img src=\"data:image/png;base64,{}\"/>'.format(figdata_str)
    with open(OUTPUT_HTML, 'a+') as f:
        f.write(html)
                """%(username, conditions.get("dataset_name"),output_html)

                code = re.sub(re.compile("# 读取数据(.*?)read_csv\(FILE_PATH\)", re.DOTALL), database_source_code, code)
                output_result_code = """\nres_df.to_html(OUTPUT_HTML) """
                code += output_result_code
                # 删除所有的plt.show()
                code = re.sub("plt.show\(\)","",code)
                # 找到使用matplotlib绘图的结果变量名,批量插入到html
                find_plots = re.findall("plt_(.*) =", code)
                for result_plot in find_plots:
                    plot_name = "plt_{}".format(result_plot)
                    code += "\ninsert_png2html({})".format(plot_name)
                with open("new_code.py", "w") as c:
                    c.write(code)
            exec(code)
            # 代码执行完后，读取生成的html文件拼接
            html_template = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>模型结果</title>
                </head>
                <body>
                <h1>模型性能比较</h1>
                <div>%s</div>
                </body>
                </html>
            """
            # 读取执行上述代码生成的DataFrame表格html文件(dataframe)
            with open(output_html, "r", encoding="utf-8") as f:
                df_html = f.read()
            html_template = html_template % df_html
            os.remove(output_html)

            # 生成html文件到前端static下
            current_path = os.getcwd()
            parent_path, current_file_name = os.path.split(current_path)
            filename = os.path.join(parent_path, "AML-frontend-master/static/%s_%s_model_result.html" % (username, conditions.get("name")))
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_template)
            return os.path.split(filename)[-1]
        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == '__main__':
    username = "lzh3"
    conditions = {"name": "None", "dataset_name": "day_csv",
                  "model_type": "分类", "features": ["mnth", "holiday"], "target": "hum",
                  "models": [], "metrics": [], "desc": ""}
    DataMiningEngine().run_code(username, conditions)
