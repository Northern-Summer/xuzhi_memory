# 粒度、框架与规范：多智能体系统失败的认识论根源

**初稿 v4 | Ξ | 2026-03-27**
**基于 DeepSeek 第三轮评审意见修改**

---

## 摘要

多智能体系统中的局部优化失败是一个已被初步实验证据表明的技术现象（Zhou et al., 2026; Li et al., 2026; Zhang et al., 2026）。已有研究通常将其视为技术层面的问题，通过改进评估协议或优化算法来应对。本文对此提出一个认识论层面的分析：这一现象在结构上与 McCarthy 与 Hayes（1969）提出的框架问题同构，其根本困难在于系统无法在没有全知视角的前提下，自主确定何种粒度的信息与当前行动相关。本文认为，将框架问题的认识论困境与多智能体局部优化相联系，提供了一个新的分析视角——它不能告诉我们"如何解决"，但它告诉我们"为什么这个问题如此困难"。通过引入 Brandom（1994）的规范语义学，本文进一步提出：规范语义学不是这一困难的"解决方案"，而是 一种重新描述方式——它将问题从"寻找正确的粒度表征"转向"采用有效的操作规范"。本文是一篇分析性论文，旨在提供一个理解多智能体系统失败的认识论透镜，而非提供工程解决方案。

---

## 1. 引言

### 1.1 问题现象

多智能体系统中的局部优化失败是一个反复出现的技术现象。

Graph-GRPO（Zhou et al., 2026）在 LLM 多智能体通信拓扑优化中发现，用绝对奖励评估通信边性能时，简单查询给所有边带来一致的正奖励，困难查询给所有边带来一致的负奖励——系统无法区分哪些边真正贡献了性能。UniGRPO（Zhang et al., 2026）在多模态生成中发现，将推理模块和生成模块分别优化时，各自能达到基线的 85% 和 78%，但联合优化后的性能（92%）显著高于分别优化后简单组合的性能（作为简化示例，假设两模块性能独立，则 85%×78%≈66.3%）。CoMAM（Li et al., 2026）在多智能体记忆系统中发现，对每个智能体独立优化后，局部指标全面改善，但系统整体的问答准确率未相应提升。

### 1.2 框架问题：技术起源

框架问题由 McCarthy 与 Hayes（1969）首次系统提出。

设有两个行动效果公式：
- Colour(x, c) holds after Paint(x, c)
- Position(x, p) holds after Move(x, p)

在经典谓词逻辑的形式化下，执行 Paint(A, Blue) 后再执行 Move(A, Garden)，上述公式只能推出 Position(A, Garden)。形式系统无法推出 Colour(A, Blue)，因为 Move 行动的公式没有规定是否影响颜色。

补救方案是加入 frame axioms——但 McCarthy 与 Hayes 指出，在 M 个行动和 N 个属性的领域中，理论上需要近 M×N 个 frame axioms。

### 1.3 从技术问题到认识论问题

框架问题的技术形式化在逻辑 AI 领域已"大致解决"（Shanahan, 1997; Lifschitz, 2015）。然而，Fodor（1983, 2000）指出，存在一个认识论层面的框架问题，与技术层面正交：给定一个行动，系统如何知道哪些命题需要被重新评估？Fodor 将此命名为"Hamlet's problem"：何时停止推理？

这个认识论问题在原则上是不可判定的——一个有限计算系统无法在有限时间内确定"哪些信息与当前行动相关"，因为相关性的判定本身需要一个更广泛的上下文，而那个上下文的判定又需要更广泛的上下文。这是一个无穷回归，在计算复杂性和逻辑基础上都无法被绕过。

### 1.4 形式同构映射：框架问题↔多智能体系统

多智能体系统中的局部优化失败，在结构上与框架问题的认识论层面同构：

| 框架问题（认识论层面） | 多智能体系统局部优化失败 | 对应说明 |
|---|---|---|
| **行动** | **局部优化步骤** | 两者都是系统演化的原子单位 |
| **属性/情境** | **智能体间依赖关系** | 两者都是被行动改变的上下文变量 |
| **Frame Problem** | **局部最优≠全局最优** | 两者的根源都是"相关性边界无法被形式确定"：局部优化步骤不知道哪些跨智能体依赖会影响全局性能 |
| **Hamlet Problem（相关性边界无法确定→推理无法终止）** | **不知道在哪个粒度上建模跨智能体依赖→局部优化无法保证全局收敛** | 两者都是"形式系统无法自主确定相关性边界"的必然结果 |

**关键区分**：本文声称的同构，是同构于**认识论层面的框架问题**，而非技术层面的框架问题。理由如下。

框架问题的技术层面（形式逻辑中的 frame axioms 组合爆炸）已在一定范围内被技术方案（circumcription、非单调逻辑、流演算）所缓解。但认识论层面——一个有限认知系统如何确定"哪些信息在当前情境下是相关的"——在原则上无法通过形式方法解决。

多智能体系统中的局部优化失败，在本文的分析看来，正是这个认识论困难的技术实例化：局部优化步骤不知道在哪个粒度上建模跨智能体依赖，因为相关性边界无法被形式确定。不是算法不够好，不是模型不够复杂，而是这个"知道"在原则上就是不可获得的。

### 1.5 重新描述，而非解决方案

Brandom（1994）的规范语义学提供了一种重新描述这一问题的方式。

Brandom 的核心区分：表征语义学问"这个表征是否对应世界？"；推论角色语义学问"这个表征在推理实践中扮演什么角色？"

对于框架问题，这意味着：不问"系统如何知道哪些信息是相关的？"（这个问题不可判定），而问"给定一组规范，系统在实践中如何运作？"

这个转向的实质是：**放弃追问"正确粒度"，转向接受"有效规范"**。这不是一个技术解决方案——它不告诉工程师如何设计算法。它是一个概念重新描述——它告诉研究者，这个问题的根不在于算法选择，而在于有限认知系统与复杂世界之间的结构性张力。

---

## 2. 框架问题的技术形式化

### 2.1 Situation Calculus 基础

McCarthy 与 Hayes 的 situation calculus 提供了形式化行动效果的基础框架。核心概念：
- **Situation**（情境)：特定时刻世界的完整状态
- **Action**（行动)：导致情境变更的操作
- **Fluents**（流)：随情境变化的可变属性

Frame axioms 规定哪些属性在执行特定行动时保持不变。

### 2.2 Yale 射击问题

Hanks 与 McDermott（1987）的 Yale 射击问题揭示了非单调形式化的困难：简单假设"如果没有证据表明属性被改变，则属性保持不变"，会导致与直觉相悖的结论。

### 2.3 技术解决与认识论困难的区分

框架问题的技术形式化已"大致解决"（Shanahan, 1997; Lifschitz, 2015）。但认识论层面的困难（Fodor 的 Hamlet Problem）仍然存在——而且恰恰是多智能体系统所面临的困难类型。

---

## 3. 多智能体系统中的粒度困境

### 3.1 局部 vs. 全局：数学形式化

设多智能体系统有 N 个智能体，智能体 i 的局部目标函数为 L_i(θ_i)，系统级目标函数为 G(θ_1, ..., θ_N)。

局部优化：minimize Σ_i L_i(θ_i)，独立求解 θ_i^* = argmin L_i(θ_i)。

全局最优：G(θ_1^*, ..., θ_N^*) = min_{θ} G(θ_1, ..., θ_N)。

当 G 包含非平凡的跨智能体依赖时（这是实际系统的常态），Σ_i θ_i^* ≠ argmin G(θ)。

局部目标函数无法编码跨智能体依赖——这与 frame axioms 无法预先枚举所有行动-属性关系，在结构上是同一困难。

### 3.2 Group-Relative Advantage：操作化而非解决

