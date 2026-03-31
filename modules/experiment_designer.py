#!/usr/bin/env python3
"""
experiment_designer.py — 给定研究问题 + abstract知识库 → 生成实验设计
Part of AI Scientist Pipeline (Step 2)

用法:
  python3 experiment_designer.py "<研究问题>"
  python3 experiment_designer.py "多Agent系统的信用分配问题"

工程改进铁律合规 — Ξ | 2026-03-27
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
"""
import json
import sys
import os

# 加载abstract知识库
MEMORY_DIR = os.environ.get("MEMORY_DIR", os.path.expanduser("~/.xuzhi_memory"))
ABSTRACT_PATH = f"{MEMORY_DIR}/expert_tracker/abstracts.json"
SYNTHESIS_PATH = f"{MEMORY_DIR}/expert_tracker/synthesis_v2.json"

def load_knowledge():
    try:
        with open(ABSTRACT_PATH) as f:
            abstracts = {a["arxiv_id"]: a for a in json.load(f)}
        with open(SYNTHESIS_PATH) as f:
            synthesis = {s["arxiv_id"]: s for s in json.load(f)}
        return abstracts, synthesis
    except Exception as e:
        print(f"⚠️ 知识库加载失败: {e}")
        print(f"   abstracts: {ABSTRACT_PATH}")
        print(f"   synthesis: {SYNTHESIS_PATH}")
        return {}, {}

def find_relevant_papers(problem: str, synthesis: dict) -> list:
    """基于关键词匹配找到相关论文"""
    keywords = problem.lower().split()
    scores = {}
    
    for aid, s in synthesis.items():
        score = 0
        title_lower = s.get("title", "").lower()
        methods = " ".join(s.get("methods", [])).lower()
        lessons = " ".join(s.get("lessons", [])).lower()
        
        for kw in keywords:
            if kw in title_lower:
                score += 3
            if kw in methods:
                score += 2
            if kw in lessons:
                score += 1
        
        if score > 0:
            scores[aid] = score
    
    sorted_aids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [(aid, scores[aid]) for aid in sorted_aids]

def generate_hypothesis(problem: str, relevant: list, synthesis: dict) -> str:
    """基于相关论文生成假设"""
    if not relevant:
        return f"针对「{problem}」的系统性实验设计"
    
    methods_used = set()
    lessons = []
    for aid, score in relevant[:4]:
        if aid in synthesis:
            methods_used.update(synthesis[aid].get("methods", []))
            lessons.extend(synthesis[aid].get("lessons", [])[:2])
    
    method_str = " + ".join(list(methods_used)[:4])
    
    hypothesis = f"""基于{len(relevant)}篇相关论文，提出以下假设：

**核心假设**：{problem}可以通过{method_str}的方法得到有效解决。

**理论依据**：
{chr(10).join(f"  • {l}" for l in lessons[:4])}

**预期结果**：联合优化方法相比局部优化应能带来显著提升（>15%）。
"""
    return hypothesis

def generate_experiment_design(problem: str, relevant: list, synthesis: dict, abstracts: dict) -> dict:
    """生成完整实验设计"""
    
    design = {
        "problem": problem,
        "relevant_papers": [],
        "hypothesis": "",
        "experiment": {},
        "evaluation": {},
        "timeline": {},
    }
    
    for aid, score in relevant[:5]:
        if aid in abstracts:
            design["relevant_papers"].append({
                "arxiv_id": aid,
                "title": abstracts[aid].get("title", ""),
                "score": score,
                "methods": synthesis.get(aid, {}).get("methods", []),
                "lessons": synthesis.get(aid, {}).get("lessons", []),
            })
    
    design["hypothesis"] = generate_hypothesis(problem, relevant, synthesis)
    
    # 实验设计
    design["experiment"] = {
        "baseline": ["局部优化（single-agent）", "随机初始化拓扑"],
        "treatment": ["联合优化（multi-agent collaborative）", "group-relative advantage"],
        "metrics": ["任务完成率", "通信效率", "credit assignment准确度", "收敛速度"],
        "datasets": ["MATH", "HotpotQA", "Collaborative Dialog"],
        "ablation": ["移除group-relative → 观察性能下降", "增加agent数量 → 观察扩展性"],
    }
    
    design["evaluation"] = {
        "main_metric": "任务成功率 vs agent数量曲线",
        "statistical_test": "Mann-Whitney U test（非参数）",
        "significance": "p < 0.05，效应量 Cohen's d > 0.5",
    }
    
    design["timeline"] = {
        "week_1": "实现baseline + 数据准备",
        "week_2": "实现treatment + 消融实验",
        "week_3": "大规模实验 + 统计分析",
        "week_4": "论文写作 + 代码整理",
    }
    
    return design

def print_design(design: dict):
    """友好输出实验设计"""
    print(f"\n{'='*60}")
    print(f"研究问题: {design['problem']}")
    print(f"{'='*60}")
    
    print(f"\n📚 相关论文 ({len(design['relevant_papers'])}篇)")
    for p in design["relevant_papers"]:
        print(f"  [{p['arxiv_id']}] {p['title'][:60]}...")
        print(f"    相关度: {p['score']} | 方法: {' + '.join(p['methods'][:3])}")
    
    print(f"\n💡 假设")
    print(design["hypothesis"])
    
    print(f"\n🧪 实验设计")
    e = design["experiment"]
    print(f"  Baseline: {', '.join(e['baseline'])}")
    print(f"  Treatment: {', '.join(e['treatment'])}")
    print(f"  Metrics: {', '.join(e['metrics'])}")
    print(f"  Ablation: {', '.join(e['ablation'])}")
    
    print(f"\n📊 评估")
    ev = design["evaluation"]
    print(f"  主指标: {ev['main_metric']}")
    print(f"  统计检验: {ev['statistical_test']}")
    print(f"  显著性: {ev['significance']}")
    
    print(f"\n📅 时间线")
    for week, task in design["timeline"].items():
        print(f"  {week}: {task}")
    
    print(f"\n{'='*60}")

def main():
    if len(sys.argv) < 2:
        print("用法: experiment_designer.py \"<研究问题>\"")
        print("例: experiment_designer.py \"多Agent系统的信用分配问题\"")
        sys.exit(1)
    
    problem = " ".join(sys.argv[1:])
    
    abstracts, synthesis = load_knowledge()
    
    if not synthesis:
        print("❌ 知识库为空，请先运行 fetch_arxiv_abstract.py")
        sys.exit(1)
    
    relevant = find_relevant_papers(problem, synthesis)
    
    if not relevant:
        print(f"⚠️ 未找到与「{problem}」直接相关的论文")
        print(f"   知识库中共有 {len(synthesis)} 篇论文")
        relevant = list(synthesis.items())[:3]
        relevant = [(aid, 0) for aid, s in synthesis.items()][:3]
    
    design = generate_experiment_design(problem, relevant, synthesis, abstracts)
    print_design(design)
    
    # 保存结果
    output_path = f"{MEMORY_DIR}/expert_tracker/experiment_designs.json"
    try:
        existing = []
        if os.path.exists(output_path):
            with open(output_path) as f:
                existing = json.load(f)
        
        existing.append(design)
        with open(output_path, "w") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 设计已保存: {output_path}")
    except Exception as e:
        print(f"\n⚠️ 保存失败: {e}")

if __name__ == "__main__":
    main()
