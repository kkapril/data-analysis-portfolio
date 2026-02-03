#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ==============================
# 电信客户流失分析 - 多维度分析报告
# ==============================

# 导入必要的库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import os
import warnings
warnings.filterwarnings('ignore')

# 创建保存目录
output_dir = r'D:\study\portfolio\telecom-churn-analysis'
images_dir = os.path.join(output_dir, 'images')
os.makedirs(output_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

# 设置中文字体（用于文本输出）
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置专业图表样式
plt.style.use('seaborn-darkgrid')
sns.set_palette("husl")
rcParams['figure.figsize'] = (12, 8)

# ==============================
# 1. 数据加载与初步探索
# ==============================

print("=" * 50)
print("电信客户流失分析 - 多维度分析报告")
print("=" * 50)

# 加载数据
df = pd.read_csv(r'D:\study\portfolio\telecom-churn-analysis\WA_Fn-UseC_-Telco-Customer-Churn.csv')

# 初步数据探索
print("\n📊 数据集概览:")
print(f"数据形状: {df.shape}")
print(f"行数: {df.shape[0]}, 列数: {df.shape[1]}")

print("\n📋 数据列信息:")
print(df.info())

print("\n🔍 数据描述性统计:")
print(df.describe())

print("\n🔍 分类变量概览:")
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"{col}: {df[col].nunique()} 个唯一值")

# ==============================
# 2. 数据预处理
# ==============================

print("\n" + "=" * 50)
print("数据预处理阶段")
print("=" * 50)

# 创建数据备份
df_original = df.copy()

# 2.1 处理缺失值和异常值
print("\n🔧 处理缺失值...")
print(f"TotalCharges 缺失值数量: {df['TotalCharges'].eq(' ').sum()}")

# 将TotalCharges中的空格转换为NaN，然后转换为数值
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(' ', np.nan), errors='coerce')

# 填充缺失值 - 使用月费乘以在网月数
missing_mask = df['TotalCharges'].isna()
df.loc[missing_mask, 'TotalCharges'] = df.loc[missing_mask, 'MonthlyCharges'] * df.loc[missing_mask, 'tenure']

print(f"处理后缺失值数量: {df['TotalCharges'].isna().sum()}")

# 2.2 数据类型转换
# 将二元分类变量转换为0/1
binary_mapping = {'Yes': 1, 'No': 0, 'Female': 0, 'Male': 1}
df['gender'] = df['gender'].map(binary_mapping)
df['Partner'] = df['Partner'].map(binary_mapping)
df['Dependents'] = df['Dependents'].map(binary_mapping)
df['PhoneService'] = df['PhoneService'].map(binary_mapping)
df['PaperlessBilling'] = df['PaperlessBilling'].map(binary_mapping)
df['Churn'] = df['Churn'].map(binary_mapping)

print("\n✅ 数据预处理完成!")

# ==============================
# 3. 客户流失总体分析 (ENGLISH LABELS)
# ==============================

print("\n" + "=" * 50)
print("客户流失总体分析")
print("=" * 50)

# 计算流失率
churn_rate = df['Churn'].mean() * 100
churn_count = df['Churn'].sum()
total_customers = len(df)

print(f"📈 总体流失分析:")
print(f"总客户数: {total_customers:,}")
print(f"流失客户数: {churn_count:,}")
print(f"流失率: {churn_rate:.2f}%")
print(f"留存客户数: {total_customers - churn_count:,}")
print(f"留存率: {100 - churn_rate:.2f}%")

# 创建流失分布可视化 (ENGLISH LABELS)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 子图1: 流失分布饼图
churn_counts = df['Churn'].value_counts()
colors = ['#2E86AB', '#A23B72']
axes[0].pie(churn_counts, labels=['Stayed', 'Churned'], autopct='%1.1f%%', 
           colors=colors, startangle=90, explode=(0.05, 0))
axes[0].set_title('Customer Churn Distribution', fontsize=14, fontweight='bold')

# 子图2: 流失客户数量柱状图 (ENGLISH LABELS)
sns.countplot(data=df, x='Churn', ax=axes[1], palette=colors)
axes[1].set_title('Customer Churn Count Comparison', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Churn Status')
axes[1].set_ylabel('Number of Customers')
axes[1].set_xticklabels(['Stayed', 'Churned'])

# 添加数量标签
for i, v in enumerate(churn_counts):
    axes[1].text(i, v + 50, str(v), ha='center', fontweight='bold')

# 子图3: 流失率趋势（按tenure分组）(ENGLISH LABELS)
tenure_churn = df.groupby('tenure')['Churn'].mean().reset_index()
axes[2].plot(tenure_churn['tenure'], tenure_churn['Churn'] * 100, 
            linewidth=2.5, color='#A23B72')
axes[2].fill_between(tenure_churn['tenure'], tenure_churn['Churn'] * 100, 
                     alpha=0.3, color='#A23B72')
axes[2].set_title('Tenure vs Churn Rate', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Tenure (Months)')
axes[2].set_ylabel('Churn Rate (%)')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(images_dir, 'churn_overview.png'), dpi=300, bbox_inches='tight')
plt.show()

# ==============================
# 4. 人口统计特征分析 (ENGLISH LABELS)
# ==============================

print("\n" + "=" * 50)
print("人口统计特征分析")
print("=" * 50)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

# 分析维度列表
demographic_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents']
titles = ['Gender', 'Senior Citizen', 'Partner', 'Dependents']
colors_demo = ['#4B8BBE', '#FFD43B', '#306998', '#646464']

for idx, (feature, title) in enumerate(zip(demographic_features, titles)):
    # 计算每个特征的流失率
    churn_by_feature = df.groupby(feature)['Churn'].agg(['mean', 'count']).reset_index()
    
    # 条形图 - 客户数量 (ENGLISH LABELS)
    feature_counts = df[feature].value_counts().sort_index()
    
    # 设置x轴标签
    if feature == 'gender':
        labels = ['Female', 'Male']
    else:
        labels = ['No', 'Yes']
    
    axes[idx].bar(range(len(feature_counts)), feature_counts.values, 
                  color=colors_demo[idx], alpha=0.7, label='Customer Count')
    axes[idx].set_xticks(range(len(feature_counts)))
    axes[idx].set_xticklabels(labels)
    axes[idx].set_ylabel('Customer Count')
    axes[idx].set_title(f'{title} Distribution', fontweight='bold')
    
    # 添加第二y轴显示流失率 (ENGLISH LABELS)
    ax2 = axes[idx].twinx()
    ax2.plot(range(len(churn_by_feature)), churn_by_feature['mean'] * 100, 
             color='#A23B72', marker='o', linewidth=2, label='Churn Rate')
    ax2.set_ylabel('Churn Rate (%)', color='#A23B72')
    ax2.tick_params(axis='y', labelcolor='#A23B72')
    
    # 添加图例
    lines1, labels1 = axes[idx].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    axes[idx].legend(lines1 + lines2, labels1 + labels2, loc='upper right')

# 人口统计特征对流失率的影响（热力图）(ENGLISH LABELS)
demographic_data = []
for feature in demographic_features:
    churn_rates = df.groupby(feature)['Churn'].mean()
    demographic_data.append(churn_rates.values)

# 设置行标签和列标签为英文
demographic_df = pd.DataFrame(demographic_data, 
                             index=['Gender', 'Senior Citizen', 'Partner', 'Dependents'],
                             columns=[['No', 'Yes'] if feature != 'gender' else ['Female', 'Male']][0])

axes[4].axis('off')  # 隐藏第五个子图
ax_heatmap = fig.add_subplot(2, 3, 5)  # 创建新的子图位置
sns.heatmap(demographic_df * 100, annot=True, fmt='.1f', cmap='YlOrRd', 
            cbar_kws={'label': 'Churn Rate (%)'}, ax=ax_heatmap)
ax_heatmap.set_title('Demographic Churn Rate Heatmap', fontweight='bold')

# 特征重要性分析（使用卡方检验简化版）
print("\n📊 人口特征流失率统计:")
for feature in demographic_features:
    if feature == 'gender':
        feature_name = '性别'
    elif feature == 'SeniorCitizen':
        feature_name = '老年人'
    elif feature == 'Partner':
        feature_name = '伴侣'
    elif feature == 'Dependents':
        feature_name = '家属'
    
    churn_stats = df.groupby(feature)['Churn'].agg(['mean', 'count'])
    print(f"\n{feature_name}:")
    for val in churn_stats.index:
        if feature == 'gender':
            label = '男' if val == 1 else '女'
        else:
            label = '是' if val == 1 else '否'
        print(f"  {label}: {churn_stats.loc[val, 'count']:,} 客户, 流失率: {churn_stats.loc[val, 'mean']*100:.1f}%")

# 隐藏第六个子图
axes[5].axis('off')

plt.tight_layout()
plt.savefig(os.path.join(images_dir, 'demographic_analysis.png'), dpi=300, bbox_inches='tight')
plt.show()

# ==============================
# 5. 服务使用特征分析 (ENGLISH LABELS)
# ==============================

print("\n" + "=" * 50)
print("服务使用特征分析")
print("=" * 50)

# 定义服务相关特征
service_features = ['PhoneService', 'MultipleLines', 'InternetService', 
                    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                    'TechSupport', 'StreamingTV', 'StreamingMovies']

# 过滤掉非服务特征（如'No internet service'）
service_df = df.copy()
for feature in ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                'TechSupport', 'StreamingTV', 'StreamingMovies']:
    service_df[feature] = service_df[feature].replace('No internet service', 'No')

# 创建服务分析可视化 (ENGLISH LABELS)
fig, axes = plt.subplots(3, 3, figsize=(18, 15))
axes = axes.flatten()

# 分析每个服务的流失率
service_churn_rates = []
service_names = []

for idx, feature in enumerate(service_features):
    if idx >= len(axes):
        break
    
    # 处理MultipleLines的特殊值
    if feature == 'MultipleLines':
        temp_df = service_df[service_df['MultipleLines'] != 'No phone service']
    else:
        temp_df = service_df
    
    # 计算流失率
    churn_by_service = temp_df.groupby(feature)['Churn'].agg(['mean', 'count']).reset_index()
    
    # 使用原始标签
    labels = churn_by_service[feature].tolist()
    
    # 绘制条形图 (ENGLISH LABELS)
    bars = axes[idx].bar(range(len(churn_by_service)), churn_by_service['mean'] * 100,
                         color=['#4B8BBE', '#FFD43B', '#306998'][:len(churn_by_service)])
    axes[idx].set_xticks(range(len(churn_by_service)))
    axes[idx].set_xticklabels(labels, rotation=45)
    axes[idx].set_ylabel('Churn Rate (%)')
    
    # 设置标题 (ENGLISH LABELS)
    axes[idx].set_title(f'{feature}\nChurn Rate Analysis', fontweight='bold')
    
    # 添加数值标签
    for bar_idx, bar in enumerate(bars):
        height = bar.get_height()
        axes[idx].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                      f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # 保存数据用于汇总
    if len(churn_by_service) > 1:
        max_churn = churn_by_service['mean'].max() * 100
        service_churn_rates.append(max_churn)
        service_names.append(feature)

plt.tight_layout()
plt.savefig(os.path.join(images_dir, 'service_analysis.png'), dpi=300, bbox_inches='tight')
plt.show()

# 服务捆绑分析
print("\n🔍 互联网服务类型分析:")
internet_analysis = service_df.groupby('InternetService')['Churn'].agg(['mean', 'count'])
for service in internet_analysis.index:
    count = internet_analysis.loc[service, 'count']
    churn_rate = internet_analysis.loc[service, 'mean'] * 100
    print(f"  {service}: {count:,} 客户, 流失率: {churn_rate:.1f}%")

# ==============================
# 6. 合同与支付方式分析 (ENGLISH LABELS)
# ==============================

print("\n" + "=" * 50)
print("合同与支付方式分析")
print("=" * 50)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 子图1: 合同类型分析 (ENGLISH LABELS)
contract_churn = df.groupby('Contract')['Churn'].agg(['mean', 'count']).sort_values('mean')
bars1 = axes[0].bar(range(len(contract_churn)), contract_churn['mean'] * 100, 
                   color=['#4B8BBE', '#FFD43B', '#A23B72'])
axes[0].set_xticks(range(len(contract_churn)))
axes[0].set_xticklabels(contract_churn.index)
axes[0].set_ylabel('Churn Rate (%)')
axes[0].set_title('Contract Type vs Churn Rate', fontsize=14, fontweight='bold')

# 添加数值标签
for i, (bar, (_, row)) in enumerate(zip(bars1, contract_churn.iterrows())):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%\n({row["count"]:,})', ha='center', va='bottom')

# 子图2: 支付方式分析 (ENGLISH LABELS)
payment_churn = df.groupby('PaymentMethod')['Churn'].agg(['mean', 'count']).sort_values('mean')
bars2 = axes[1].bar(range(len(payment_churn)), payment_churn['mean'] * 100, 
                   color=['#4B8BBE', '#FFD43B', '#A23B72', '#306998'])
axes[1].set_xticks(range(len(payment_churn)))
axes[1].set_xticklabels(payment_churn.index, rotation=15, ha='right')
axes[1].set_ylabel('Churn Rate (%)')
axes[1].set_title('Payment Method vs Churn Rate', fontsize=14, fontweight='bold')

# 添加数值标签
for i, (bar, (_, row)) in enumerate(zip(bars2, payment_churn.iterrows())):
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%\n({row["count"]:,})', ha='center', va='bottom')

plt.tight_layout()
plt.savefig(os.path.join(images_dir, 'contract_payment_analysis.png'), dpi=300, bbox_inches='tight')
plt.show()

print("\n📊 合同类型详细分析:")
for contract in contract_churn.index:
    count = contract_churn.loc[contract, 'count']
    churn_rate = contract_churn.loc[contract, 'mean'] * 100
    print(f"  {contract}: {count:,} 客户, 流失率: {churn_rate:.1f}%")

print("\n💳 支付方式详细分析:")
for method in payment_churn.index:
    count = payment_churn.loc[method, 'count']
    churn_rate = payment_churn.loc[method, 'mean'] * 100
    print(f"  {method}: {count:,} 客户, 流失率: {churn_rate:.1f}%")

# ==============================
# 7. 财务指标分析 (ENGLISH LABELS)
# ==============================

print("\n" + "=" * 50)
print("财务指标分析")
print("=" * 50)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 子图1: 月费分布 (ENGLISH LABELS)
axes[0, 0].hist([df[df['Churn'] == 0]['MonthlyCharges'], 
                 df[df['Churn'] == 1]['MonthlyCharges']],
                bins=30, alpha=0.7, label=['Stayed', 'Churned'],
                color=['#4B8BBE', '#A23B72'])
axes[0, 0].set_xlabel('Monthly Charges ($)')
axes[0, 0].set_ylabel('Customer Count')
axes[0, 0].set_title('Monthly Charges Distribution - Stayed vs Churned', fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 子图2: 总费用分布 (ENGLISH LABELS)
axes[0, 1].hist([df[df['Churn'] == 0]['TotalCharges'], 
                 df[df['Churn'] == 1]['TotalCharges']],
                bins=30, alpha=0.7, label=['Stayed', 'Churned'],
                color=['#4B8BBE', '#A23B72'])
axes[0, 1].set_xlabel('Total Charges ($)')
axes[0, 1].set_ylabel('Customer Count')
axes[0, 1].set_title('Total Charges Distribution - Stayed vs Churned', fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 子图3: 月费与流失率关系 (ENGLISH LABELS)
monthly_bins = pd.cut(df['MonthlyCharges'], bins=10)
monthly_churn = df.groupby(monthly_bins)['Churn'].mean()
axes[1, 0].plot(range(len(monthly_churn)), monthly_churn.values * 100, 
                marker='o', linewidth=2, color='#A23B72')
axes[1, 0].fill_between(range(len(monthly_churn)), monthly_churn.values * 100, 
                        alpha=0.3, color='#A23B72')
axes[1, 0].set_xticks(range(len(monthly_churn)))
axes[1, 0].set_xticklabels([str(x) for x in monthly_churn.index], rotation=45)
axes[1, 0].set_xlabel('Monthly Charges Range ($)')
axes[1, 0].set_ylabel('Churn Rate (%)')
axes[1, 0].set_title('Monthly Charges Range vs Churn Rate', fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# 子图4: 在网时长与总费用关系 (ENGLISH LABELS)
scatter = axes[1, 1].scatter(df['tenure'], df['TotalCharges'], 
                            c=df['Churn'], alpha=0.6, cmap='coolwarm',
                            s=30)
axes[1, 1].set_xlabel('Tenure (Months)')
axes[1, 1].set_ylabel('Total Charges ($)')
axes[1, 1].set_title('Tenure vs Total Charges (Color: Churn)', fontweight='bold')
plt.colorbar(scatter, ax=axes[1, 1], label='Churn (0=Stayed, 1=Churned)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(images_dir, 'financial_analysis.png'), dpi=300, bbox_inches='tight')
plt.show()

# 财务指标统计
print("\n💰 财务指标统计:")
print(f"平均月费: ${df['MonthlyCharges'].mean():.2f}")
print(f"平均总费用: ${df['TotalCharges'].mean():.2f}")
print(f"平均在网时长: {df['tenure'].mean():.1f} 月")

print("\n💰 留存客户 vs 流失客户财务对比:")
churn_stats = df.groupby('Churn')[['MonthlyCharges', 'TotalCharges', 'tenure']].mean()
print("留存客户:")
print(f"  平均月费: ${churn_stats.loc[0, 'MonthlyCharges']:.2f}")
print(f"  平均总费用: ${churn_stats.loc[0, 'TotalCharges']:.2f}")
print(f"  平均在网时长: {churn_stats.loc[0, 'tenure']:.1f} 月")

print("\n流失客户:")
print(f"  平均月费: ${churn_stats.loc[1, 'MonthlyCharges']:.2f}")
print(f"  平均总费用: ${churn_stats.loc[1, 'TotalCharges']:.2f}")
print(f"  平均在网时长: {churn_stats.loc[1, 'tenure']:.1f} 月")

# ==============================
# 8. 多维度综合分析 (ENGLISH LABELS)
# ==============================

print("\n" + "=" * 50)
print("多维度综合分析")
print("=" * 50)

# 创建综合热力图 - 特征相关性分析
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# 准备数值特征数据
numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen', 
                    'gender', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']

# 计算相关系数矩阵
correlation_matrix = df[numeric_features + ['Churn']].corr()

# 子图1: 特征相关性热力图 (ENGLISH LABELS)
im = axes[0].imshow(correlation_matrix, cmap='coolwarm', aspect='auto')
axes[0].set_xticks(range(len(correlation_matrix.columns)))
axes[0].set_yticks(range(len(correlation_matrix.columns)))
axes[0].set_xticklabels([col for col in correlation_matrix.columns], rotation=45, ha='right')
axes[0].set_yticklabels([col for col in correlation_matrix.columns])
axes[0].set_title('Feature Correlation Heatmap', fontweight='bold', fontsize=14)

# 添加相关系数值
for i in range(len(correlation_matrix.columns)):
    for j in range(len(correlation_matrix.columns)):
        text = axes[0].text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                           ha="center", va="center", color="w", fontsize=9)

# 子图2: 与流失最相关的特征 (ENGLISH LABELS)
churn_corr = correlation_matrix['Churn'].drop('Churn').sort_values(ascending=False)
bars = axes[1].barh(range(len(churn_corr)), churn_corr.values,
                   color=np.where(churn_corr.values > 0, '#A23B72', '#4B8BBE'))
axes[1].set_yticks(range(len(churn_corr)))
axes[1].set_yticklabels([label for label in churn_corr.index])
axes[1].set_xlabel('Correlation Coefficient')
axes[1].set_title('Feature Correlation with Churn', fontweight='bold', fontsize=14)
axes[1].axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# 添加数值标签
for i, (bar, val) in enumerate(zip(bars, churn_corr.values)):
    axes[1].text(val + (0.01 if val >= 0 else -0.01), i, f'{val:.3f}',
                va='center', ha='left' if val >= 0 else 'right',
                color='black', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(images_dir, 'correlation_analysis.png'), dpi=300, bbox_inches='tight')
plt.show()

# ==============================
# 9. 业务洞察与建议
# ==============================

print("\n" + "=" * 50)
print("业务洞察与建议")
print("=" * 50)

print("\n🎯 关键发现:")
print("1. 📉 总体流失率: {:.1f}%".format(churn_rate))
print("2. 🔍 高流失群体特征:")
print("   - 使用光纤互联网服务的客户")
print("   - 月费较高的客户")
print("   - 使用月付合同的客户")
print("   - 使用电子支票支付的客户")
print("   - 在网时间较短的客户")

print("\n3. 📊 低流失群体特征:")
print("   - 使用两年期合同的客户")
print("   - 使用自动支付方式的客户")
print("   - 使用DSL互联网服务的客户")
print("   - 在网时间较长的客户")

print("\n💡 战略建议:")
print("1. 🎯 目标客户干预:")
print("   - 重点关注使用光纤互联网+月付合同+电子支票的客户")
print("   - 对新客户（在网时间<6个月）加强客户关系管理")

print("\n2. 📋 产品与服务优化:")
print("   - 推广长期合同优惠（年付/两年付折扣）")
print("   - 推广自动支付方式的奖励计划")
print("   - 为光纤用户提供增值服务捆绑")

print("\n3. 💰 定价策略调整:")
print("   - 针对高月费客户提供个性化套餐")
print("   - 建立客户忠诚度计划，奖励长期客户")

print("\n4. 📞 客户服务改进:")
print("   - 对高风险流失客户进行主动关怀")
print("   - 改善光纤客户的技术支持服务")

print("\n5. 📈 监控指标:")
print("   - 月流失率变化趋势")
print("   - 客户生命周期价值（LTV）")
print("   - 新客户第1-3个月的留存率")

# ==============================
# 10. 数据导出
# ==============================

print("\n" + "=" * 50)
print("数据导出")
print("=" * 50)

# 导出处理后的数据
output_data_path = os.path.join(output_dir, 'telecom_churn_processed.csv')
df.to_csv(output_data_path, index=False)
print(f"✅ 处理后的数据已保存为: {output_data_path}")

# 导出分析摘要
analysis_summary = f"""
电信客户流失分析报告
生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

关键指标:
- 总客户数: {total_customers:,}
- 流失客户数: {churn_count:,}
- 总体流失率: {churn_rate:.2f}%

高流失特征:
1. 合同类型: 月付合同流失率最高
2. 互联网服务: 光纤用户流失率最高
3. 支付方式: 电子支票用户流失率最高
4. 在网时长: 低于12个月的客户流失风险高

业务建议:
1. 针对高风险客户群体制定保留策略
2. 推广长期合同和自动支付方式
3. 优化光纤客户的服务体验
4. 加强新客户的留存管理
"""

summary_path = os.path.join(output_dir, 'analysis_summary.txt')
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(analysis_summary)

print(f"✅ 分析摘要已保存为: {summary_path}")

# 列出所有保存的文件
print("\n📁 生成的文件:")
print(f"1. 处理后的数据: {output_data_path}")
print(f"2. 分析摘要: {summary_path}")
print(f"3. 可视化图表:")
for file in os.listdir(images_dir):
    if file.endswith('.png'):
        print(f"   - {os.path.join(images_dir, file)}")

print(f"\n🎉 分析完成! 所有文件已保存到: {output_dir}")


# In[ ]:





# In[ ]:




