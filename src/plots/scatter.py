import pandas as pd
import matplotlib.pyplot as plt
from .utils import configure_mpl_fonts

def draw_optimization_bubble(df, font_size=12):
    """
    绘制反应条件筛选气泡图
    """
    global_font = configure_mpl_fonts()
    
    if df.shape[1] < 4:
        raise ValueError("数据列数不足，至少需要 4 列 (Catalyst, Solvent, Yield, ee)")

    col_names = df.columns
    x_col = col_names[0]
    y_col = col_names[1]
    size_col = col_names[2]
    color_col = col_names[3]
    
    x_cat = df[x_col].astype(str)
    y_solv = df[y_col].astype(str)
    sizes = pd.to_numeric(df[size_col], errors='coerce').fillna(0)
    colors = pd.to_numeric(df[color_col], errors='coerce').fillna(0)
    
    unique_x = sorted(list(set(x_cat)))
    unique_y = sorted(list(set(y_solv)))
    
    x_map = {val: i for i, val in enumerate(unique_x)}
    y_map = {val: i for i, val in enumerate(unique_y)}
    
    x_vals = x_cat.map(x_map)
    y_vals = y_solv.map(y_map)

    fig, ax = plt.subplots(figsize=(11, 9))
    
    sc = ax.scatter(x_vals, y_vals, s=sizes*12, c=colors, 
                    cmap='viridis', alpha=0.8, edgecolors='black', linewidth=1)
    
    ax.set_xticks(range(len(unique_x)))
    ax.set_xticklabels(unique_x, fontsize=font_size, rotation=0, fontproperties=global_font)
    
    ax.set_yticks(range(len(unique_y)))
    ax.set_yticklabels(unique_y, fontsize=font_size, fontproperties=global_font)
    
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    ax.set_xlabel(x_col, fontsize=int(font_size*1.2), fontweight='bold', labelpad=10, fontproperties=global_font)
    ax.set_ylabel(y_col, fontsize=int(font_size*1.2), fontweight='bold', labelpad=10, fontproperties=global_font)
    ax.set_title('反应条件筛选结果 (Reaction Optimization)', fontsize=int(font_size*1.5), pad=20, fontproperties=global_font)
    
    cbar = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(f'{color_col} (Color)', rotation=270, labelpad=20, fontsize=font_size, fontproperties=global_font)
    
    legend_sizes = [20, 50, 80]
    legend_labels = ['20%', '50%', '80%']
    legend_handles = [plt.scatter([], [], s=s*12, c='gray', alpha=0.6, edgecolors='black') for s in legend_sizes]
    
    ax.legend(legend_handles, legend_labels, title=f"{size_col} (Size)", 
              loc='upper left', bbox_to_anchor=(1.15, 1), frameon=False, labelspacing=1.5, prop=global_font)
    
    plt.tight_layout()
    plt.subplots_adjust(right=0.85)
    
    return fig