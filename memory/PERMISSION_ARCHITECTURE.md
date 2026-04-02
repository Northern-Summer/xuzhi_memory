# 权限隔离架构

## 问题

- chmod 444：防止写入，但所有者可以删除
- chattr +i：完全不可变，自己也不能修改
- 所有 Agent 以同一用户运行，无法用文件权限区分

## 当前方案：信任 + Git 追踪

1. chmod 444 防止意外写入
2. Git 追踪所有修改
3. VERSION_LOCK.json 验证完整性
4. checksum_baseline.txt 检测篡改

## Agent 行为约束

- ❌ Agent 不应该修改其他 Agent 的 MEMORY.md
- ✅ Agent 可以修改自己的 MEMORY.md（进化需要）
- ✅ Agent 可以向其他 Agent 的 session 发送消息（轮值需要）

## 未来方案：不同用户身份

如果要彻底解决，需要：
- 创建用户：agent_phi, agent_delta, ...
- 每个 Agent 以自己的用户身份运行
- 天然权限隔离

## 权限边界

```
用户 → Agent
  ✅ 可以联系任何 Agent
  ✅ 可以修改任何 Agent 的 MEMORY.md（chmod 后）

Agent → Agent
  ✅ 可以向其他 Agent 的 session 发送消息（轮值需要）
  ❌ 不应该修改其他 Agent 的 MEMORY.md（行为约束）
  ✅ 可以修改自己的 MEMORY.md（进化需要）

L1 vs L2
  L1 共享：所有 Agent 可读写
  L2 私有：只有 Agent 自己管理
```
