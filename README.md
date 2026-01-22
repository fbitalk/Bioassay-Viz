"# 📊 Bioassay Visualization Tool (生测数据可视化工具)

这是一个基于 Python Streamlit 的生测数据可视化工具，旨在简化实验室数据的图表生成过程。用户只需上传 Excel 文件，即可自动生成符合学术规范的热图和柱状图。

## ✨ 主要功能

本工具整合了三个核心功能模块：

1.  **🔥 活性热图 (Heatmap)**
    *   将生测数据（0-1 或 0-100）转换为带有颜色梯度的热图。
    *   支持自定义排序（罗马数字、生测编号）。
    *   支持数据分割（Split Point），可将长图表拆分为多张。
    *   自动将小数转换为百分数。
    
    ![Heatmap Demo](assets/demo_heatmap.png)

2.  **🌿 除草活性极坐标图 (Polar Bar)**
    *   生成美观的极坐标柱状图，展示不同作物对样品的敏感度。
    *   自动适配作物数量。
    
    ![Polar Bar Demo](assets/demo_polar.png)

3.  **🍄 除菌活性柱状图 (Bar Chart)**
    *   自动识别“灰霉”和“赤霉”数据。
    *   生成对比分组柱状图，包含学术风格的配色和布局。
    
    ![Bar Chart Demo](assets/demo_bar.png)

4.  **📦 数据分布箱线图 (Boxplot)**
    *   **新功能**：统计各指标（作物/菌种）的活性分布情况。
    *   展示最大值、最小值、中位数及异常值，快速评估数据质量。
    
    ![Boxplot Demo](assets/demo_boxplot.png)

5.  **🕸️ 广谱活性雷达图 (Radar Chart)**
    *   **新功能**：多维度展示化合物的广谱活性。
    *   直观对比单一化合物对多个靶标的综合效果。
    
    ![Radar Chart Demo](assets/demo_radar.png)

## 🚀 快速开始

### 方式一：直接运行 (Windows)
双击项目根目录下的 **`run_app.bat`** 脚本。它会自动检查依赖并在浏览器中启动应用。

### 方式二：手动安装运行

1.  **克隆仓库**
    ```bash
    git clone https://github.com/fbitalk/Bioassay-Viz.git
    cd Bioassay-Viz
    ```

2.  **安装依赖**
    确保已安装 Python (3.8+)，然后运行：
    ```bash
    pip install -r requirements.txt
    ```

3.  **启动应用**
    ```bash
    streamlit run app.py
    ```

### 🧪 生成测试数据
如果你想快速体验所有功能，可以运行以下命令生成一份包含所有场景的测试数据：
```bash
python generate_test_data.py
```
运行后会在目录下生成 `test_data.xlsx`，直接上传即可使用。

## 📂 数据格式说明

为了确保图表正确生成，请参考以下 Excel 数据格式：

*   **热图**: 第一列为样本编号（如 `Ⅰ2-1`），后续列为不同浓度的数值。
*   **除草图**: 第一列为样本编号，后续列名为作物名称（如 `小麦`, `玉米`），值为抑制率。
*   **除菌图**: 必需包含列名 `生测编号`, `灰霉`, `赤霉`。
*   **箱线图**: 第一列为编号，后续均为数值列。
*   **雷达图**: 第一列为编号，后续为各维度指标（建议数据不超过6行以保证可读性）。

## 🛠️ 技术栈
*   [Streamlit](https://streamlit.io/) - Web 应用框架
*   [Pandas](https://pandas.pydata.org/) - 数据处理
*   [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) - 数据可视化

## 📄 License
MIT License"