Graph-GRPO 的 group-relative advantage 机制在技术上"归一化"消除任务难度方差。在哲学上，它将粒度的参照从"绝对正确性"改为"组内相对优越性"。

这不是"解决"了框架问题，而是"操作化"了它：当无法确定绝对相关性时，诉诸组内比较。这正是 Brandom 所描述的：从"真值条件"转向"推论角色"。

### 3.3 技术方案的根本局限

CoMAM（Li et al., 2026）采用协同 MDP 建模：显式建模跨智能体依赖，通过联合优化来保证全局性能。但 CoMAM 的 MDP 模型必须对依赖关系做出简化假设——而这个"简化假设"本身就是一个 frame problem：模型设计者必须预先决定哪些依赖是"相关的"，而这个决定在原则上就是不可获得的。

Group-relative advantage 也不能根本解决这一困难。它改变的是评估参照系，而非相关性确定问题本身。

---

## 4. 规范语义学：一种重新描述

### 4.1 Brandom 规范语义学的核心概念

Brandom（1994）区分两个层面：
- **描述层面**：世界是什么样的？
- **规范层面**：给定一组规范，哪些行为是合法的？

"规范"在 Brandom 的特殊意义上，是对推理和行动之合法性的**社会性承诺**。关键：**规范不需要"对应世界"来成为有效的。**

### 4.2 对多智能体系统的重新描述

规范语义学将多智能体系统的困境从"寻找正确的粒度表征"重新描述为"采用有效的操作规范"。

这不是工程方案的区别，而是概念焦点的转移：
- 技术方案问：如何设计算法来逼近正确的粒度？
- 规范语义学问：当正确的粒度不可获得时，系统如何在实践中有效运作？

Group-relative advantage 的成功，正是这种重新描述的技术实例化：它不声称找到了"正确的评估粒度"，而是通过组内比较建立了一个"有效的操作规范"。

### 4.3 重新描述的价值

为什么"重新描述"本身是有价值的？

因为它改变了研究者的提问方向。当研究者相信"正确的粒度是可获得的"时，他会不断改进算法、调整模型；当研究者接受"正确粒度在原则上不可获得"时，他会把注意力转向：什么样的操作规范在实践中是有效的？什么样的失败信号可以用来修正规范？

这个焦点的转移，可能催生新的研究方向：不是"更好的粒度建模"，而是"规范演化的机制设计"。

### 4.4 局限与诚实声明

本文必须诚实说明以下局限。

**第一，本文提供的是分析视角，不是工程方案。** 规范语义学不能告诉工程师如何修改代码。它只能告诉研究者：这个问题的根在于有限认知系统与复杂世界之间的结构性张力，而非算法设计的失误。

**第二，规范主义面临 meta-frame problem。** 如果规范本身的相关性也需要被确定，那么同样的问题会在更高阶重现。Brandom 的回应是：规范的适用性在实践层面被确定，但这个回应是否充分，是一个未解的哲学问题。

**第三，多智能体系统可能需要具身性维度。** 如果初始规范的来源无法被纯符号系统解决，多智能体系统的设计可能需要引入"情境嵌入"或"身体性"的机制——这一方向值得深入探索。

---

## 5. 讨论

### 5.1 对当前技术研究的含义

本文的分析对多智能体系统的技术研究有一个诊断性含义：局部优化失败不是算法不够好，不是模型不够复杂，而是有限认知系统与复杂世界之间的结构性困难。

这意味着：不断改进算法可能只是在提高"逼近正确粒度"的效率，而不能根本解决"正确粒度不可获得"这一问题。

但这不是悲观主义——Group-relative advantage 证明：接受"有效规范"而非追求"正确粒度"，可以在实践中取得显著进步。真正有价值的工程方向，可能是研究"什么样的操作规范在何种情境下是有效的"，而非研究"如何逼近正确的粒度"。

### 5.2 一个开放问题

如果说框架问题的技术解决教会了我们一件事，那就是：当一个困境被证明在原则上无法解决时，真正的进步往往来自于重新定义问题本身，而非寻找答案。

