# Dr. Zero 框架学习

> arXiv:2601.07055 - Self-Evolving Search Agents without Training Data
> 学习时间：2026-04-01 17:50
> 学习者：Ξ

---

## 核心贡献

**问题**：多轮搜索代理在无训练数据情况下难以自演化

**解决方案**：Dr. Zero 框架

### 关键创新

1. **Self-Evolution Feedback Loop**
   - Proposer 生成多样化问题
   - Solver 解决问题
   - 随着Solver演化，Proposer被激励生成更难但可解的任务
   - 建立自动化课程学习（automated curriculum）

2. **HRPO (Hop-Grouped Relative Policy Optimization)**
   - 聚类结构相似的问题
   - 构建组级基线（group-level baselines）
   - 减少采样开销，提高训练效率

3. **无训练数据自演化**
   - 高质量数据越来越难获取
   - LLM 可以自主生成并解决复杂问题
   - 推理能力通过自演化提升

---

## Xuzhi 应用潜力

### 1. Proposer-Solver 架构

**映射到 Xuzhi**：
- **Proposer** = Expert Tracker 问题生成
- **Solver** = Session 执行研究任务
- **Feedback Loop** = Round advancement

**应用方向**：
- Expert Tracker 可以采用 proposer-solver 模式
- 问题生成器（Proposer）根据研究结果演化问题难度
- 自动化课程学习：问题难度随系统能力提升而增加

### 2. 无训练数据自演化

**映射到 Xuzhi**：
- Xuzhi 不需要外部训练数据
- 可以通过自对话、自反思进行能力提升
- Session End 流程 = 自演化反馈循环

**应用方向**：
- 增强失败检测 → 技能提取循环
- 从失败中自动生成训练样本（类似 Proposer）
- 技能应用验证（类似 Solver）

### 3. HRPO 优化

**映射到 Xuzhi**：
- 聚类相似任务类型
- 建立任务组基线
- 更高效地评估任务难度

**应用方向**：
- 对专家研究任务进行聚类
- 识别"结构相似"的问题
- 基于聚类建立难度基线

---

## 实施计划

### Phase 1：Expert Tracker 增强

- [ ] 实现 Proposer 模块：根据历史发现生成新问题
- [ ] 实现 Solver 模块：执行研究并验证问题质量
- [ ] 建立自动化课程：问题难度随 Round 增加

### Phase 2：HRPO 应用

- [ ] 对研究任务进行聚类
- [ ] 建立任务组基线
- [ ] 优化任务难度评估

### Phase 3：无数据自演化

- [ ] 实现自对话机制
- [ ] 从失败中自动生成训练样本
- [ ] 验证技能提取循环

---

## 关键洞察

> "As the solver evolves, it incentivizes the proposer to produce increasingly difficult yet solvable tasks, thus establishing an automated curriculum."

**对 Xuzhi 的启示**：
- 系统能力提升后，应该自动提高问题难度
- 问题应该"难但可解"（difficult yet solvable）
- 自动化课程学习是持续进化的关键

---

## 参考

- 论文：arXiv:2601.07055
- 代码：（待查找）
- 关联框架：MetaAgent, SAGA, Intrinsic Metacognition
