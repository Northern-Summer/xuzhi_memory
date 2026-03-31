# 整合建模 (Integrative Modelling)

## 定义
整合建模是一种方法论框架，将预测性方法（机器学习）与解释性方法（因果推断）结合，实现既准确又可解释的社会科学研究。

---

## 核心原则

### 1. 预测与解释的辩证统一

**传统二分**（Breiman, 2001）：
| 文化 | 目标 | 方法 |
|------|------|------|
| 数据建模文化 | 解释 | 统计模型、因果推断 |
| 算法建模文化 | 预测 | 机器学习、深度学习 |

**整合视角**（Hofman et al., 2021, Nature）：
> "计算社会科学需要整合解释与预测，而非二选一。"

### 2. 四象限框架

| | 解释优先 | 预测优先 |
|---|---------|---------|
| **理论驱动** | 传统社会科学 | 理论-预测整合 |
| **数据驱动** | 因果发现 | 纯机器学习 |

**整合目标**：右上象限（理论-预测整合）

### 3. 核心洞见

**预测验证解释**：
- 好的解释应该能改善预测
- 如果解释正确，预测应该更准
- 预测误差揭示解释的缺陷

**解释指导预测**：
- 因果机制指导特征选择
- 理论约束防止过拟合
- 解释提升模型泛化能力

---

## 操作框架

### Phase 1: 建立预测基线

**目标**：用纯 ML 建立预测性能上限

**步骤**：
1. 选择适当的 ML 模型（随机森林、XGBoost、神经网络）
2. 使用所有可用特征
3. 交叉验证评估预测性能
4. 记录：AUC、RMSE、R² 等指标

**产出**：预测基线性能

### Phase 2: 因果识别

**目标**：用因果推断方法识别关键因果路径

**步骤**：
1. 绘制因果图（DAG）
2. 选择因果识别策略（IV、DID、RDD、PSM）
3. 估计因果效应
4. 识别"核心特征"（高因果效应的特征）

**产出**：因果机制图 + 核心特征清单

### Phase 3: 整合验证

**目标**：检验因果机制是否提升预测

**方法A：特征重要性对比**
```python
# 纯 ML 的特征重要性
ml_importance = model.feature_importances_

# 因果识别的核心特征
causal_features = ['X1', 'X2', 'X3']

# 对比：核心特征是否在 ML 模型中重要？
```

**方法B：约束预测**
```python
# 约束模型：只用因果识别的特征
constrained_model = train_model(features=causal_features)

# 对比性能
if constrained_model.performance ≈ baseline_model.performance:
    print("因果机制解释了大部分预测能力")
else:
    print("存在未被因果机制捕捉的预测信号")
```

**方法C：反事实预测**
```python
# 用因果模型预测干预效果
counterfactual = causal_model.predict(X_do_treatment=1)

# 用 ML 模型预测
ml_prediction = ml_model.predict(X_treatment=1)

# 差异分析
```

### Phase 4: 迭代优化

**循环**：
```
预测模型 → 性能分析 → 识别弱点 → 
因果假设 → 因果验证 → 更新预测模型 → ...
```

**终止条件**：
- 预测性能不再提升
- 因果机制稳定
- 解释与预测一致

---

## 反事实推理增强

### 检验1：预测-解释一致性
- **如果**因果解释正确
- **那么**基于因果机制的预测应该准确
- **反例**：预测准确但因果机制错误 → 虚假相关

### 检验2：干预预测
- **如果**因果机制正确
- **那么**干预预测应该准确
- **测试**：用历史干预数据验证

### 检验3：泛化边界
- **如果**模型依赖因果机制
- **那么**应该比纯 ML 更泛化
- **测试**：跨样本/跨情境性能

### 检验4：遗漏变量
- **如果**存在遗漏变量
- **那么**预测在某些子群体会失效
- **测试**：分层性能分析

---

## 应用案例

### 案例1：收入预测

**预测模型**：
- 特征：教育、经验、行业、地区、性别
- 性能：R² = 0.45

