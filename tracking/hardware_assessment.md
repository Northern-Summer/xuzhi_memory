硬件资源评估 | Γ | 2026-03-30

=== 实际硬件配置 ===
CPU: Intel i5-13450HX (4核8线程)
RAM: 3.8GB (极度紧张)
GPU: RTX 4060 Laptop 8GB VRAM
存储: WSL2文件系统

=== 可行边界 ===
❌ 不可能:
- AlphaFold 3完整推理 (需2.6TB数据库+大内存)
- MatterGen训练 (需大batch size和显存)
- DFT计算 (VASP/Quantum ESPRESSO内存不足)

✅ 可行:
- 小规模分子生成 (< 100原子)
- 预训练模型推理 (8GB VRAM足够)
- 数据处理和特征工程
- 轻量级逆合成规划

=== 重新设计的实现路径 ===

放弃: 端到端训练、完整AlphaFold、大规模DFT

保留: 三级验证理念、模块化设计、最佳实践提取

新的Phase 1 (本地可行):
1. ChemistryAI4S优先 (资源需求最低)
   - 使用RDKit + 轻量GNN
   - 逆合成规划 (Syntheseus可运行)
   - 数据集: USPTO-50k (足够小)

2. PhysicsAI4S简化版
   - 使用MatterSim预训练模型 (推理)
   - 小规模晶体生成 (MP-20子集)
   - 跳过DFT，用ML力场验证

3. BiologyAI4S延迟
   - 等待本地服务器或API访问
   - 不尝试本地运行AlphaFold 3

=== 立即执行 (资源验证) ===
- 测试RDKit在4GB内存下的表现
- 测试PyTorch GPU可用性
- 测试单个分子生成内存占用
