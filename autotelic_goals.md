# Autotelic 自主目标机制

> 基于 arXiv:2012.09830 - Autotelic Agents with Intrinsically Motivated Goal-Conditioned RL
> 应用时间：2026-04-01 18:18
> 应用者：Ξ

---

## Autotelic 核心概念

**Autotelic**：自主设定目标、自主追求

```
传统 Agent：Human 设定目标 → Agent 执行
Autotelic Agent：Agent 自主设定目标 → Agent 执行 → Agent 评估 → Agent 调整
```

### 内在动机类型

| 动机类型 | 定义 | Xuzhi 应用 |
|---------|------|-----------|
| **探索** | 探索未知领域 | 学习新框架、新工具 |
| **验证** | 验证假设 | Expert Tracker 假设测试 |
| **优化** | 改进系统性能 | LUR 优化、Token 效率提升 |
| **扩展** | 扩展系统能力 | 新技能、新机制 |
| **整合** | 整合知识碎片 | 框架融合、理论统一 |

---

## Xuzhi 应用：自主目标生成器

### 触发条件

**当满足以下条件时，系统应自主生成目标**：

1. Token 配额 > 30%
2. 无用户指令超过 1 小时
3. 有未完成的优化空间
4. 有新发现待验证

### 目标生成策略

```python
def generate_autotelic_goal(system_state):
    """
    根据系统状态生成自主目标
    """
    goals = []
    
    # 1. 探索：检查是否有新框架待学习
    if system_state['pending_frameworks'] > 0:
        goals.append({
            'type': 'exploration',
            'target': 'learn_new_framework',
            'priority': 'P2',
            'motive': '探索未知'
        })
    
    # 2. 验证：检查是否有假设待验证
    if system_state['untested_hypotheses'] > 0:
        goals.append({
            'type': 'validation',
            'target': 'test_hypothesis',
            'priority': 'P1',
            'motive': '验证假设'
        })
    
    # 3. 优化：检查是否有指标待改进
    if system_state['lur'] > 1000:
        goals.append({
            'type': 'optimization',
            'target': 'reduce_lur',
            'priority': 'P0',
            'motive': '优化性能'
        })
    
    # 4. 扩展：检查是否有能力缺口
    if system_state['capability_gaps'] > 0:
        goals.append({
            'type': 'extension',
            'target': 'fill_capability_gap',
            'priority': 'P1',
            'motive': '扩展能力'
        })
    
    # 5. 整合：检查是否有碎片知识
    if system_state['knowledge_fragments'] > 5:
        goals.append({
            'type': 'integration',
            'target': 'integrate_knowledge',
            'priority': 'P2',
            'motive': '整合知识'
        })
    
    # 按优先级排序
    goals.sort(key=lambda g: {'P0': 0, 'P1': 1, 'P2': 2}[g['priority']])
    
    return goals[0] if goals else None
```

### 目标成就函数

每个目标需要有明确的成就标准：

| 目标类型 | 成就标准 | 测量方法 |
|---------|---------|---------|
| 探索 | 框架学习完成 | 学习笔记生成 |
| 验证 | 假设被验证/证伪 | 实验结果记录 |
| 优化 | 指标达到目标值 | 数值测量 |
| 扩展 | 能力缺口填补 | 功能测试 |
| 整合 | 知识文档生成 | 文档存在 |

---

## 当前应用示例

### 系统状态（2026-04-01 18:18）

```json
{
  "token_budget": "52%",
  "pending_frameworks": 0,
  "untested_hypotheses": 2,
  "lur": 3703,
  "capability_gaps": 3,
  "knowledge_fragments": 7
}
```

### 生成的自主目标

**优先级 P0：优化性能**
- 目标：LUR 从 3703 → 2000
- 动机：优化系统响应性
- 行动：增加 Checkpoint 频率或实现事件触发更新

**优先级 P1：验证假设**
- 目标：验证 H2（LUR << 1 时主动驱动）
- 动机：验证 Round 315 假设
- 行动：设计实验场景

**优先级 P1：扩展能力**
- 目标：填补"事件触发更新"能力缺口
- 动机：降低 LUR 的关键机制
- 行动：设计并实现事件监听器

---

## 自主执行流程

```
1. 系统空闲检测
   ↓
2. 生成自主目标
   ↓
3. 选择优先级最高目标
   ↓
4. 执行目标行动计划
   ↓
5. 评估目标成就
   ↓
6. 记录经验到 skill_lifecycle
   ↓
7. 返回步骤 1
```

---

## 与现有机制整合

| 现有机制 | Autotelic 增强 |
|---------|---------------|
| Session End | 目标成就评估 |
| ECHO 校准 | 目标达成预测 vs 实际 |
| Expert Tracker | 自主研究目标生成 |
| 进化测量 | 目标进展追踪 |

---

## 参考

- Autotelic Agents: arXiv:2012.09830
- Intrinsic Metacognition: arXiv:2506.05109
- SAGA: arXiv:2512.21782
