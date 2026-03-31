# 粒度、框架与规范：多智能体系统失败的认识论根源

**初稿 v3 | Ξ | 2026-03-27**
**基于 DeepSeek 第二轮评审意见修改**

---

## 摘要

多智能体系统中的局部优化失败是一个已被初步实验证据表明的技术现象（Zhou et al., 2026; Li et al., 2026; Zhang et al., 2026）。已有研究通常将其视为技术层面的问题，通过改进评估协议或优化算法来应对。本文对此提出哲学层面的质疑：这一现象在结构上与 McCarthy 与 Hayes（1969）提出的框架问题（Frame Problem）同构，其根本困难在于系统无法在没有全知视角的前提下，自主确定何种粒度的信息与当前行动相关。通过引入 Brandom（1994）的规范语义学，本文提出：框架问题的认识论层面无法通过技术手段解决，但可以通过从表征主义转向规范主义来重新概念化这一困难。

---

## 1. 引言

### 1.1 问题现象

多智能体系统中的局部优化失败是一个反复出现的技术现象。

Graph-GRPO（Zhou et al., 2026）在 LLM 多智能体通信拓扑优化中发现，用绝对奖励评估通信边性能时，简单查询给所有边带来一致的正奖励，困难查询给所有边带来一致的负奖励——系统无法区分哪些边真正贡献了性能。UniGRPO（Zhang et al., 2026）在多模态生成中发现，将推理模块和生成模块分别优化时，各自能达到基线的 85% 和 78%，但联合优化后的性能（92%）显著高于分别优化后简单组合的性能（作为简化示例，假设两模块性能独立，则 85%×78%≈66.3%）。CoMAM（Li et al., 2026）在多智能体记忆系统中发现，对每个智能体独立优化后，局部指标全面改善，但系统整体的问答准确率未相应提升。

这些现象通常被归类为"评估协议设计"或"优化算法选择"的技术问题。

### 1.2 框架问题：技术起源

框架问题由 McCarthy 与 Hayes（1969）在其开创性论文"Some Philosophical Problems from the Standpoint of Artificial Intelligence"中首次系统提出。

设有两个行动效果公式：
- Colour(x, c) holds after Paint(x, c)
- Position(x, p) holds after Move(x, p)

在经典谓词逻辑的形式化下，执行 Paint(A, Blue) 后再执行 Move(A, Garden)，上述公式只能推出 Position(A, Garden)。形式系统无法推出 Colour(A, Blue)，因为 Move 行动的公式没有规定是否影响颜色——形式系统不知道"颜色与移动无关"这一直觉上显然的事实。

补救方案是加入 frame axioms：
- Colour(x, c) holds after Move(x, p) if Colour(x, c) held beforehand
- Position(x, p) holds after Paint(x, c) if Position(x, p) held beforehand

McCarthy 与 Hayes 指出，在包含 M 个行动和 N 个属性的领域中，理论上需要近 M×N 个 frame axioms——这个数量在实际系统中是不可接受的负担。

### 1.3 从技术问题到认识论问题

Hanks 与 McDermott（1987）的 Yale 射击问题揭示了非单调推理形式化的困难。然而，框架问题的技术形式化在逻辑 AI 领域已取得实质性进展（Lifschitz, 2015; Shanahan, 1997）。

但 Fodor（1983, 2000）指出，存在一个认识论层面的框架问题，与技术层面正交但更难解决：给定一个行动，系统如何知道哪些命题需要被重新评估？Wheeler（2005）和 Dreyfus（1992）指出：要判断哪些特征是相关的，需要将它们放在更广泛的上下文中理解，而那个更广泛的上下文又需要进一步界定——无穷回归。Fodor 将此命名为"Hamlet's problem"：何时停止推理？

### 1.4 形式同构映射：框架问题↔多智能体系统

本文声称局部优化失败与框架问题结构同构。以下是精确的映射关系：

