MY_TRANSFORMATIONS = []


def transformation(name, key):
    def wrapper(func):
        MY_TRANSFORMATIONS.append((name, key, func))
        return func

    return wrapper


########################################


import pkgutil

# 获取当前包的路径
package_path = __path__[0]

# 遍历当前包下的所有模块
for _, module_name, _ in pkgutil.walk_packages([package_path]):
    # 使用 importlib 导入模块
    module = __import__(f'{__name__}.{module_name}', fromlist=[module_name])

    # 可选：将导入的模块赋值给当前的命名空间，这样可以直接使用模块中的函数或变量
    globals()[module_name] = module
