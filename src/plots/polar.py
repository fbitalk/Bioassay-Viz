import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .utils import configure_mpl_fonts

def draw_polar_bar(df, font_size=12):
    """
    绘制极坐标除草柱图
    """
    global_font = configure_mpl_fonts()
    
    labels = df.iloc[:, 0].astype(str).values
    data_df = df.iloc[:, 1:]
    crops = data_df.columns.tolist()
    n_sample = len(df)
    n_crop = len(crops)
    
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
            try:
                value = float(value)
            except:
                value = 0
                
            angle = base_angle + (j + 0.5) * bar_width
            scaled_value = inner_radius + (value / 100) * (max_radius - inner_radius)
            
            ax.bar(angle, scaled_value - inner_radius, width=bar_width * 0.9, bottom=inner_radius,
                   color=bar_colors[j % len(bar_colors)], edgecolor="black", linewidth=0.2, alpha=0.85,
                   label=crop if i == 0 else "")

    for i in range(n_sample):
        base_angle = i * (sector_angle + gap_angle)
        theta_sector = np.linspace(base_angle, base_angle + sector_angle, 100)
        ax.plot(theta_sector, [max_radius] * len(theta_sector), color='#CCCCCC', linewidth=2, zorder=10)
        
    axis_angle = -gap_angle * 3.7
    yticks = [0, 20, 40, 60, 80, 100]
    for y in yticks:
        r = inner_radius + (y / 100) * (max_radius - inner_radius)
        theta_grid = np.linspace(0, 2*np.pi, 200)
        ax.plot(theta_grid, [r]*len(theta_grid), color="gray", linestyle="--", linewidth=0.5, alpha=0.3, zorder=0)
        ax.text(axis_angle, r, str(y), ha='left', va='center', fontsize=int(font_size*0.7), color='gray')

    sample_angles_rad = [i * (sector_angle + gap_angle) + sector_angle / 2 for i in range(n_sample)]
    ax.set_thetagrids([], labels=[])
    label_radius = inner_radius - 8
    
    for i, label in enumerate(labels):
        angle_rad = sample_angles_rad[i]
        angle_deg = np.degrees(angle_rad) % 360
        rotation = 90 - angle_deg
        if 180 < angle_deg < 360: rotation += 180
        ax.text(angle_rad, label_radius, label, ha='center', va='center', fontsize=font_size, rotation=rotation, fontproperties=global_font)
        
    ax.set_ylim(0, max_radius + 5)
    
    handles, labels_legend = ax.get_legend_handles_labels()
    ax.legend(handles, labels_legend, loc='center', fontsize=int(font_size*1.1), frameon=False,
              bbox_to_anchor=(0.5, 0.5), prop=global_font)
              
    plt.tight_layout()
    return fig

def draw_radar_chart(df, font_size=14):
    """
    绘制雷达图
    """
    global_font = configure_mpl_fonts()
    
    names = df.iloc[:, 0].astype(str).values
    data_df = df.iloc[:, 1:].select_dtypes(include=[np.number])
    
    if data_df.empty:
        raise ValueError("未找到数值数据列")
        
    categories = list(data_df.columns)
    N = len(categories)
    
    max_show = 6
    if len(df) > max_show:
        names = names[:max_show]
        data_df = data_df.iloc[:max_show]

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, (name, row) in enumerate(zip(names, data_df.values)):
        values = row.flatten().tolist()
        values += values[:1]
        
        color = colors[i % len(colors)]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=name, color=color)
        ax.fill(angles, values, color=color, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontproperties=global_font, fontsize=font_size)
    
    ax.yaxis.set_tick_params(labelsize=int(font_size*0.7))
    plt.yticks(fontproperties=global_font)
    
    ax.set_title("多靶标广谱活性评价", fontproperties=global_font, fontsize=int(font_size*1.4), pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 1.1), prop=global_font, frameon=False)
    
    plt.tight_layout()
    return fig