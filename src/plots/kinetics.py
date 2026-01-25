import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from .utils import configure_mpl_fonts

def draw_kinetics(df, font_size=14):
    """
    绘制反应动力学曲线
    :param df: 第一列必须是时间（数值），后续列为各组实验的产率/转化率
    """
    global_font = configure_mpl_fonts()
    
    # 确保第一列作为时间轴
    time_col = df.columns[0]
    df = df.set_index(time_col)
    
    # 简单清洗：确保索引是数值型
    try:
        df.index = df.index.astype(float)
    except:
        raise ValueError("第一列必须是代表时间的数值")
        
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 定义一组清晰的标记形状和颜色
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, col in enumerate(df.columns):
        # 提取数据并去除空值
        series = df[col].dropna()
        
        ax.plot(series.index, series.values, 
                marker=markers[i % len(markers)], 
                color=colors[i % len(colors)],
                linewidth=2.5, 
                markersize=8, 
                alpha=0.85,
                label=str(col))
    
    # 设置轴标签和标题
    ax.set_xlabel(f"{time_col}", fontsize=int(font_size*1.2), fontweight='bold', labelpad=10, fontproperties=global_font)
    ax.set_ylabel("Yield / Conversion (%)", fontsize=int(font_size*1.2), fontweight='bold', labelpad=10, fontproperties=global_font)
    ax.set_title("Reaction Kinetics Monitoring", fontsize=int(font_size*1.5), pad=20, fontproperties=global_font)
    
    # 设置刻度字体
    ax.tick_params(axis='both', which='major', labelsize=font_size)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(global_font)
    
    # 图例设置
    ax.legend(frameon=False, fontsize=font_size, prop=global_font, loc='best')
    
    # 网格和边框
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 尝试设置Y轴范围（如果是产率通常在0-100）
    if df.max().max() <= 105 and df.min().min() >= -5:
        ax.set_ylim(-2, 105)
    
    plt.tight_layout()
    return fig