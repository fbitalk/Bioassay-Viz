import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import configure_mpl_fonts

def draw_boxplot(df, font_size=14):
    """
    绘制数据分布箱线图
    """
    global_font = configure_mpl_fonts()
    
    if df.columns[0] not in df.select_dtypes(include=[np.number]).columns:
        df = df.set_index(df.columns[0])
    
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        raise ValueError("未找到有效的数值列用于绘制箱线图")

    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.boxplot(data=numeric_df, ax=ax, palette="Set3", width=0.5)
    sns.stripplot(data=numeric_df, ax=ax, color=".25", size=4, alpha=0.6, jitter=True)
    
    ax.set_title('各指标活性数据分布', fontproperties=global_font, fontsize=int(font_size*1.3), pad=20)
    ax.set_ylabel('活性数值', fontproperties=global_font, fontsize=font_size)
    ax.set_xlabel('测试指标', fontproperties=global_font, fontsize=font_size)
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontproperties=global_font, fontsize=int(font_size*0.85))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    return fig