import platform
import os
import re
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties

# ==============================
# 通用字体设置工具
# ==============================
def get_chinese_font():
    """尝试获取可用的中文字体"""
    system = platform.system()
    font_names = ['Microsoft YaHei', 'SimHei', 'SimSun', 'PingFang SC', 'Heiti TC', 'Droid Sans Fallback']
    
    # 优先检查 Windows 常用路径
    if system == 'Windows':
        win_fonts = [r'C:\Windows\Fonts\msyh.ttc', r'C:\Windows\Fonts\simhei.ttf']
        for f in win_fonts:
            if os.path.exists(f):
                try:
                    prop = FontProperties(fname=f)
                    return prop
                except:
                    pass
    
    # 检查系统已安装字体
    for name in font_names:
        try:
            path = fm.findfont(fm.FontProperties(family=name))
            if os.path.exists(path):
                return FontProperties(fname=path)
        except:
            continue
            
    # 如果都失败，返回默认
    return FontProperties(family='sans-serif')

def configure_mpl_fonts():
    """配置 Matplotlib 全局字体"""
    font_prop = get_chinese_font()
    font_name = font_prop.get_name()
    plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    return font_prop

# ==============================
# 通用排序工具
# ==============================
def sort_key(name):
    """生测编号排序逻辑"""
    name_str = str(name).strip()
    if '阿维菌素' in name_str: return (998, 0, 0)
    if 'CK' in name_str or 'ck' in name_str or '对照' in name_str: return (999, 0, 0)
    
    roman_map = {'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅳ': 4, 'Ⅴ': 5, 'Ⅵ': 6, 'Ⅶ': 7, 'Ⅷ': 8, 'Ⅸ': 9, 'Ⅹ': 10,
                 'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
    
    m = re.match(r'^([ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩIVX]+)\s*(\d+)-(\d+)$', name_str)
    if m:
        return (roman_map.get(m.group(1), 0), int(m.group(2)), int(m.group(3)))
    
    nums = re.findall(r'\d+', name_str)
    if nums:
        return (997, int(nums[0]), int(nums[1]) if len(nums) > 1 else 0)
    
    return (996, 0, 0)