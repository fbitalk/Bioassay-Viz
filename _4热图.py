# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties
import os
import sys
import re
import math

# ==============================
# 防止窗口一闪而过
# ==============================
def exit_program():
    input("\n程序运行结束，请按回车键退出...")
    sys.exit()

print("Step 1: 初始化环境...")

# ==============================
# 1. 全局绘图风格（论文级） + 中文字体
# ==============================
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties

font_path = r'C:\Windows\Fonts\msyh.ttc'  # ✅ 不要用 simhei
try:
    fm.fontManager.addfont(font_path)
    prop = FontProperties(fname=font_path)
    font_name = prop.get_name()

    plt.rcParams['font.sans-serif'] = [font_name]
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['pdf.fonttype'] = 42

    global_font = prop
    print(f"✓ 成功加载字体: {font_name}")
except Exception as e:
    print("⚠ 字体加载失败，使用默认字体")
    global_font = None

# ==============================
# 2. 文件路径
# ==============================
file_path = r'C:\Users\11142\Downloads\4CX.xlsx'
save_dir = r'C:\Users\11142\Downloads'

if not os.path.exists(file_path):
    print("【严重错误】未找到 Excel 文件")
    exit_program()

# ==============================
# 3. 颜色映射
# ==============================
colors = ["#ffe5e5", "#ffcccc", "#fcbba1", "#fb6a4a", "#de2d26", "#a50f15"]
cmap = mcolors.LinearSegmentedColormap.from_list("academic_red", colors, N=256)

# ==============================
# 4. 安全的编号排序函数
# ==============================
def sort_key(name):
    name_str = str(name).strip()

    if '阿维菌素' in name_str:
        return (998, 0, 0)
    if 'CK' in name_str or 'ck' in name_str or '对照' in name_str:
        return (999, 0, 0)

    roman_map = {
        'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅳ': 4, 'Ⅴ': 5,
        'Ⅵ': 6, 'Ⅶ': 7, 'Ⅷ': 8, 'Ⅸ': 9, 'Ⅹ': 10,
        'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
        'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10
    }

    m = re.match(r'^([ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩIVX]+)\s*(\d+)-(\d+)$', name_str)
    if m:
        roman = m.group(1)
        a = int(m.group(2))
        b = int(m.group(3))
        return (roman_map.get(roman, 0), a, b)

    nums = re.findall(r'\d+', name_str)
    if nums:
        return (997, int(nums[0]), int(nums[1]) if len(nums) > 1 else 0)

    return (996, 0, 0)

# ==============================
# 🔧 全局格子尺寸（可自由调整）
# ==============================
cell_width = 1.15   # 每列宽度（英寸）
cell_height = 0.65 # 每行高度（英寸）

# ==============================
# 4.5 数据读取与预处理 (最终修正版：小数转百分数)
# ==============================
print("Step 2: 读取并处理数据...")

try:
    # 1. 读取 Excel (您的表格第一行即为表头，无需 header=None)
    df_plot = pd.read_excel(file_path)

    # 2. 设置索引
    # 优先寻找 '生测编号'，如果找不到，默认使用第 1 列作为索引
    if '生测编号' in df_plot.columns:
        df_plot.set_index('生测编号', inplace=True)
    else:
        print(f"⚠ 提示：未找到精确的 '生测编号' 列，自动将第一列 '{df_plot.columns[0]}' 设为索引")
        df_plot.set_index(df_plot.columns[0], inplace=True)

    # 3. 数据清洗与类型转换
    # 将所有非数字内容强制转换为 NaN，然后填 0
    df_plot = df_plot.apply(pd.to_numeric, errors='coerce').fillna(0)

    # ============================================================
    # 🚩 核心修正：将小数转换为百分数 (0.1 -> 10, 1 -> 100)
    # ============================================================
    print("ℹ 正在执行量纲转换：将小数 (0-1) 转换为百分数 (0-100)...")
    df_plot = df_plot * 100

    # 4. 应用自定义排序 (I, II... CK, 阿维菌素)
    try:
        sorted_index = sorted(df_plot.index, key=sort_key)
        df_plot = df_plot.reindex(sorted_index)
        print("✓ 已应用自定义排序规则")
    except Exception as e:
        print(f"⚠ 排序规则应用失败，保持原序: {e}")

    # 5. 保留列的原始顺序 (防止 0.8ppm 被排到 250ppm 前面)
    # 不执行 sort_index(axis=1)

    print(f"✓ 数据加载完成。")
    print(f"  - 数据示例：最大值={df_plot.max().max()} (应为100), 最小值={df_plot.min().min()}")
    print("------------------------------------------------------")

