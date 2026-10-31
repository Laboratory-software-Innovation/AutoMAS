# AutoMAS — Automated Generation of Multi-Agent Systems


> **AutoMAS** is the first framework to automate the end-to-end generation of functional LangGraph-based multi-agent system implementations from a natural language description, achieving Pass1Rate of 82.75% and accuracy of 89.78% on the literature dataset — outperforming all zero-shot and one-shot baselines across GPT-4.1, DeepSeek, and Claude Sonnet 4.5.

---

## 🔍 What is AutoMAS?

LLM-based multi-agent systems are rapidly emerging as a powerful paradigm for automating complex software engineering tasks, yet constructing functional implementations remains a largely manual and error-prone process. State-of-the-art zero-shot and one-shot prompting approaches consistently fail to generate compilable, let alone functional, multi-agent system code across leading LLMs.

**AutoMAS** addresses this gap by decomposing the generation task into five cooperative layers:

| Layer | Role |
|---|---|
| 🎯 **Orchestrator** | Classifies task as single-agent or multi-agent and routes accordingly |
| 🏗️ **Architect** | Designs the high-level agent structure, roles, and interaction topology |
| 🔧 **Tool Agent** | Identifies, generates, and binds tools required by each agent |
| 💻 **Developer** | Generates complete, executable LangGraph implementation |
| ✅ **Tester** | Validates via syntax checking, AST validation, auto-repair, and runtime execution |

---

## 📊 Dataset

**Location:** `dataset/Dataset Multi-agent.xlsx`

Our dataset comprises **91 real-world agentic systems** collected from two sources:

- **29** implementations from academic literature
- **62** open-source GitHub repositories

Each entry includes:
- **Agent Intent** — natural language description of the agent's purpose
- **Type** — single-agent or multi-agent
- **Domain** — finance, healthcare, software engineering, security, etc.
- **Tools** — list of tools and APIs used
- **Memory** — memory mechanism employed
- **LLM** — underlying language model
- **Test Cases** — base behavioral test cases
- **Extended Test Cases** — node-level coverage test cases

---

## 🗂️ Repository Structure

```
automas/
│
├── dataset/
│   └── Dataset Multi-agent.xlsx     # Annotated dataset of 91 agentic systems
│
├── prompts/                         # Prompt templates for each pipeline layer
│   ├── orchestrator.md
│   ├── architect_single.md
│   ├── architect_multi.md
│   ├── tool_planner.md
│   ├── tool_generator.md
│   ├── developer.md
│   └── tester.md
│
├── approach/
│   └── automas.ipynb                # Main AutoMAS pipeline notebook
│
├── sota/
│   └── baselines.ipynb              # Zero-shot, one-shot, and SEW baselines
│
├── scripts/                         # Data processing and evaluation scripts
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install langgraph langchain-openai langchain-core openai
```

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/automas.git
cd automas

# 2. Set your API key
export OPENAI_API_KEY=your_key_here

# 3. Open and run the main pipeline
jupyter notebook approach/automas.ipynb
```

---

## 📈 Results

| Method | Literature Pass1Rate | Literature Accuracy | GitHub Pass1Rate | GitHub Accuracy |
|---|---|---|---|---|
| **AutoMAS** | **82.75%** | **89.78%** | **72.58%** | **82.43%** |
| One-shot Claude | 72.41% | 86.67% | 59.68% | 67.85% |
| Zero-shot GPT | 58.60% | 83.27% | 51.61% | 74.19% |
| One-shot DeepSeek | 20.68% | — | — | — |
| SEW | ✗ Incompatible | — | ✗ Incompatible | — |

---

## 🧠 Prompts

**Location:** `prompts/*.md`

Each prompt is designed for a specific layer of the AutoMAS pipeline and follows the **RISE framework** (Role, Instructions, Steps, Expectation). Prompts are modular and can be adapted for different LLMs or extended to support additional agent frameworks beyond LangGraph.

---

## 📝 Citation

If you use AutoMAS or our dataset in your research, please cite:

```bibtex
@inproceedings{raza2026automas,
  title     = {{AutoMAS}: End-to-End Generation of Functional Multi-Agent Systems},
  author    = {Raza, Muhammad Anas and Islam, Niful and Wardat, Mohammad},
  booktitle = {2026 IEEE International Conference on Software Quality, Reliability, and Security (QRS)},
  year      = {2026},
  url       = {https://github.com/Laboratory-software-Innovation/automas}
}
```

---

## 📬 Contact

For questions or issues, please open a GitHub issue or contact the authors directly.
