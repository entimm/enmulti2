"""测试引导：把包根目录的父目录（Packages/）加入 sys.path，使 enmulti2 可作为包导入。"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
