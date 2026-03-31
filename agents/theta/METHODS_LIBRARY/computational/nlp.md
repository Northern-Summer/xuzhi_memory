# 自然语言处理 (NLP)

## 定义
自然语言处理是一系列计算方法，用于分析、理解和生成人类语言文本。

## 适用场景
- 大规模文本分析
- 情感和意见挖掘
- 主题发现和建模
- 文本分类和预测

## 核心技术栈

### 1. 基础处理
| 技术 | 功能 |
|------|------|
| 分词 (Tokenization) | 文本切分为词元 |
| 词性标注 (POS tagging) | 标注名词、动词等 |
| 命名实体识别 (NER) | 识别人名、地名、机构 |
| 依存句法分析 | 分析句子结构 |

### 2. 向量化表示
| 方法 | 特点 |
|------|------|
| TF-IDF | 词频-逆文档频率 |
| Word2Vec | 词嵌入（静态） |
| BERT embeddings | 上下文嵌入（动态） |
| Sentence Transformers | 句子级嵌入 |

### 3. 下游任务
| 任务 | 应用 |
|------|------|
| 文本分类 | 情感分析、主题分类 |
| 序列标注 | 命名实体识别、词性标注 |
| 文本生成 | 摘要、翻译、对话 |
| 问答系统 | 信息抽取、知识问答 |

## 操作步骤

### 1. 数据预处理
- 清洗（去除噪声、HTML 标签）
- 标准化（小写、词形还原）
- 分词
- 去停用词（谨慎，可能丢失信息）

### 2. 特征工程
- 选择向量化方法
- 构建 document-term matrix
- 可选：降维（PCA, UMAP）

### 3. 模型选择
- **传统 ML**: SVM, Random Forest, XGBoost
- **深度学习**: CNN, LSTM, Transformer
- **预训练模型**: BERT, RoBERTa, GPT

### 4. 训练和评估
- 划分训练/验证/测试集
- 交叉验证
- 评估指标：准确率、F1、AUC

### 5. 解释和验证
- 特征重要性分析
- 错误案例分析
- 领域专家验证

## 反事实推理（关键检验）

### 检验1：预训练偏见
- **如果**使用通用预训练模型
- **那么**可能携带训练语料的偏见
- **对策**：领域微调、偏见检测、对抗训练

### 检验2：标注质量
- **如果**标注数据质量差
- **那么**模型学到错误模式
- **对策**：多标注员、一致性检验、主动学习

### 检验3：领域迁移
- **如果**模型在领域外数据上应用
- **那么**性能可能急剧下降
- **对策**：领域适应、零样本/少样本学习

### 检验4：解释性
- **如果**只用黑箱模型
- **那么**无法解释预测原因
- **对策**：可解释 AI (SHAP, LIME, Attention 可视化)

## 前沿方法（2024-2026）

### 1. 大语言模型 (LLM) 应用
- **零样本/少样本学习**：无需微调
- **提示工程**：设计任务指令
- **思维链 (Chain-of-Thought)**：复杂推理
- **工具调用**：LLM + 外部工具

### 2. 多模态 NLP
- 文本 + 图像（图文理解）
- 文本 + 音频（语音情感）
- 工具：CLIP, GPT-4V, LLaVA

### 3. 社会科学专用模型
- **社会学**: SocBERT, SocioloBERT
- **政治学**: PolBERT
- **心理学**: MentalBERT
- **领域微调**: 在学科语料上继续预训练

### 4. 可解释 NLP
- Attention 可视化
- 探针任务 (Probing tasks)
- 反事实解释

## 工具栈
- **基础**: NLTK, spaCy, jieba (中文)
- **深度学习**: Hugging Face Transformers, PyTorch, TensorFlow
- **LLM**: OpenAI API, Claude API, 本地部署 (Ollama, vLLM)
- **可视化**: LIT, BertViz

## 社会科学应用案例

### 1. 计算社会学
- 社交媒体情感分析
- 政治文本分析
- 舆论动态建模

### 2. 文化分析
- 文化维度测量
- 价值观演化追踪
- 文化差异比较

### 3. 组织研究
- 企业年报分析
- 组织身份识别
- 网络文本挖掘

## 局限
- 语言依赖（模型多为英语）
- 领域迁移困难
- 上下文长度限制
- 计算资源需求
- 黑箱问题
- 偏见和伦理风险

## AI辅助应用（元认知）

### LLM 用于 NLP 研究本身
- **数据增强**：生成合成数据
- **标注辅助**：弱监督学习
- **代码生成**：自动化分析流水线
- **论文写作**：文献综述、方法描述

### ⚠️ 警告
- LLM 可能生成虚假引用
- 自动化分析需研究者审核
- 理论洞见来自人类，非模型

## 参考文献进阶阅读
- Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing* (3rd ed. draft).
- Eisenstein, J. (2019). *Introduction to Natural Language Processing*.
- Grimmer, J., & Stewart, B. M. (2013). Text as data. *Political Analysis*.
- Rodriguez, P. L., & Spirling, A. (2022). Word embeddings: What works, what doesn't, and how to tell the difference. *American Journal of Political Science*.
