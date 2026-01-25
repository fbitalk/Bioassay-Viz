# 📊 Lab Data Visualization Tool (实验数据可视化工具)

这是一个基于 Python Streamlit 的科研数据可视化工具，专为生物测定（Bioassay）和有机合成（Organic Synthesis）领域的科研人员设计。用户只需上传 Excel 文件，即可一键生成符合学术发表规范（Publication-Ready）的高质量图表。

## ✨ 主要功能 (7大模块)

本工具整合了有机合成领域的常用图表：

### 1. 🔥 活性热图 (Heatmap)
*   **用途**：展示不同浓度下的杀虫/杀菌活性。
*   **特点**：支持罗马数字排序、超长数据自动分割、自动百分比转换。
*   ![Heatmap Demo](assets/demo_heatmap.png)

### 2. 🌿 除草活性极坐标图 (Polar Bar)
*   **用途**：直观展示样品对多种作物（如小麦、玉米等）的抑制活性。
*   **特点**：极坐标布局，信息密度高，美观度优于传统柱状图。
*   ![Polar Bar Demo](assets/demo_polar.png)

### 3. 🍄 除菌活性柱状图 (Bar Chart)
*   **用途**：针对
灰霉、赤霉等菌种的活性对比。
*   **特点**：双柱对比，学术风格配色。
*   ![Bar Chart Demo](assets/demo_bar.png)

### 4. 📦 数据分布箱线图 (Boxplot)
*   **用途**：统计各测试指标（作物/菌种）的活性分布情况。
*   **特点**：快速发现异常值，展示最大/最小值及中位数。
*   ![Boxplot Demo](assets/demo_boxplot.png)

### 5. 🕸️ 广谱活性雷达图 (Radar Chart)
*   **用途**：多维度评价化合物的广谱性（Broad-spectrum activity）。
*   **特点**：直观对比单一化合物在多个靶标上的综合表现。
*   ![Radar Chart Demo](assets/demo_radar.png)

### 6. ⚗️ 反应条件筛选气泡图 (Optimization Bubble Plot)
*   **用途**：有机合成方法学中展示反应条件（溶剂、催化剂等）的筛选结果。
*   **特点**：**四维展示**——X轴(催化剂)、Y轴(溶剂)、气泡大小(产率)、气泡颜色(ee值/立体选择性)。
*   ![Optimization Bubble Demo](assets/bubble_opt_反应条件筛选.png)

### 7. 📈 反应能级图 (Reaction Energy Profile)
*   **用途**：DFT计算或机理研究中展示反应路径的能量变化。
*   **特点**：支持多路径对比（有无催化剂），自动平滑曲线连接，标注相对能量(kcal/mol)。
*   ![Energy Profile Demo](assets/energy_profile_反应能级数据.png)

---

## 🚀 快速开始

### 方式一：直接运行 (Windows)
双击项目根目录下的 **
un_app.bat** 脚本。它会自动检查依赖并在浏览器中启动应用。

### 方式二：手动安装运行

1.  **克隆仓库**
    `
    git clone https://github.com/fbitalk/Bioassay-Viz.git
    cd Bioassay-Viz
    `

2.  **安装依赖**
    确保已安装 Python (3.8+)，然后运行：
    `
    pip install -r requirements.txt
    `

3.  **启动应用**
    `
    streamlit run app.py
    `

### 🧪 生成测试数据
如果你想快速体验所有功能，可以运行以下命令生成一份包含所有场景的测试数据：
`...
python generate_test_data.py
`
运行后会在目录下生成 	est_data.xlsx，直接上传即可使用。包含以下工作表：
*   除草&广谱测试: 用于雷达图、极坐标图、箱线图。
*   除菌测试: 用于除菌柱状图。
*   热图测试: 用于热图。
*   反应条件筛选: 用于气泡图。
*   反应能级数据: 用于能级图。

## 📂 数据格式说明

为了确保图表正确生成，请参考以下 Excel 数据格式：

*   **热图**: 第一列为样本编号，后续列为不同浓度的数值。
*   **除草图**: 第一列为样本编号，后续列名为作物名称，值为抑制率。
*   **除菌图**: 必需包含列名 生测编号, 灰霉, 赤霉。
*   **箱线图**: 第一列为编号，后续均为数值列。
*   **雷达图**: 第一列为编号，后续为各维度指标。
*   **气泡图**: 至少4列，顺序建议为 [催化剂, 溶剂, 产率, ee值]。
*   **能级图**: 第一列为步骤名称(Reactant, TS...)，后续列为各路径能量值。

## 🛠️ 技术栈
*   [Streamlit](https://streamlit.io/) - Web 应用框架
*   [Pandas](https://pandas.pydata.org/) - 数据处理
*   [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) - 数据可视化

## 📄 License
MIT License



