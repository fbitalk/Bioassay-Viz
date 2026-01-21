import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os
import plot_functions as pf

# 设置页面配置
st.set_page_config(page_title="数据可视化工具", layout="wide")

# 标题
st.title("📊 生测数据可视化工具")
st.markdown("上传 Excel 文件，自动生成热图、柱状图。")

# 侧边栏：功能选择
mode = st.sidebar.selectbox(
    "选择功能模块",
    ("热图生成 (Heatmap)", "除草活性柱图 (Polar Bar)", "除菌活性柱图 (Bar Chart)")
)

# 通用文件上传
uploaded_file = st.sidebar.file_uploader("上传 Excel 文件", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 读取 Excel 的所有 Sheet 名称
        xl = pd.ExcelFile(uploaded_file)
        sheet_names = xl.sheet_names
        
        st.sidebar.markdown("---")
        selected_sheet = st.sidebar.selectbox("选择工作表 (Sheet)", sheet_names)
        
        # 读取数据
        df = xl.parse(selected_sheet)
        
        st.subheader("数据预览")
        st.dataframe(df.head())
        
        # ==========================================
        # 模式 1: 热图生成
        # ==========================================
        if mode == "热图生成 (Heatmap)":
            st.header("🔥 活性热图")
            
            with st.expander("高级设置"):
                split_index = st.text_input("分割点编号 (例如: Ⅲ2-16)", value="Ⅲ2-16")
            
            if st.button("生成热图"):
                with st.spinner("正在绘制热图..."):
                    try:
                        figures = pf.draw_heatmap(df.copy(), split_index)
                        
                        # 确保输出目录存在
                        output_dir = "output"
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                            
                        for i, fig in enumerate(figures):
                            st.pyplot(fig)
                            
                            # 保存到本地
                            local_path = os.path.join(output_dir, f"heatmap_{selected_sheet}_{i+1}.png")
                            fig.savefig(local_path, format="png", dpi=300, bbox_inches='tight')
                            st.success(f"图片已保存至: {local_path}")

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
                        fig = pf.draw_polar_bar(df.copy())
                        st.pyplot(fig)
                        
                        # 确保输出目录存在
                        output_dir = "output"
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)

                        # 保存到本地
                        local_path = os.path.join(output_dir, f"polar_bar_{selected_sheet}.png")
                        fig.savefig(local_path, format="png", dpi=300, bbox_inches='tight')
                        st.success(f"图片已保存至: {local_path}")

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
                        fig = pf.draw_fungicide_bar(df.copy())
                        st.pyplot(fig)
                        
                        # 确保输出目录存在
                        output_dir = "output"
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)

                        # 保存到本地
                        local_path = os.path.join(output_dir, f"fungicide_bar_{selected_sheet}.png")
                        fig.savefig(local_path, format="png", dpi=300, bbox_inches='tight')
                        st.success(f"图片已保存至: {local_path}")

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
    """)