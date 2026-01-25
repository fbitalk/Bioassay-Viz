import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os
import sys

# 确保可以导入 src 模块
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import plots as pf

# 设置页面配置
st.set_page_config(page_title="数据可视化工具", layout="wide")

# ==========================================
# 辅助函数
# ==========================================
@st.cache_resource
def load_excel(file):
    """缓存加载 Excel 文件"""
    return pd.ExcelFile(file)

def clean_data(df):
    """自动清洗数据"""
    # 1. 删除全空行和全空列
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # 2. 处理表头空白 (Unnamed)
    # 如果第一列是索引但没有名字，通常 pandas 会命名为 Unnamed: 0，这通常没问题
    # 但如果中间有空白列，最好还是删掉
    cols_to_drop = [c for c in df.columns if "Unnamed" in str(c) and df[c].isnull().all()]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        
    return df

def get_download_link_for_template():
    """读取本地生成的模板文件并返回"""
    file_path = "test_data.xlsx"
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return f.read()
    return None

# ==========================================
# 主界面
# ==========================================

# 标题
st.title("📊 生测数据可视化工具")
st.markdown("上传 Excel 文件，自动生成热图、柱状图。")

# 侧边栏：全局设置
with st.sidebar.expander("🎨 全局绘图设置", expanded=False):
    global_font_size = st.slider("基准字体大小", 10, 24, 16)
    heatmap_cmap = st.selectbox("热图配色方案", ["academic_red", "coolwarm", "viridis", "YlOrRd"], index=0)

# 侧边栏：功能选择
mode = st.sidebar.selectbox(
    "选择功能模块",
    ("热图生成 (Heatmap)", "除草活性柱图 (Polar Bar)", "除菌活性柱图 (Bar Chart)", "数据分布箱线图 (Boxplot)", "广谱活性雷达图 (Radar Chart)", "反应条件筛选气泡图 (Optimization Bubble)", "反应能级图 (Energy Profile)", "反应动力学曲线 (Kinetics)")
)

st.sidebar.markdown("---")

# 模板下载区
template_bytes = get_download_link_for_template()
if template_bytes:
    st.sidebar.download_button(
        label="📥 下载 Excel 数据模板",
        data=template_bytes,
        file_name="template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="点击下载示例数据，查看各功能模块所需的数据格式。"
    )
else:
    st.sidebar.warning("⚠️ 未找到模板文件 test_data.xlsx")

