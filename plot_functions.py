import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties
import numpy as np
import re
import os
import platform

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
# 1. 热图功能
# ==============================
def sort_key(name):
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

def draw_heatmap(df, split_index=None):
    """
    绘制热图。如果不提供 split_index，则绘制一张图。
    如果提供 split_index 且存在，则返回两张图的列表。
    """
    # 初始化字体
    global_font = configure_mpl_fonts()
    
    # 数据清洗
    if '生测编号' in df.columns:
        df.set_index('生测编号', inplace=True)
    else:
        df.set_index(df.columns[0], inplace=True)
    
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # 假设数据是 0-1 小数，转为百分数
    if df.max().max() <= 1.0:
         df = df * 100
            
    # 排序
    try:
        sorted_index = sorted(df.index, key=sort_key)
        df = df.reindex(sorted_index)
    except Exception:
        pass

    # 分割逻辑
    dfs_to_plot = []
    if split_index and split_index in df.index:
        split_pos = df.index.get_loc(split_index)
        dfs_to_plot.append(df.iloc[:split_pos+1])
        if split_pos + 1 < len(df):
            dfs_to_plot.append(df.iloc[split_pos+1:])
    else:
        dfs_to_plot.append(df)
        
    figures = []
    
    # 绘图配置
    cell_width = 1.15
    cell_height = 0.65
    colors = ["#ffe5e5", "#ffcccc", "#fcbba1", "#fb6a4a", "#de2d26", "#a50f15"]
    cmap = mcolors.LinearSegmentedColormap.from_list("academic_red", colors, N=256)
    
    for df_sub in dfs_to_plot:
        if df_sub.empty: continue
        
        n_rows, n_cols = df_sub.shape
        fig_w = n_cols * cell_width + 3
        fig_h = n_rows * cell_height + 2
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        sns.heatmap(df_sub, ax=ax, cmap=cmap, vmin=0, vmax=100, annot=False,
                    linewidths=0.4, linecolor="white", cbar_kws={'fraction': 0.04, 'pad': 0.04})
        
        # 添加数值
        for i in range(n_rows):
            for j in range(n_cols):
                v = df_sub.iloc[i, j]
                ax.text(j + 0.5, i + 0.5, str(int(round(v))),
                        ha='center', va='center', fontsize=18, weight='bold', color='black',
                        fontproperties=global_font)
        
        ax.xaxis.tick_top()
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=16, fontproperties=global_font)
        
        # Y轴
        ax.yaxis.set_tick_params(length=0)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right', fontproperties=global_font, fontsize=16)
        ax.set_ylabel('生测编号', fontproperties=global_font, fontsize=24)
        
        # 标题
        ax.text(0.5, 1.04, '处理浓度 (ppm)', transform=ax.transAxes, ha='center', va='bottom',
                fontsize=16, fontweight='semibold', fontproperties=global_font)
        
        # Colorbar
        cbar = ax.collections[0].colorbar
        cbar.set_label('死亡率 (%)', fontproperties=global_font, fontsize=14)
        
        ax.spines['bottom'].set_visible(False)
        plt.tight_layout()
        figures.append(fig)
        
    return figures