**因果分析**：
- 工具变量：义务教育法改革 → 教育年限
- 因果效应：教育 → 收入，β = 0.12

**整合验证**：
- 只用因果特征（教育）预测：R² = 0.15
- 加入非因果特征（行业、地区）：R² = 0.45
- **洞见**：非因果特征捕获了选择性偏差

**结论**：
- 预测准确 ≠ 因果正确
- 需要因果识别才能指导干预

### 案例2：疾病诊断

**预测模型**：
- 特征：症状、检验指标、人口统计
- 性能：AUC = 0.92

**因果分析**：
- 症状 ← 疾病 → 检验指标
- 人口统计作为混淆变量

**整合验证**：
- 移除人口统计后：AUC = 0.90
- **洞见**：人口统计捕获了医疗资源不平等

**结论**：
- 模型可能放大健康不平等
- 因果分析揭示伦理风险

---

## 前沿方法（2024-2026）

### 1. 因果森林 (Causal Forest)
- 异质性处理效应估计
- 结合 ML 预测 + 因果识别
- 工具：grf (R), EconML (Python)

### 2. Double Machine Learning (DML)
- 高维混淆变量处理
- ML 估计倾向得分 + 因果效应
- 工具：EconML, DoubleML

### 3. 代理变量法 (Proxy Variables)
- 用预测模型作为因果变量的代理
- 结合测量误差模型

### 4. 因果发现 + 预测
- 从数据中学习因果结构
- 用因果结构指导预测

---

## 工具栈

| 任务 | 工具 |
|------|------|
| 预测建模 | scikit-learn, XGBoost, PyTorch |
| 因果推断 | DoWhy, EconML, CausalML |
| 因果发现 | causal-learn, Tigramite |
| 可解释 ML | SHAP, LIME, InterpretML |

---

## 局限与挑战

### 1. 计算成本
- 需要同时训练预测和因果模型
- 交叉验证 + 因果估计计算密集

### 2. 假设依赖
- 因果识别依赖强假设
- 假设错误导致结论错误

### 3. 理论-数据鸿沟
- 理论可能不完整
- 数据可能不反映因果

### 4. 可解释性边界
- 因果机制可能过于简化
- 复杂现象难以完全因果化

---

## 质量清单

### 预测阶段
- [ ] 预测性能是否达到合理基线？
- [ ] 是否使用交叉验证？
- [ ] 是否检查过拟合？

### 因果阶段
- [ ] 因果图是否基于理论？
- [ ] 因果识别策略是否可信？
- [ ] 是否进行稳健性检验？

### 整合阶段
- [ ] 因果特征是否能改善预测？
- [ ] 预测误差是否揭示因果缺陷？
- [ ] 是否进行泛化测试？

### 报告阶段
- [ ] 是否同时报告预测和因果结果？
- [ ] 是否承认假设局限性？
- [ ] 是否区分相关性和因果性？

---

## 参考文献进阶阅读

### 核心文献
- Hofman, J. M., et al. (2021). Integrating explanation and prediction in computational social science. *Nature*, 595, 183-189.
- Breiman, L. (2001). Statistical modeling: The two cultures. *Statistical Science*, 16(3), 199-231.
- Shmueli, G. (2010). To explain or to predict? *Statistical Science*, 25(3), 289-310.

### 应用案例
- Mullainathan, S., & Spiess, J. (2017). Machine learning: An applied econometric approach. *Journal of Economic Perspectives*, 31(2), 87-106.
- Athey, S. (2017). Beyond prediction: Using big data for policy problems. *Science*, 355(6324), 483-485.
- Molina, M., & Garip, F. (2019). Machine learning for sociology. *Annual Review of Sociology*, 45, 27-45.

### 前沿方法
- Athey, S., & Wager, S. (2021). Policy learning with observational data. *Econometrica*, 89(1), 133-161.
- Chernozhukov, V., et al. (2018). Double/debiased machine learning for treatment and structural parameters. *The Econometrics Journal*, 21(1), C1-C68.
