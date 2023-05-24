MY_TRANSFORMATIONS = []


def transformation(name, key):
    def wrapper(func):
        MY_TRANSFORMATIONS.append((name, key, func))
        return func

    return wrapper


########################################


import os
import importlib

# 获取当前包的路径
package_path = __path__[0]
# package_path = os.path.dirname(__file__)

# 遍历当前文件夹下的所有文件
for file in os.listdir(package_path):
    # 判断文件是否是以 .py 结尾并且不是 __init__.py 文件
    if file.endswith('.py') and file != '__init__.py':
        # 获取模块名，去除文件扩展名
        module_name = file[:-3]

        # 使用 importlib 导入模块
        module = importlib.import_module(f'.{module_name}', __package__)

        # 可选：将导入的模块赋值给当前的命名空间，这样可以直接使用模块中的函数或变量
        # globals()[module_name] = module
