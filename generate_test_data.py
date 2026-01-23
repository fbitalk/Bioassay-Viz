import pandas as pd
import numpy as np

# ==========================================
# 1. 生成通用/除草活性数据 (适合雷达图、箱线图、极坐标图)
# ==========================================
def create_herbicidal_data():
    np.random.seed(42)
    compounds = [f"化合物-{i+1:02d}" for i in range(8)]
    crops = ['稗草', '马唐', '狗尾草', '反枝苋', '苘麻', '小麦', '玉米']
    
    data = np.random.randint(0, 101, size=(len(compounds), len(crops)))
    
    # 模拟一些特定的活性模式
    # 化合物-01: 广谱高活性
    data[0] = [95, 98, 92, 100, 96, 10, 15]
    # 化合物-02: 对阔叶杂草有效
    data[1] = [10, 15, 12, 98, 95, 0, 0]
    
    df = pd.DataFrame(data, columns=crops)
    df.insert(0, '生测编号', compounds)
    return df

# ==========================================
# 2. 生成除菌活性数据 (适合除菌柱状图)
# ==========================================
def create_fungicidal_data():
    np.random.seed(2023)
    compounds = [f"B-{i+1:03d}" for i in range(10)]
    # 必须包含 '灰霉', '赤霉'
    diseases = ['灰霉', '赤霉', '白粉', '锈病']
    
    data = np.random.randint(0, 101, size=(len(compounds), len(diseases)))
    df = pd.DataFrame(data, columns=diseases)
    df.insert(0, '生测编号', compounds)
    return df

# ==========================================
# 3. 生成热图数据 (适合热图)
# ==========================================
def create_heatmap_data():
    # 模拟包含不同批次的编号，用于测试分割功能
    rows = []
    
    # 批次 1: Ⅲ 系列
    for i in range(1, 11):
        rows.append(f"Ⅲ 2-{i:02d}")
        
    # 批次 2: CK 和 对照
    rows.append("CK")
    rows.append("阿维菌素")
    
    cols = ['100 ppm', '50 ppm', '25 ppm', '12.5 ppm', '6.25 ppm', '3.125 ppm']
    
    data = []
    for r in rows:
        if r == "CK":
            data.append([0, 0, 0, 0, 0, 0])
        elif r == "阿维菌素":
            data.append([100, 100, 100, 95, 80, 60])
        else:
            # 模拟剂量效应：浓度越低活性越低
            base_activity = np.random.randint(80, 100)
            row_data = []
            for j in range(len(cols)):
                act = max(0, base_activity - j * np.random.randint(10, 20))
                row_data.append(act)
            data.append(row_data)
            
    df = pd.DataFrame(data, columns=cols)
    df.insert(0, '生测编号', rows)
    return df

# ==========================================
# 4. 生成反应条件筛选数据 (适合气泡图)
# ==========================================
def create_optimization_data():
    np.random.seed(888)
    data = {
        'Catalyst': [],
        'Solvent': [],
        'Yield': [],
        'ee': []
    }
    
    catalysts = ['Cat. A', 'Cat. B', 'Cat. C', 'Cat. D', 'Cat. E']
    solvents = ['THF', 'DCM', 'Toluene', 'MeCN', 'DMF']
    
    for cat in catalysts:
        for solv in solvents:
            data['Catalyst'].append(cat)
            data['Solvent'].append(solv)
            
            base_yield = np.random.randint(10, 60)
            base_ee = np.random.randint(0, 50)
            
            if cat == 'Cat. C':
                base_yield += 30
                base_ee += 40
            if solv == 'Toluene':
                base_yield += 15
                base_ee += 10
                
            final_yield = min(99, base_yield + np.random.randint(-5, 5))
            final_ee = min(99, base_ee + np.random.randint(-5, 5))
            
            data['Yield'].append(max(0, final_yield))
            data['ee'].append(max(0, final_ee))
            
    return pd.DataFrame(data)

# ==========================================
# 5. 生成反应能级数据 (适合能级图)
# ==========================================
def create_energy_profile_data():
    # 模拟两条路径：有催化剂 vs 无催化剂
    data = {
        'Step': ['Reactant', 'TS1', 'Intermediate', 'TS2', 'Product'],
        'Uncatalyzed_Energy': [0.0, 28.5, 15.2, 22.1, -8.5],
        'Catalyzed_Energy': [0.0, 14.8, 6.5, 9.2, -8.5]
    }
    return pd.DataFrame(data)

# ==========================================
# 保存到 Excel
# ==========================================
if __name__ == "__main__":
    file_name = "test_data.xlsx"
    
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        df1 = create_herbicidal_data()
        df1.to_excel(writer, sheet_name='除草&广谱测试', index=False)
        
        df2 = create_fungicidal_data()
        df2.to_excel(writer, sheet_name='除菌测试', index=False)
        
        df3 = create_heatmap_data()
        df3.to_excel(writer, sheet_name='热图测试', index=False)

        df4 = create_optimization_data()
        df4.to_excel(writer, sheet_name='反应条件筛选', index=False)

        df5 = create_energy_profile_data()
        df5.to_excel(writer, sheet_name='反应能级数据', index=False)
        
    print(f"成功生成测试文件: {file_name}")
    print("包含工作表: '除草&广谱测试', '除菌测试', '热图测试', '反应条件筛选', '反应能级数据'")