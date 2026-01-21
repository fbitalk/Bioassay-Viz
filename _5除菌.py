# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import matplotlib.font_manager as fm
import os

# ===========================
# 1. 读取 Excel 数据
# ===========================
file_path = r"C:\Users\11142\Downloads\无cx.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet3')

print(f"✓ 成功读取数据，共 {len(df)} 行")
print(f"列名: {list(df.columns)}")

# ===========================
# 2. 中文字体 & 学术风格设置
# ===========================
# 查找可用的中文字体
chinese_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi', 'FangSong']
available_font = None
font_path_found = None
for font_name in chinese_fonts:
    try:
        font_path = fm.findfont(fm.FontProperties(family=font_name))
        if font_path and os.path.exists(font_path):
            available_font = font_name
            font_path_found = font_path
            break
    except:
        continue

# 设置字体
if available_font:
    rcParams['font.sans-serif'] = [available_font, 'Arial', 'DejaVu Sans']
    print(f"使用字体: {available_font} ({font_path_found})")
else:
    rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
    print("使用默认字体设置")

rcParams['axes.unicode_minus'] = False  # 负号正常显示

# 创建字体属性对象用于所有文本
if available_font:
    text_font = fm.FontProperties(family=available_font, size=15)
    title_font = fm.FontProperties(family=available_font, size=17, weight='bold')
    label_font = fm.FontProperties(family=available_font, size=19)
    tick_font = fm.FontProperties(family=available_font, size=14)
else:
    text_font = fm.FontProperties(family='sans-serif', size=12)
    title_font = fm.FontProperties(family='sans-serif', size=14, weight='bold')
    label_font = fm.FontProperties(family='sans-serif', size=12)
    tick_font = fm.FontProperties(family='sans-serif', size=11)

# 设置样式（避免seaborn样式错误）
try:
    plt.style.use('default')
    # 手动设置白色背景，不使用seaborn的set_style
    rcParams['axes.facecolor'] = 'white'
    rcParams['figure.facecolor'] = 'white'
    rcParams['axes.grid'] = False
except:
    pass

# ===========================
# 3. 创建图形
# ===========================
plt.figure(figsize=(14, 7))

x_labels = df['生测编号']
x = range(len(x_labels))
bar_width = 0.35

# ===========================
# 4. 学术配色柱状图（使用指定的蓝色和红色）
# ===========================
colors = ['#4a90c0', '#d9534f']  # 蓝色对灰霉，红色对赤霉

plt.bar([i - bar_width/2 for i in x], df['灰霉'], width=bar_width, label='灰霉', color=colors[0])
plt.bar([i + bar_width/2 for i in x], df['赤霉'], width=bar_width, label='赤霉', color=colors[1])

# 在y=0处画一条水平线
plt.axhline(y=0, color='black', linewidth=1.5, linestyle='-', zorder=1)

# ===========================
# 5. 美化图形
# ===========================
ax = plt.gca()

# 设置X轴标签（水平显示，无旋转）
ax.set_xticks(x)
ax.set_xticklabels(x_labels, rotation=0, ha='center', fontproperties=tick_font)

# 设置Y轴刻度
plt.yticks(fontproperties=tick_font)

# 设置Y轴标签
ax.set_ylabel('抑制率 / 相对值', fontproperties=label_font)

# 设置X轴标签（添加X轴标题）
ax.set_xlabel('生测编号', fontproperties=label_font)

# 设置标题
ax.set_title('', fontproperties=title_font)

# 设置图例（放在Y轴上部右侧，与原图保持一致）
plt.legend(fontsize=14, frameon=False, prop=text_font, loc='upper left', bbox_to_anchor=(0.02, 0.98))  # Y轴上部右侧

# 去掉顶部和右边框，更学术
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

# 确保X轴和底部框线可见
ax.spines['bottom'].set_visible(True)

# 调整布局
plt.tight_layout()

# 强制所有文本使用正确字体
for label in ax.get_xticklabels():
    if available_font:
        label.set_fontproperties(tick_font)
    else:
        label.set_fontfamily('sans-serif')
for label in ax.get_yticklabels():
    if available_font:
        label.set_fontproperties(tick_font)
    else:
        label.set_fontfamily('sans-serif')
if available_font:
    ax.xaxis.label.set_fontproperties(label_font)
    ax.yaxis.label.set_fontproperties(label_font)
    ax.title.set_fontproperties(title_font)
else:
    ax.xaxis.label.set_fontfamily('sans-serif')
    ax.yaxis.label.set_fontfamily('sans-serif')
    ax.title.set_fontfamily('sans-serif')

print("\n✓ 图表生成完成")
plt.show()
