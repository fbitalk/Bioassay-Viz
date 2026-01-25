import numpy as np
import matplotlib.pyplot as plt
from .utils import configure_mpl_fonts

def draw_energy_profile(df, font_size=12):
    """
    绘制反应能级图 (Reaction Energy Profile)
    """
    global_font = configure_mpl_fonts()
    
    if df.shape[1] < 2:
        raise ValueError("数据列数不足，至少需要 2 列 (Step, Energy...)")
    
    steps = df.iloc[:, 0].astype(str).values
    n_steps = len(steps)
    
    path_cols = df.iloc[:, 1:].select_dtypes(include=[np.number]).columns
    
    if len(path_cols) == 0:
        raise ValueError("未找到数值列作为能量数据")
        
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = ['#d62728', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', '#8c564b']
    
    level_width = 0.6
    gap = 0.4
    
    for idx, col in enumerate(path_cols):
        energies = df[col].values
        color = colors[idx % len(colors)]
        label = str(col).replace('_Energy', '').replace('_', ' ')
        
        connector_x = []
        connector_y = []
        
        for i, E in enumerate(energies):
            if np.isnan(E): 
                connector_x.append(None)
                connector_y.append(None)
                continue
                
            center_x = i * (level_width + gap)
            
            x_start = center_x - level_width / 2
            x_end = center_x + level_width / 2
            ax.plot([x_start, x_end], [E, E], color=color, linewidth=2.5, label=label if i == 0 else "")
            
            connector_x.append(center_x)
            connector_y.append(E)
            
            ax.text(center_x, E + (1.0 if E >= 0 else -1.5), f"{E:.1f}", ha='center', va='bottom', 
                    fontsize=int(font_size*0.8), color=color, fontweight='bold', fontproperties=global_font)

        for i in range(len(connector_x) - 1):
            if connector_x[i] is None or connector_x[i+1] is None:
                continue
                
            x1 = connector_x[i] + level_width / 2
            y1 = connector_y[i]
            x2 = connector_x[i+1] - level_width / 2
            y2 = connector_y[i+1]
            
            t = np.linspace(0, 1, 50)
            x_smooth = x1 + (x2 - x1) * t
            y_smooth = y1 + (y2 - y1) * (1 - np.cos(t * np.pi)) / 2
            
            ax.plot(x_smooth, y_smooth, color=color, linestyle='--', linewidth=1.2, alpha=0.6)
            
    ax.set_xticks([i * (level_width + gap) for i in range(n_steps)])
    ax.set_xticklabels(steps, fontsize=font_size, fontweight='semibold', fontproperties=global_font)
    
    ax.set_ylabel('相对吉布斯自由能 (kcal/mol)', fontsize=font_size, fontproperties=global_font)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.legend(frameon=False, loc='best', prop=global_font)
    ax.set_title('反应能级图 (Reaction Energy Profile)', fontsize=int(font_size*1.3), pad=15, fontproperties=global_font)
    
    plt.tight_layout()
    return fig