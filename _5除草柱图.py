import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ===========================
# 1. 基础设置
# ===========================
rcParams["font.sans-serif"] = ["Microsoft YaHei"]
rcParams["axes.unicode_minus"] = False

# ===========================
# 2. 读取数据
# ===========================
file_path = r"C:\Users\11142\Downloads\无CX.xlsx"

try:
    # 尝试读取
    df = pd.read_excel(file_path, sheet_name="Sheet4")
except Exception as e:
    # 这里改成英文提示，防止编码报错
    print(f"Error reading file: {e}")
    print("Generating simulation data...")
    
    np.random.seed(42)
    df = pd.DataFrame(np.random.randint(10, 95, size=(24, 6)), 
                      columns=[f'作物{x}' for x in 'ABCDEF'])
    df.insert(0, 'Label', [f"I2-{i+1}" for i in range(24)])

labels = df.iloc[:, 0].astype(str).values
data = df.iloc[:, 1:]
crops = data.columns.tolist()
n_sample = len(df)
n_crop = len(crops)

# ===========================
# 3. 极坐标参数
# ===========================
gap_ratio = 0.05 
sector_angle = (2 * np.pi / n_sample) * (1 - gap_ratio)
gap_angle = (2 * np.pi / n_sample) * gap_ratio
bar_width = sector_angle / (n_crop + 1)

inner_radius = 50
max_radius = 100
colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B3", "#CCB974", "#64B5CD"]

# ===========================
# 4. 绘图主体
# ===========================
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
        value = data[crop].iloc[i]
        angle = base_angle + (j + 0.5) * bar_width
        scaled_value = inner_radius + (value / 100) * (max_radius - inner_radius)
        
        ax.bar(
            angle,
            scaled_value - inner_radius,
            width=bar_width * 0.9,
            bottom=inner_radius,
            color=colors[j],
            edgecolor="black",
            linewidth=0.2,
            alpha=0.85,
            label=crop if i == 0 else ""
        )

for i in range(n_sample):
    base_angle = i * (sector_angle + gap_angle)
    theta_sector = np.linspace(base_angle, base_angle + sector_angle, 100)
    ax.plot(theta_sector, [max_radius] * len(theta_sector),
            color='#CCCCCC', linewidth=2, zorder=10)

# ===========================
# 5. 自定义Y轴 (镜像翻转 + 灰色)
# ===========================
axis_angle = -gap_angle * 3.7
yticks = [0, 20, 40, 60, 80, 100]
tick_length_angle = 0.01 

for y in yticks:
    r = inner_radius + (y / 100) * (max_radius - inner_radius)
    theta_grid = np.linspace(0, 2*np.pi, 200)
    ax.plot(theta_grid, [r]*len(theta_grid), 
            color="gray", linestyle="--", linewidth=0.5, alpha=0.3, zorder=0)
    ax.plot([axis_angle, axis_angle + tick_length_angle], [r, r], 
            color="gray", linewidth=1.2, zorder=10) 
    ax.text(axis_angle + tick_length_angle + 0.005, r, str(y), 
            ha='left', va='center', fontsize=6, 
            fontweight='bold', color='gray') 

ax.plot([axis_angle, axis_angle], [inner_radius, max_radius], 
        color="gray", linewidth=1.5, zorder=10)

# ===========================
# 6. X轴标签
# ===========================
sample_angles_rad = [i * (sector_angle + gap_angle) + sector_angle / 2
                     for i in range(n_sample)]
ax.set_thetagrids([], labels=[])
label_radius = inner_radius - 8

for i, label in enumerate(labels):
    angle_rad = sample_angles_rad[i]
    angle_deg = np.degrees(angle_rad) % 360
    rotation = 90 - angle_deg
    if 180 < angle_deg < 360:
        rotation += 180
    
    ax.text(
        angle_rad, 
        label_radius, 
        label, 
        ha='center', 
        va='center', 
        fontsize=12, 
        rotation=rotation
    )

ax.set_ylim(0, max_radius + 5)
ax.set_yticks([]) 
ax.set_yticklabels([]) 

# ===========================
# 7. 图例
# ===========================
handles, labels_legend = ax.get_legend_handles_labels()
center_legend = ax.legend(
    handles, labels_legend,
    loc='center', fontsize=13, frameon=False,
    title='作物类型\n(抑制率 %)', title_fontsize=15,
    bbox_to_anchor=(0.5, 0.5), handletextpad=0.5, labelspacing=0.8
)

ax.set_title("", fontsize=16, pad=30, fontweight='bold')

plt.tight_layout()
plt.show()