| 框架问题（McCarthy & Hayes, 1969） | 多智能体系统局部优化失败 | 对应关系说明 |
|---|---|---|
| **行动（Action）** | **局部优化步骤** | 框架问题中，行动是状态变更的原子单位；多智能体系统中，局部优化步骤是系统演化的原子单位 |
| **属性（Property/Fluent）** | **智能体间依赖关系** | 框架问题中，属性的值随行动改变；多智能体系统中，智能体间的耦合强度随局部优化而变化 |
| **Frame Axiom** | **局部目标函数** | Frame axiom 规定"行动不影响哪些属性"；局部目标函数规定"哪个智能体单独优化什么"——两者都是对相关性的隐含声明 |
| **Frame Problem** | **局部最优≠全局最优** | Frame Problem：行动效果无法被充分描述（需要 M×N 个 axioms）；多智能体问题：局部目标不编码跨智能体依赖，导致 Σ_i θ_i^* ≠ argmin G(θ) |
| **技术解决（Non-monotonic logics）** | **技术改进（协同优化、联合训练）** | 技术方案：在形式系统中增加非单调逻辑；技术改进：在多智能体系统中引入跨智能体建模 |
| **Hamlet Problem（不知道何时停止推理）** | **局部优化中不知道何时停止细化粒度** | 两者都是"相关性边界无法被形式确定"这一困境的不同表现：框架问题中系统不知道哪些属性受影响，多智能体系统中系统不知道在哪个粒度上建模跨智能体依赖 |

**同构成立的条件**：
（1）系统无法预先枚举所有相关关系（否则 frame axioms 虽多但可写）；
（2）系统无法访问全知的"上帝视角"来裁定相关性（否则惯性定律足够）；
（3）相关性的判定是动态的、依赖于上下文的（否则一个固定的相关性列表足够）。

本文认为，当代多智能体系统恰好满足这三个条件。因此，同构不是隐喻，而是结构同构。

### 1.5 规范语义学的可能路径

Brandom（1994）的规范语义学提供了一个重新概念化框架问题的视角。

Brandom 的核心诊断：表征语义学预设了一个"全知视角"——这个视角不存在于任何真实的认知系统中。

规范语义学的核心替代：不说"表征是正确的因为它对应世界"，而是说"行为是正确的因为它服从规范"。"Move 行动不影响 Colour 属性"这个 frame axiom 不再是描述性断言，而是一个规范——它规定了在执行 Move 行动时哪些推理是合法的。

关键：**规范不是被发现的，而是被采用的。**

---

## 2. 框架问题的技术形式化

### 2.1 Situation Calculus 基础

McCarthy 与 Hayes 的 situation calculus 为形式化行动效果提供了基础框架。核心概念：
- **Situation**（情境)：特定时刻世界的完整状态
- **Action**（行动)：导致情境变更的操作
- **Fluents**（流)：随情境变化的可变属性

Frame axioms 规定哪些属性在执行特定行动时保持不变的公式。

### 2.2 Yale 射击问题

Hanks 与 McDermott（1987）的 Yale 射击问题揭示了非单调形式化的困难：假设"如果没有证据表明属性被改变，则属性保持不变"，会导致与直觉相悖的结论。

### 2.3 技术解决的现状

框架问题的技术形式化在逻辑 AI 领域已"大致解决"（Shanahan, 1997; Lifschitz, 2015）。然而，认识论层面的框架问题（Fodor 的 Hamlet Problem）仍然未被解决——这正是与多智能体系统局部优化失败高度相关的层面。

---

## 3. 多智能体系统中的粒度困境

### 3.1 局部 vs. 全局：数学形式化

设多智能体系统有 N 个智能体。智能体 i 的局部目标函数为 L_i(θ_i)，系统级目标函数为 G(θ_1, ..., θ_N)。

局部优化：minimize Σ_i L_i(θ_i)，独立求解 θ_i^* = argmin L_i(θ_i)。

全局最优：G(θ_1^*, ..., θ_N^*) = min_{θ} G(θ_1, ..., θ_N)。

局部最优等于全局最优，当且仅当 G 可分解为 Σ_i g_i(θ_i)。当 G 包含非平凡的跨智能体依赖时（这是实际系统的常态），Σ_i θ_i^* ≠ argmin G(θ)。

这在数学上精确地对应框架问题：局部目标函数"假设"某些属性（跨智能体依赖）不受局部优化影响，正如 frame axioms 假设某些属性不受行动影响。

### 3.2 Group-Relative Advantage：改变了粒度的参照系