except FileNotFoundError:
    print("【严重错误】找不到文件，请检查路径")
    exit_program()
except Exception as e:
    print(f"【读取数据错误】: {e}")
    exit_program()

# ==============================
# 5. 热图绘制函数 (最终修复：强制锁定 Y 轴大字体)
# ==============================
def create_heatmap(df_plot, fig_num, sheet_name):
    print(f"正在绘制图表 {fig_num}...")
    n_rows, n_cols = df_plot.shape

    # 计算图表尺寸
    fig_w = n_cols * cell_width + 3  #稍微加宽一点，给大字体留空间
    fig_h = n_rows * cell_height + 2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # 绘制热图
    sns.heatmap(
        df_plot, ax=ax, cmap=cmap, vmin=0, vmax=100,
        annot=False,
        linewidths=0.4, linecolor="white",
        cbar_kws={'fraction': 0.04, 'pad': 0.04}
    )

    # 手动添加数值 (全黑加粗)
    for i in range(n_rows):
        for j in range(n_cols):
            v = df_plot.iloc[i, j]
            v_int = int(round(v))
            ax.text(j + 0.5, i + 0.5, str(v_int),
                    ha='center', va='center',
                    fontsize=18,
                    weight='bold',
                    color='black',
                    fontproperties=global_font if global_font else None)

    # X轴设置
    ax.xaxis.tick_top()
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=0,
        ha='center',
        fontsize=16,
        fontproperties=global_font
    )

    # -------------------------------------------------------
    # 🚩 Y轴设置 (强制大字体修正版)
    # -------------------------------------------------------
    ax.yaxis.set_tick_params(length=0) # 这里不设大小了，没用
    
    # ⬇️ 关键修改：在设置字体的同时，强制 fontsize=24 ⬇️
    ax.set_yticklabels(
        ax.get_yticklabels(), 
        rotation=0, 
        ha='right', 
        fontproperties=global_font, 
        fontsize=16  # ✅ 这里才是真正生效的地方
    )

    # 轴标签
    ax.set_ylabel('生测编号', fontproperties=global_font, fontsize=24)
    # -------------------------------------------------------

    # 顶部标题
    ax.text(0.5, 1.04, '处理浓度 (ppm)',
            transform=ax.transAxes,
            ha='center', va='bottom',
            fontsize=16, fontweight='semibold',
            fontproperties=global_font)

    # 色条设置
    cbar = ax.collections[0].colorbar
    cbar.set_label('死亡率 (%)', fontproperties=global_font, fontsize=14)
    
    # 去掉底部边框
    ax.spines['bottom'].set_visible(False)

    plt.tight_layout()

    # 保存图片
    save_path_png = os.path.join(save_dir, f'生测活性热图_{sheet_name}_图{fig_num}.png')
    plt.savefig(save_path_png, format='png', dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ 已保存PNG: {save_path_png}")

    save_path_svg = os.path.join(save_dir, f'生测活性热图_{sheet_name}_图{fig_num}.svg')
    plt.savefig(save_path_svg, format='svg', dpi=300, bbox_inches='tight')
    print(f"  ✓ 已保存SVG: {save_path_svg}")

    plt.close()
# ==============================
# 🔹 按手动分割点绘制热图
# ==============================
split_index = 'Ⅲ2-16'  # 分割点

# 找到分割行的位置
if split_index in df_plot.index:
    split_pos = df_plot.index.get_loc(split_index)
else:
    print(f"⚠ 警告：分割点 {split_index} 不在 df_plot 中，使用最后一行")
    split_pos = len(df_plot)  # 默认不拆分

# 第一部分
df_part1 = df_plot.iloc[:split_pos+1]
create_heatmap(df_part1, 1, "Sheet1")

# 第二部分
df_part2 = df_plot.iloc[split_pos+1:]
if not df_part2.empty:
    create_heatmap(df_part2, 2, "Sheet1")
