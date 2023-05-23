from . import transformation

@transformation("TESTING", "testing")
def testing_transform(v, i, secs):
    """测试"""
    return "testing"