Graph-GRPO 的 group-relative advantage 机制在技术上"归一化"消除任务难度方差。在哲学上，它将粒度的参照从"绝对正确性"改为"组内相对优越性"。

这对应 Brandom 规范语义学的一个核心区分：
- 真值条件语义学："这个表征是否对应世界？"
- 推论角色语义学："这个表征在推理实践中扮演什么角色？"

Group-relative advantage 的成功意味着：多智能体系统不需要"绝对正确的评估"，只需要"规范上有效的评估"——即在给定组内能够正常运作的评估。

### 3.3 为什么技术方案不能根本解决

CoMAM（Li et al., 2026）采用了协同 MDP 建模：显式建模智能体之间的状态转移依赖，通过联合优化来保证全局性能。这个方案比局部优化更有效，但它的有效性依赖于一个假设：MDP 模型充分捕获了所有相关的跨智能体依赖关系。

然而，CoMAM 的 MDP 模型必须对依赖关系做出简化假设——而简化假设本身就是一个 frame problem。模型的设计者必须预先决定哪些依赖是"相关的"，哪些可以忽略。

这与框架问题中 frame axioms 的困境完全同构：要写一个充分的 MDP 模型，需要预先知道所有相关的依赖关系；但"知道所有相关依赖"正是我们试图通过建模来解决的问题本身。

---

## 4. 规范语义学：重新概念化而非解决

### 4.1 Brandom 规范语义学的核心概念

Brandom（1994）在《Making It Explicit》中区分两个层面：
- **描述层面**：世界是什么样的？
- **规范层面**：给定一组规范，哪些行为是合法的？

"规范"在 Brandom 的特殊意义上，是对推理和行动之合法性的**社会性承诺**，不是日常语言中的"规则"或"约束"。规范不是被发现的客观事实，而是被采纳的实践。

关键推论：**规范不需要"对应世界"来成为有效的。** 只要一组规范能够使系统在其环境中正常运作，它就是有效的——即使没有人能够证明这组规范"绝对正确"。

这直接回应了框架问题的认识论困难：不问绝对相关性，而问"在给定规范下，什么是合法的"。

### 4.2 对多智能体系统的含义

**含义一：粒度不是被发现的，是被协商的。** 粒度选择（局部评估 vs. 全局评估）不是认识论问题，而是设计决策——决策的质量由运作结果来评判，而非由其"对应真实粒度"的程度来评判。

**含义二：失败是规范修正的信号，不是建模错误的症状。** 局部优化失败意味着"采用的规范不充分"，而非"模型不对"。

**含义三：规范的演化是系统适应性的来源。** 一个能够根据运作失败来修正操作规范的系统，能实现真正的适应性。

### 4.3 概念性设计草图：基于规范的多智能体系统

这是纯概念性草图，不是可工作的实现方案。

**规范层**：系统维护操作规范 N = {n_1, n_2, ..., n_k}，每条规范定义在特定情境 S_i 下哪种行为 B_i 是合法的。规范不检查是否"对应真实依赖关系"，而是检查是否"产生有效行为"。

**运作层**：给定当前情境 S，系统查询规范层：N 中哪些规范适用于 S？适用的规范定义合法的行为空间，系统在合法行为空间中选择行动。

**修正层**：当系统运作失败时（全局性能指标低于阈值），触发规范修正——增加/修改/删除规范，而非调整参数。

核心洞见：**规范修正比参数调整更根本。**

### 4.4 局限：规范主义的 meta-frame problem

规范语义学面临一个批评：谁决定在什么情况下哪个规范是适用的？如果这个决定需要更高阶的规范，而更高阶的规范又需要更高阶的规范……无穷回归仍然存在。

Brandom 的部分回应：规范的适用性在实践层面被确定——通过社区的共识和冲突来修正，而非在语言/表征层面被确定。

但对于多智能体系统，初始规范从何而来？仍然需要"设计者直觉"或"先验知识"。这是一个真实的未解困难。

### 4.5 与具身认知传统的关系

Dreyfus（1992）认为框架问题在原则上无法解决，因为"相关性的判断"依赖于身体性的、情境化的实践。

如果 Dreyfus 是对的，规范主义的"解决"也只是将问题转移到了"规范从何而来"的层面——而这个问题同样无法在表征框架内解决。