# 通用文件上传
uploaded_file = st.sidebar.file_uploader("上传 Excel 文件", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 读取 Excel
        xl = load_excel(uploaded_file)
        sheet_names = xl.sheet_names
        
        st.sidebar.markdown("---")
        selected_sheet = st.sidebar.selectbox("选择工作表 (Sheet)", sheet_names)
        
        # 读取并清洗数据
        raw_df = xl.parse(selected_sheet)
        df = clean_data(raw_df)
        
        st.subheader("数据预览")
        st.dataframe(df.head())
        
        # ==========================================
        # 模式 1: 热图生成
        # ==========================================
        if mode == "热图生成 (Heatmap)":
            st.header("🔥 活性热图")
            
            with st.expander("高级设置", expanded=True):
                split_index = st.text_input("分割点编号 (例如: Ⅲ2-16)", value="Ⅲ2-16")
            
            if st.button("生成热图"):
                with st.spinner("正在绘制热图..."):
                    try:
                        # 传递 UI 参数
                        figures = pf.draw_heatmap(df.copy(), split_index, cmap_name=heatmap_cmap, font_size=global_font_size)
                        
                        for i, fig in enumerate(figures):
                            st.pyplot(fig)
                            
                            # 下载按钮
                            buf = BytesIO()
                            fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                            st.download_button(
                                label=f"下载图表 {i+1} (PNG)",
                                data=buf.getvalue(),
                                file_name=f"heatmap_{selected_sheet}_{i+1}.png",
                                mime="image/png"
                            )
                    except Exception as e:
                        st.error(f"绘图失败: {e}")
                        st.exception(e)

        # ==========================================
        # 模式 2: 除草柱图 (极坐标)
        # ==========================================
        elif mode == "除草活性柱图 (Polar Bar)":
            st.header("🌿 除草活性极坐标图")
            st.info("说明：请确保第一列为编号，后续列为不同作物的数据。")
            
            if st.button("生成图表"):
                with st.spinner("正在绘制..."):
                    try:
                        fig = pf.draw_polar_bar(df.copy(), font_size=global_font_size)
                        st.pyplot(fig)
                        
                        buf = BytesIO()
                        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                        st.download_button(
                            label="下载图表 (PNG)",
                            data=buf.getvalue(),
                            file_name=f"polar_bar_{selected_sheet}.png",
                            mime="image/png"
                        )
                    except Exception as e:
                        st.error(f"绘图失败: {e}")

        # ==========================================
        # 模式 3: 除菌柱图
        # ==========================================
        elif mode == "除菌活性柱图 (Bar Chart)":
            st.header("🍄 除菌活性柱状图")
            st.info("说明：需要包含 '生测编号', '灰霉', '赤霉' 列。如果列名不匹配，将默认使用第1、2、3列。")
            
            if st.button("生成图表"):
                with st.spinner("正在绘制..."):
                    try:
                        fig = pf.draw_fungicide_bar(df.copy(), font_size=global_font_size)
                        st.pyplot(fig)

                        buf = BytesIO()
                        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                        st.download_button(
                            label="下载图表 (PNG)",
                            data=buf.getvalue(),
                            file_name=f"fungicide_bar_{selected_sheet}.png",
                            mime="image/png"
                        )
                    except Exception as e:
                        st.error(f"绘图失败: {e}")

        # ==========================================
        # 模式 4: 数据分布箱线图
        # ==========================================
        elif mode == "数据分布箱线图 (Boxplot)":
            st.header("📦 活性数据分布箱线图")
            st.info("说明：用于展示不同测试指标（作物/菌种）的数据分布情况，快速发现异常值。")
            
            if st.button("生成箱线图"):
                with st.spinner("正在绘制..."):
                    try:
                        fig = pf.draw_boxplot(df.copy(), font_size=global_font_size)
                        st.pyplot(fig)

                        buf = BytesIO()
                        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                        st.download_button(
                            label="下载图表 (PNG)",
                            data=buf.getvalue(),
                            file_name=f"boxplot_{selected_sheet}.png",
                            mime="image/png"
                        )
                    except Exception as e:
                        st.error(f"绘图失败: {e}")

        # ==========================================
        # 模式 5: 广谱活性雷达图
        # ==========================================
        elif mode == "广谱活性雷达图 (Radar Chart)":
            st.header("🕸️ 广谱活性雷达图")
            st.info("说明：第一列为化合物编号，其余列为各靶标活性。建议数据量不要过多（只展示前6个）。")
            
            if st.button("生成雷达图"):
                with st.spinner("正在绘制..."):
                    try:
                        fig = pf.draw_radar_chart(df.copy(), font_size=global_font_size)
                        st.pyplot(fig)

                        buf = BytesIO()
                        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                        st.download_button(
                            label="下载图表 (PNG)",
                            data=buf.getvalue(),
                            file_name=f"radar_{selected_sheet}.png",
                            mime="image/png"
                        )
                    except Exception as e:
                        st.error(f"绘图失败: {e}")

        # ==========================================
        # 模式 6: 反应条件筛选气泡图
        # ==========================================
        elif mode == "反应条件筛选气泡图 (Optimization Bubble)":
            st.header("⚗️ 反应条件筛选气泡图")
            st.markdown("**列映射设置**：请选择对应的列")
            
            cols = df.columns.tolist()
            c1, c2, c3, c4 = st.columns(4)
            
            # 智能默认值
            def_x = cols[0] if len(cols) > 0 else None
            def_y = cols[1] if len(cols) > 1 else None
            def_size = cols[2] if len(cols) > 2 else None
            def_color = cols[3] if len(cols) > 3 else None
            
            x_col = c1.selectbox("X轴 (如: 催化剂)", cols, index=cols.index(def_x) if def_x else 0)
            y_col = c2.selectbox("Y轴 (如: 溶剂)", cols, index=cols.index(def_y) if def_y else 0)
            size_col = c3.selectbox("大小 (如: 产率)", cols, index=cols.index(def_size) if def_size else 0)
            color_col = c4.selectbox("颜色 (如: ee值)", cols, index=cols.index(def_color) if def_color else 0)
            
            if st.button("生成气泡图"):
                with st.spinner("正在绘制..."):
                    try:
                        # 构建新的 DF 传递给绘图函数，以适配旧接口
                        plot_df = df[[x_col, y_col, size_col, color_col]].copy()
                        fig = pf.draw_optimization_bubble(plot_df, font_size=global_font_size)
                        st.pyplot(fig)

                        buf = BytesIO()
                        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                        st.download_button(
                            label="下载图表 (PNG)",
                            data=buf.getvalue(),
                            file_name=f"bubble_opt_{selected_sheet}.png",
                            mime="image/png"
                        )
                    except Exception as e:
                        st.error(f"绘图失败: {e}")
                        st.exception(e)

        # ==========================================
        # 模式 7: 反应能级图
        # ==========================================
        elif mode == "反应能级图 (Energy Profile)":
            st.header("📈 反应能级图 (Reaction Profile)")
            
            cols = df.columns.tolist()
            step_col = st.selectbox("步骤名称列 (Step)", cols, index=0)
            energy_cols = st.multiselect("能量数据列 (Energy Paths)", cols, default=cols[1:] if len(cols) > 1 else [])
            
            if not energy_cols:
                st.warning("请至少选择一列作为能量数据")
            
            if st.button("生成能级图"):
                if energy_cols:
                    with st.spinner("正在绘制..."):
                        try:
                            # 重组数据
                            plot_df = df[[step_col] + energy_cols].copy()
                            fig = pf.draw_energy_profile(plot_df, font_size=global_font_size)
                            st.pyplot(fig)

                            buf = BytesIO()
                            fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                            st.download_button(
                                label="下载图表 (PNG)",
                                data=buf.getvalue(),
                                file_name=f"energy_profile_{selected_sheet}.png",
                                mime="image/png"
                            )
                        except Exception as e:
                            st.error(f"绘图失败: {e}")
                            st.exception(e)

        # ==========================================
        # 模式 8: 反应动力学曲线
        # ==========================================
        elif mode == "反应动力学曲线 (Kinetics)":
            st.header("⏱️ 反应动力学曲线")
            
            cols = df.columns.tolist()
            time_col = st.selectbox("时间列 (Time)", cols, index=0)
            yield_cols = st.multiselect("产率数据列 (Yields)", cols, default=cols[1:] if len(cols) > 1 else [])
            
            if not yield_cols:
                st.warning("请至少选择一列作为产率数据")
                
            if st.button("生成动力学曲线"):
                if yield_cols:
                    with st.spinner("正在绘制..."):
                        try:
                            plot_df = df[[time_col] + yield_cols].copy()
                            fig = pf.draw_kinetics(plot_df, font_size=global_font_size)
                            st.pyplot(fig)

                            buf = BytesIO()
                            fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                            st.download_button(
                                label="下载图表 (PNG)",
                                data=buf.getvalue(),
                                file_name=f"kinetics_{selected_sheet}.png",
                                mime="image/png"
                            )
                        except Exception as e:
                            st.error(f"绘图失败: {e}")
                            st.exception(e)

    except Exception as e:
        st.error(f"无法读取文件: {e}")
else:
    st.info("请在左侧上传 Excel 文件以开始。")
    
    # 显示示例说明
    st.markdown("### 数据格式说明")
    st.markdown("""
    - **热图**: 第一列为编号，其余列为数值（0-1 或 0-100）。
    - **除草**: 第一列为编号，其余列为作物名称和数值。
    - **除菌**: 需包含 '生测编号', '灰霉', '赤霉' 列。
    - **箱线图**: 第一列为编号，其余为数值列。
    - **雷达图**: 第一列为编号，其余为各维度指标。
    - **气泡图**: 需4列数据：[变量A, 变量B, 大小(产率), 颜色(ee)]。
    - **能级图**: 第一列为步骤，后续为能量数值。
    - **动力学**: 第一列为时间，后续为不同条件的产率。
    """)