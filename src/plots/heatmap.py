import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
from .utils import configure_mpl_fonts, sort_key

def draw_heatmap(df, split_index=None, cmap_name="academic_red", font_size=16):
    """
    绘制热图
    :param df: 数据 DataFrame
    :param split_index: 分割点索引
    :param cmap_name: 颜色主题名
    :param font_size: 基础字体大小
    """
    global_font = configure_mpl_fonts()
    
    # 数据清洗
    if '生测编号' in df.columns:
        df.set_index('生测编号', inplace=True)
    else:
        df.set_index(df.columns[0], inplace=True)
    
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    if df.max().max() <= 1.0:
         df = df * 100
            
    try:
        sorted_index = sorted(df.index, key=sort_key)
        df = df.reindex(sorted_index)
    except Exception:
        pass

    dfs_to_plot = []
    if split_index and split_index in df.index:
        split_pos = df.index.get_loc(split_index)
        dfs_to_plot.append(df.iloc[:split_pos+1])
        if split_pos + 1 < len(df):
            dfs_to_plot.append(df.iloc[split_pos+1:])
    else:
        dfs_to_plot.append(df)
        
    figures = []
    
    # 颜色映射处理
    if cmap_name == "academic_red":
        colors = ["#ffe5e5", "#ffcccc", "#fcbba1", "#fb6a4a", "#de2d26", "#a50f15"]
        cmap = mcolors.LinearSegmentedColormap.from_list("academic_red", colors, N=256)
    elif cmap_name == "coolwarm":
        cmap = "coolwarm"
    elif cmap_name == "viridis":
        cmap = "viridis"
    else:
        cmap = "YlOrRd"

    cell_width = 1.15
    cell_height = 0.65
    
    for df_sub in dfs_to_plot:
        if df_sub.empty: continue
        
        n_rows, n_cols = df_sub.shape
        fig_w = n_cols * cell_width + 3
        fig_h = n_rows * cell_height + 2
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        sns.heatmap(df_sub, ax=ax, cmap=cmap, vmin=0, vmax=100, annot=False,
                    linewidths=0.4, linecolor="white", cbar_kws={'fraction': 0.04, 'pad': 0.04})
        
        for i in range(n_rows):
            for j in range(n_cols):
                v = df_sub.iloc[i, j]
                ax.text(j + 0.5, i + 0.5, str(int(round(v))),
                        ha='center', va='center', fontsize=int(font_size*1.125), weight='bold', color='black',
                        fontproperties=global_font)
        
        ax.xaxis.tick_top()
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=font_size, fontproperties=global_font)
        
        ax.yaxis.set_tick_params(length=0)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right', fontproperties=global_font, fontsize=font_size)
        ax.set_ylabel('生测编号', fontproperties=global_font, fontsize=int(font_size*1.5))
        
        ax.text(0.5, 1.04, '处理浓度 (ppm)', transform=ax.transAxes, ha='center', va='bottom',
                fontsize=font_size, fontweight='semibold', fontproperties=global_font)
        
        cbar = ax.collections[0].colorbar
        cbar.set_label('死亡率 (%)', fontproperties=global_font, fontsize=int(font_size*0.875))
        
        ax.spines['bottom'].set_visible(False)
        plt.tight_layout()
        figures.append(fig)
        
    return figures