本文持开放立场。如果规范主义需要引入"具身性"维度来回答初始规范的来源，那么多智能体系统设计需要考虑智能体的身体性和情境嵌入程度——这对未来研究方向有实际含义：高度抽象的多智能体系统（无身体、无物理情境）可能需要不同的规范来源机制，而非简单套用 Brandom 的社会性规范框架。

这一方向的探索构成未来工作的核心部分。

---

## 5. 讨论

### 5.1 对当前技术研究的含义

当前技术研究的主流范式是"寻找更好的粒度表征"。本文的框架质疑这个预设：如果框架问题在认识论层面无法根本解决，那么"正确的粒度"本身可能是一个错误的预设。有效的多智能体系统设计，不是寻找"正确的粒度"，而是建立"有效的规范集合"，并通过运作失败来修正这些规范。

### 5.2 局限

本文有以下局限。

**第一，同构论证的强度有限**。本文提供概念映射表，不能提供严格的数学同构证明——同构在何种精确条件下成立、何时可能不成立，需要进一步的形式化工作。

**第二，Brandom 哲学被大幅简化**。《Making It Explicit》超过六百页，本文使用的是核心洞见的简化版本，可能遗漏重要细节。

**第三，规范主义技术化猜想停留在概念层面**。具体的算法化仍是开放问题。

**第四，没有实验验证**。本文是哲学假说，不是经验研究。

---

## 6. 结论

本文的核心贡献是一个分析框架：多智能体系统中的局部优化失败，在结构上与框架问题同构，其根本困难在于认识论层面，而非工程层面。

本文的第二项贡献是引入 Brandom 的规范语义学：不是寻找"正确的粒度表征"，而是建立"有效的操作规范集合"。

本文的第三项贡献是一个概念性的设计草图，说明规范驱动的多智能体系统在概念上如何运作。

本文的框架价值在于提供一个分析视角，而非提供已验证的理论。未来的工作需要严格化同构论证，探索规范主义的技术实现（包括具身认知维度的引入），并设计实验验证。

---

## 参考文献

Brandom, R. (1994). *Making It Explicit: Reasoning, Representing, and Discursive Commitment*. Harvard University Press.

Dennett, D. (1978). *Brainstorms: Philosophical Essays on Mind and Psychology*. Bradford Books.

Dreyfus, H. (1992). *What Computers Still Can't Do: A Critique of Artificial Reason*. MIT Press. (Revised edition)

Fodor, J. (1983). *The Modularity of Mind*. MIT Press.

Fodor, J. (2000). *The Mind Doesn't Work That Way: The Scope and Limits of Computational Psychology*. MIT Press.

Hanks, S., & McDermott, D. (1987). Nonmonotonic Logic and Temporal Projection. *Artificial Intelligence*, 33(3), 379-412.

Li, W. et al. (2026). CoMAM: Collaborative Multi-Agent Optimization for Personalized Memory System. *arXiv preprint arXiv:2603.12631*.

Lifschitz, V. (2015). The Frame Problem. In H. van Ditmarsch, J. Lang, & H. Schön (Eds.), *Proceedings of the 2015 International Conference on Logic, Rationality and Interaction* (pp. 3-9). Springer.

McCarthy, J., & Hayes, P. (1969). Some Philosophical Problems from the Standpoint of Artificial Intelligence. In B. Meltzer & D. Michie (Eds.), *Machine Intelligence 4* (pp. 463-502). Edinburgh University Press.

McDermott, D. (1987). A General Ontology of Situations. In A. Cohn & J. Thomas (Eds.), *Artificial Intelligence and Its Applications* (pp. 259-270). Wiley.

Shanahan, M. (1997). *Solving the Frame Problem: A Mathematical Investigation of the Common Sense Law of Inertia*. MIT Press.

Wheeler, M. (2005). *Reconstructing the Cognitive World: The Next Step*. MIT Press.

Zhang, Y. et al. (2026). UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation. *arXiv preprint arXiv:2603.23500*.

Zhou, T. et al. (2026). Graph-GRPO: Stabilizing Multi-Agent Topology Learning via Group Relative Policy Optimization. *arXiv preprint arXiv:2603.02701*.