# ==============================
# 2. 除草柱图功能 (极坐标)
# ==============================
def draw_polar_bar(df):
    """
    绘制极坐标除草柱图
    """
    global_font = configure_mpl_fonts()
    
    # 数据预处理
    # 假设第一列是 Label，后面是数据
    labels = df.iloc[:, 0].astype(str).values
    data_df = df.iloc[:, 1:]
    crops = data_df.columns.tolist()
    n_sample = len(df)
    n_crop = len(crops)
    
    # 极坐标参数
    gap_ratio = 0.05
    sector_angle = (2 * np.pi / n_sample) * (1 - gap_ratio)
    gap_angle = (2 * np.pi / n_sample) * gap_ratio
    bar_width = sector_angle / (n_crop + 1)
    
    inner_radius = 50
    max_radius = 100
    bar_colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B3", "#CCB974", "#64B5CD"]
    
    fig = plt.figure(figsize=(12, 11))
    ax = plt.subplot(111, polar=True)
    ax.grid(False)
    ax.set_facecolor('white')
    ax.spines['polar'].set_visible(False)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    for i, label in enumerate(labels):
        base_angle = i * (sector_angle + gap_angle)
        for j, crop in enumerate(crops):
            value = data_df[crop].iloc[i]
            # 确保 value 是数值
            try:
                value = float(value)
            except:
                value = 0
                
            angle = base_angle + (j + 0.5) * bar_width
            scaled_value = inner_radius + (value / 100) * (max_radius - inner_radius)
            
            ax.bar(angle, scaled_value - inner_radius, width=bar_width * 0.9, bottom=inner_radius,
                   color=bar_colors[j % len(bar_colors)], edgecolor="black", linewidth=0.2, alpha=0.85,
                   label=crop if i == 0 else "")

    # 分隔线
    for i in range(n_sample):
        base_angle = i * (sector_angle + gap_angle)
        theta_sector = np.linspace(base_angle, base_angle + sector_angle, 100)
        ax.plot(theta_sector, [max_radius] * len(theta_sector), color='#CCCCCC', linewidth=2, zorder=10)
        
    # Y轴刻度
    axis_angle = -gap_angle * 3.7
    yticks = [0, 20, 40, 60, 80, 100]
    for y in yticks:
        r = inner_radius + (y / 100) * (max_radius - inner_radius)
        theta_grid = np.linspace(0, 2*np.pi, 200)
        ax.plot(theta_grid, [r]*len(theta_grid), color="gray", linestyle="--", linewidth=0.5, alpha=0.3, zorder=0)
        ax.text(axis_angle, r, str(y), ha='left', va='center', fontsize=8, color='gray')

    # 标签
    sample_angles_rad = [i * (sector_angle + gap_angle) + sector_angle / 2 for i in range(n_sample)]
    ax.set_thetagrids([], labels=[])
    label_radius = inner_radius - 8
    
    for i, label in enumerate(labels):
        angle_rad = sample_angles_rad[i]
        angle_deg = np.degrees(angle_rad) % 360
        rotation = 90 - angle_deg
        if 180 < angle_deg < 360: rotation += 180
        ax.text(angle_rad, label_radius, label, ha='center', va='center', fontsize=12, rotation=rotation, fontproperties=global_font)
        
    ax.set_ylim(0, max_radius + 5)
    
    # 图例
    handles, labels_legend = ax.get_legend_handles_labels()
    ax.legend(handles, labels_legend, loc='center', fontsize=13, frameon=False,
              bbox_to_anchor=(0.5, 0.5), prop=global_font)
              
    plt.tight_layout()
    return fig

# ==============================
# 3. 除菌柱图功能
# ==============================
def draw_fungicide_bar(df):
    """
    绘制除菌柱状图（灰霉 vs 赤霉）
    """
    global_font = configure_mpl_fonts()
    
    # 确保有需要的列
    required_cols = ['生测编号', '灰霉', '赤霉']
    # 简单的列名映射尝试
    if '生测编号' not in df.columns:
        df.rename(columns={df.columns[0]: '生测编号'}, inplace=True)
    
    # 检查灰霉和赤霉列是否存在，如果不存在则尝试模糊匹配或报错
    # 这里简单处理，如果没找到，就取第2和第3列
    if '灰霉' not in df.columns and len(df.columns) > 1:
        df.rename(columns={df.columns[1]: '灰霉'}, inplace=True)
    if '赤霉' not in df.columns and len(df.columns) > 2:
        df.rename(columns={df.columns[2]: '赤霉'}, inplace=True)
        
    if '灰霉' not in df.columns or '赤霉' not in df.columns:
        raise ValueError("数据缺少 '灰霉' 或 '赤霉' 列，且无法自动推断。")

    fig, ax = plt.subplots(figsize=(14, 7))
    
    x_labels = df['生测编号']
    x = range(len(x_labels))
    bar_width = 0.35
    colors = ['#4a90c0', '#d9534f']
    
    ax.bar([i - bar_width/2 for i in x], df['灰霉'], width=bar_width, label='灰霉', color=colors[0])
    ax.bar([i + bar_width/2 for i in x], df['赤霉'], width=bar_width, label='赤霉', color=colors[1])
    
    ax.axhline(y=0, color='black', linewidth=1.5, linestyle='-', zorder=1)
    
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=0, ha='center', fontproperties=global_font)
    
    for label in ax.get_yticklabels():
        label.set_fontproperties(global_font)
        
    ax.set_ylabel('抑制率 / 相对值', fontproperties=global_font, fontsize=14)
    ax.set_xlabel('生测编号', fontproperties=global_font, fontsize=14)
    
    ax.legend(fontsize=14, frameon=False, prop=global_font, loc='upper left', bbox_to_anchor=(0.02, 0.98))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig

# ==============================
# 4. 统计箱线图功能
# ==============================
def draw_boxplot(df):
    """
    绘制数据分布箱线图
    """
    global_font = configure_mpl_fonts()
    
    # 尝试将第一列设为索引（通常是编号），剩下的作为数值列
    if df.columns[0] not in df.select_dtypes(include=[np.number]).columns:
        df = df.set_index(df.columns[0])
    
    # 只保留数值列
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        raise ValueError("未找到有效的数值列用于绘制箱线图")

    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 绘图
    sns.boxplot(data=numeric_df, ax=ax, palette="Set3", width=0.5)
    sns.stripplot(data=numeric_df, ax=ax, color=".25", size=4, alpha=0.6, jitter=True)
    
    # 设置字体
    ax.set_title('各指标活性数据分布', fontproperties=global_font, fontsize=18, pad=20)
    ax.set_ylabel('活性数值', fontproperties=global_font, fontsize=14)
    ax.set_xlabel('测试指标', fontproperties=global_font, fontsize=14)
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontproperties=global_font, fontsize=12)
    
    # 移除上右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    return fig

# ==============================
# 5. 广谱雷达图功能
# ==============================
def draw_radar_chart(df):
    """
    绘制多维雷达图（适合展示广谱性）
    默认只取前5行数据进行展示，避免过于混乱
    """
    global_font = configure_mpl_fonts()
    
    # 数据预处理：第一列为名称
    names = df.iloc[:, 0].astype(str).values
    data_df = df.iloc[:, 1:].select_dtypes(include=[np.number])
    
    if data_df.empty:
        raise ValueError("未找到数值数据列")
        
    categories = list(data_df.columns)
    N = len(categories)
    
    # 限制展示数量，防止图表混乱
    max_show = 6
    if len(df) > max_show:
        names = names[:max_show]
        data_df = data_df.iloc[:max_show]
        print(f"Warning: 只展示前 {max_show} 条数据的雷达图")

    # 角度设置
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # 闭合
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # 颜色库
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, (name, row) in enumerate(zip(names, data_df.values)):
        values = row.flatten().tolist()
        values += values[:1]  # 闭合
        
        color = colors[i % len(colors)]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=name, color=color)
        ax.fill(angles, values, color=color, alpha=0.1)

    # 设置各种标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontproperties=global_font, fontsize=14)
    
    # 设置Y轴标签（不显示具体刻度值，避免重叠，或者只显示几个）
    ax.yaxis.set_tick_params(labelsize=10)
    plt.yticks(fontproperties=global_font)
    
    # 标题和图例
    ax.set_title("多靶标广谱活性评价", fontproperties=global_font, fontsize=20, pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 1.1), prop=global_font, frameon=False)
    
    plt.tight_layout()
    return fig