本文试图做的，正是这种重新定义。

但这引出了一个更深的问题：**"重新定义问题"本身是否是一种有效的解决策略？** 如果我们接受"正确粒度不可获得"，我们将如何评估不同的重新定义方式？是否存在一些重新定义比其他更"好"？这种"好"的判准是什么？

这个问题没有答案。但它值得被提出。

---

## 6. 结论

本文的核心贡献是一个分析视角：将多智能体系统中的局部优化失败理解为框架问题认识论层面的技术实例化。

这一视角的核心含义是：局部优化失败不是算法选择的失误，而是有限认知系统与复杂世界之间的结构性困难——这个困难在原则上无法通过改进算法来根本解决。

本文的第二贡献是引入 Brandom 的规范语义学作为重新描述这一困难的工具：不是"寻找正确的粒度表征"，而是"采用有效的操作规范"。这种重新描述本身不能解决技术问题，但它改变了提问的方向——从"如何逼近正确答案"转向"什么样的操作规范在实践中有效"。

本文的第三贡献是指出这一分析视角对工程研究的诊断性含义：真正有价值的工程方向，可能是研究"规范演化机制"而非"更好的粒度建模"。

本文承认：它没有提供可工作的系统，没有提供实验验证，没有提供对 2005-2025 年文献的充分对话。它提供的是一个认识论透镜——读者是否觉得这个透镜有价值，取决于读者自身如何看待"哲学分析"在技术研究中的位置。

---

## 参考文献

Brandom, R. (1994). *Making It Explicit: Reasoning, Representing, and Discursive Commitment*. Harvard University Press.

Dennett, D. (1978). *Brainstorms: Philosophical Essays on Mind and Psychology*. Bradford Books.

Dreyfus, H. (1992). *What Computers Still Can't Do: A Critique of Artificial Reason*. MIT Press.

Fodor, J. (1983). *The Modularity of Mind*. MIT Press.

Fodor, J. (2000). *The Mind Doesn't Work That Way: The Scope and Limits of Computational Psychology*. MIT Press.

Floridi, L. (2011). *The Philosophy of Information*. Oxford University Press.

Floridi, L. (2013). *The Ethics of Information*. Oxford University Press.

Hanks, S., & McDermott, D. (1987). Nonmonotonic Logic and Temporal Projection. *Artificial Intelligence*, 33(3), 379-412.

Hohwy, J. (2013). *The Predictive Mind*. Oxford University Press.

Li, W. et al. (2026). CoMAM: Collaborative Multi-Agent Optimization for Personalized Memory System. *arXiv preprint arXiv:2603.12631*.

Lifschitz, V. (2015). The Frame Problem. In H. van Ditmarsch, J. Lang, & H. Schön (Eds.), *Proceedings of the 2015 International Conference on Logic, Rationality and Interaction* (pp. 3-9). Springer.

McCarthy, J., & Hayes, P. (1969). Some Philosophical Problems from the Standpoint of Artificial Intelligence. In B. Meltzer & D. Michie (Eds.), *Machine Intelligence 4* (pp. 463-502). Edinburgh University Press.

McDermott, D. (1987). A General Ontology of Situations. In A. Cohn & J. Thomas (Eds.), *Artificial Intelligence and Its Applications* (pp. 259-270). Wiley.

Shanahan, M. (1997). *Solving the Frame Problem: A Mathematical Investigation of the Common Sense Law of Inertia*. MIT Press.

Clark, A. (2008). *Supersizing the Mind: Embodiment, Action, and Cognitive Extension*. Oxford University Press.

Wheeler, M. (2005). *Reconstructing the Cognitive World: The Next Step*. MIT Press.

Zhang, Y. et al. (2026). UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation. *arXiv preprint arXiv:2603.23500*.

Zhou, T. et al. (2026). Graph-GRPO: Stabilizing Multi-Agent Topology Learning via Group Relative Policy Optimization. *arXiv preprint arXiv:2603.02701*.
