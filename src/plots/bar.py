import matplotlib.pyplot as plt
from .utils import configure_mpl_fonts

def draw_fungicide_bar(df, font_size=14):
    """
    绘制除菌柱状图（灰霉 vs 赤霉）
    """
    global_font = configure_mpl_fonts()
    
    # 确保有需要的列
    if '生测编号' not in df.columns:
        df.rename(columns={df.columns[0]: '生测编号'}, inplace=True)
    
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
    ax.set_xticklabels(x_labels, rotation=0, ha='center', fontproperties=global_font, fontsize=font_size)
    
    for label in ax.get_yticklabels():
        label.set_fontproperties(global_font)
        
    ax.set_ylabel('抑制率 / 相对值', fontproperties=global_font, fontsize=font_size)
    ax.set_xlabel('生测编号', fontproperties=global_font, fontsize=font_size)
    
    ax.legend(fontsize=font_size, frameon=False, prop=global_font, loc='upper left', bbox_to_anchor=(0.02, 0.98))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig