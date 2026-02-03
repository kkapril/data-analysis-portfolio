# 电信客户流失分析项目

## 项目概述
本项目通过对电信客户流失数据的多维度分析，识别关键流失驱动因素，为企业提供数据驱动的决策支持。分析涵盖数据预处理、探索性分析、可视化展示和业务洞察等完整流程。

## 项目目标
1. 识别客户流失的主要影响因素
2. 分析不同客户群体的流失特征
3. 为企业提供降低流失率的策略建议
4. 建立可复用的数据分析框架


## 项目结构
telecom-churn-analysis/                            
├── telecom_churn_analysis.py                 (主脚本)                       
├── WA_Fn-UseC_-Telco-Customer-Churn.csv      (原始数据)             
├── telecom_churn_processed.csv               (处理数据)  
├── analysis_summary.txt                      (结果摘要)  
├── images                                    (图表目录)  
│   ├── churn_overview.png                 
│   ├── demographic_analysis.png           
│   ├── service_analysis.png               
│   ├── contract_payment_analysis.png      
│   ├── financial_analysis.png             
│   └── correlation_analysis.png           
├── requirements.txt                          (依赖列表)                    
└── README.md                                 (项目说明)


## 技术栈
- Python 3.8+
- Pandas (数据处理)
- Matplotlib & Seaborn (数据可视化)
- NumPy (数值计算)

## 数据来源
数据集来自Kaggle的Telco Customer Churn数据集，包含7043名电信客户的信息。

## 分析流程
1. 数据加载与探索: 加载数据，查看数据结构，识别数据质量问题
2. 数据清洗与预处理: 处理缺失值，转换数据类型，处理异常值
3. 探索性数据分析: 统计描述，分布分析，相关性分析
4. 多维度可视化分析: 人口统计、服务使用、合同类型、财务指标等维度
5. 业务洞察提取: 识别关键流失因素，提出业务建议
6. 结果输出: 生成可视化图表和分析报告

## 关键分析维度
1. 总体流失分析: 总体流失率26.5%，流失客户1869人
2. 人口统计特征: 老年人、无伴侣、无家属的客户流失率较高
3. 服务使用特征: 光纤互联网服务用户流失率最高（41.9%）
4. 合同与支付: 月付合同、电子支票支付的客户流失风险最高
5. 财务指标: 高月费客户流失率较高，在网时间与流失率呈负相关

## 主要发现
1. 高流失群体特征:
   - 使用光纤互联网服务
   - 采用月付合同
   - 使用电子支票支付
   - 在网时间少于12个月

2. 低流失群体特征:
   - 使用两年期合同
   - 采用自动支付方式
   - 使用DSL互联网服务
   - 在网时间超过24个月

## 业务建议
1. 客户分层管理: 针对高流失风险客户制定主动干预策略
2. 产品优化: 推广长期合同套餐，优化光纤服务体验
3. 支付方式引导: 鼓励客户采用自动支付方式
4. 新客户关怀: 加强新客户前6个月的关系维护

## 使用方法

### 环境准备
```bash
pip install -r requirements.txt


### 运行分析
python telecom_churn_analysis.py

### 查看结果
   - 分析结果将输出到控制台		
   - 可视化图表将保存到images文件夹
   - 处理后的数据将保存为telecom_churn_processed.csv
   - 分析摘要将保存为analysis_summary.txt

### 文件说明
   - telecom_churn_analysis.py: 主分析脚本，包含完整的数据处理和分析流程
   - WA_Fn-UseC_-Telco-Customer-Churn.csv: 原始数据集，来自Kaggle
   - telecom_churn_processed.csv: 清洗和处理后的数据集
   - analysis_summary.txt: 分析关键发现和业务建议摘要
   - images/: 包含所有生成的可视化图表
