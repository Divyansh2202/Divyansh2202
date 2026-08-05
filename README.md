<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Divyansh2202/Divyansh2202/main/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Divyansh2202/Divyansh2202/main/banner-light.svg">
  <img alt="Divyansh Rai — AI Engineer. Retrieval, model and agent layers. Available for hire." src="https://raw.githubusercontent.com/Divyansh2202/Divyansh2202/main/banner-light.svg" width="100%">
</picture>

<br/><br/>

<a href="https://divyanshrai.dev"><img alt="Portfolio" src="https://img.shields.io/badge/Portfolio-divyanshrai.dev-007b7c?style=for-the-badge&logo=safari&logoColor=white&labelColor=0b1015"></a>
<a href="mailto:divyanshr988@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-divyanshr988-c2410c?style=for-the-badge&logo=maildotru&logoColor=white&labelColor=0b1015"></a>
<a href="https://linkedin.com/in/divyanshrai01"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-divyanshrai01-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=0b1015"></a>
<a href="https://divyanshrai.dev/resume"><img alt="Resume" src="https://img.shields.io/badge/Resume-read-6d4bd6?style=for-the-badge&logo=readdotcv&logoColor=white&labelColor=0b1015"></a>

</div>

---

I take GenAI features from a notebook to production — fine-tuned LLMs and VLMs,
multi-agent orchestration, and RAG pipelines that stay fast, cheap, and
debuggable under real traffic.

**Available now** · Remote, hybrid or on-site · Open to relocating · IST, full overlap with EU and mornings with US East

---

## 🧩 toolcontract — contract testing for LLM tool-calls

<a href="https://pypi.org/project/toolcontract/"><img alt="PyPI" src="https://img.shields.io/pypi/v/toolcontract?style=flat-square&logo=pypi&logoColor=white&label=PyPI&color=007b7c&labelColor=0b1015"></a>
<a href="https://pypistats.org/packages/toolcontract"><img alt="Downloads" src="https://img.shields.io/pypi/dm/toolcontract?style=flat-square&label=downloads&color=6d4bd6&labelColor=0b1015"></a>
<a href="https://github.com/Divyansh2202/toolcontract/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/Divyansh2202/toolcontract/actions/workflows/ci.yml/badge.svg"></a>

**The problem.** A provider ships a new model version and your agent's
tool-calling quietly changes — an argument is invented or dropped, a different
tool gets picked for the same input, a value stops matching the schema your
downstream code depends on. Your tests still pass, because nothing in a normal
CI pipeline asserts on *which tools got called with what*. You find out in
production.

**The idea.** Pin a golden set of expected tool-call trajectories, replay them
against a live model, and get a verdict plus a diff. Pact does this for
microservice contracts; Percy does it for visual regressions. `toolcontract`
does it for tool calls.

```mermaid
flowchart LR
    A["Contract<br/><i>input + expected calls</i>"] --> R
    T["Tool schemas"] --> R
    R["Runner"] -->|"replay"| M["Live model<br/><i>OpenAI · Anthropic · LiteLLM</i>"]
    M -->|"actual tool calls"| C["Comparators"]
    R --> C
    C --> J{"Match?"}
    J -->|"structural + semantic"| V["PASS"]
    J -->|"drift found"| F["FAIL + diff"]
    J -->|"no signal"| I["INCONCLUSIVE"]
    V --> L[("Verification<br/>ledger")]
    F --> L
    I --> L

    style A fill:#007b7c,stroke:#007b7c,color:#fff
    style T fill:#007b7c,stroke:#007b7c,color:#fff
    style M fill:#6d4bd6,stroke:#6d4bd6,color:#fff
    style V fill:#15803d,stroke:#15803d,color:#fff
    style F fill:#b91c1c,stroke:#b91c1c,color:#fff
    style I fill:#b5731a,stroke:#b5731a,color:#fff
```

```bash
pip install toolcontract
toolcontract run contracts/ --provider openai --model gpt-4o --tools tools.json
```

Ships with the contract model, a comparator/matching engine, a verification
ledger, OpenAI / Anthropic / LiteLLM adapters, a CLI (`run` / `accept` /
`check-version`), a pytest plugin, and an LLM-judge tier for semantic matching.

> **Honest gap:** the adapters are verified against real provider APIs for
> request-building, auth and error handling, but not yet end-to-end through a
> genuine successful tool-call response — every live attempt so far hit a
> billing wall first. Those fixtures are research-backed, not live-confirmed.

---

## 🧠 mnemos — a memory layer for AI assistants

<a href="https://github.com/Divyansh2202/mnemos"><img alt="Repo" src="https://img.shields.io/badge/GitHub-mnemos-181717?style=flat-square&logo=github&logoColor=white&labelColor=0b1015"></a>
<a href="https://github.com/Divyansh2202/mnemos/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Divyansh2202/mnemos?style=flat-square&color=f0b23f&labelColor=0b1015"></a>
<a href="https://divyanshrai.dev/projects/mnemos"><img alt="Live demo" src="https://img.shields.io/badge/Live-interactive%20demo-007b7c?style=flat-square&logo=vercel&logoColor=white&labelColor=0b1015"></a>

Assistants forget everything between sessions. mnemos extracts facts from
conversations, embeds them, and injects the relevant ones before each new
message — invisibly, across ChatGPT and Claude. Memories live per *user*, not
per platform, so context follows the person instead of resetting with the tool.

```mermaid
flowchart LR
    U["You type<br/>in ChatGPT / Claude"] --> E["Chrome extension<br/><i>MV3</i>"]
    E -->|"intercept"| API["FastAPI"]
    API --> X["Extract facts<br/><i>LLM</i>"]
    X --> EM["Embed<br/><i>bge-m3</i>"]
    EM --> DB[("PostgreSQL<br/>+ pgvector")]
    API -->|"retrieve top-k"| DB
    DB --> INJ["Inject context"]
    INJ --> P["Prompt the model<br/>actually sees"]

    style E fill:#f0b23f,stroke:#f0b23f,color:#000
    style API fill:#6d4bd6,stroke:#6d4bd6,color:#fff
    style DB fill:#007b7c,stroke:#007b7c,color:#fff
    style P fill:#15803d,stroke:#15803d,color:#fff
```

`FastAPI` · `PostgreSQL + pgvector` · `Ollama` · `Chrome Extension (MV3)` · `MCP`

---

## 🚀 Shipped to production

Three systems serving real users at **TapHealth** (Mar 2025 – Jul 2026).

| System | What it does | What it took |
|---|---|---|
| **Multimodal macro-nutrient pipeline** | Logs meals from speech, text or a photo | ASR + NLP + Vision over a 10K-recipe / 30K-alias store. ~2s on the DB path, 3–5s on LLM fallback, ~90% accuracy |
| **AI Coach** | Conversational health agent | Rebuilt orchestration onto a bounded tool-calling loop over 13 steps, driven by 16+ Kafka event domains |
| **Qwen3-VL-2B fine-tune** | Food recognition at the edge | 300K+ samples curated; 6GB → 1.9GB INT4 GGUF (68% smaller) with accuracy held; ≤6s on-device |

---

## 🔬 Research

| | |
|---|---|
| **AECA** | Whether an agent can learn *when* to keep a memory raw, compress it to a skill, or crystallise it into a rule — instead of one fixed compression level for everything |
| **RLVR-TTT** | Pairing test-time training with verifiable rewards, so a weight update is kept only when it measurably helps |
| **ICICES 2023** | Published, IET DAVV — data science for precision agriculture |

---

## 🛠 Stack

| | |
|---|---|
| **Machine Learning** | PyTorch · TensorFlow · Scikit-Learn · Computer Vision · NLP · large-scale training pipelines |
| **Fine-Tuning & Optimisation** | LoRA · QLoRA · SFT · Unsloth · TRL · LLaMA-Factory · Quantization (GGUF, INT4) · llama.cpp · vLLM |
| **Generative AI & LLMs** | LLM/VLM system design · RAG pipelines · Prompt Engineering · Multi-Agent & Tool-Calling Systems |
| **LLM Orchestration** | Vercel AI SDK · LangGraph · LangChain |
| **Agentic Systems & SDKs** | MCP · Gemini SDK · Ollama · Memory: HindSight, Mem0 |
| **Backend & Data Infra** | Redis · Kafka · PostgreSQL · ClickHouse |
| **Observability** | Langfuse · OpenTelemetry · distributed tracing · cost & performance optimisation |
| **Vector Databases** | pgVector · semantic search · embedding pipelines |
| **Programming** | Python (Pandas, NumPy, SciPy) · SQL · OpenCV · NLTK · Streamlit · Hugging Face Transformers |
| **Deployment & MLOps** | Docker · Git · CI/CD · Edge AI deployment · scalable inference systems |
| **Data & Analytics** | Power BI · Matplotlib · Seaborn · SQL |

---

<div align="center">

### Building something that needs an AI engineer who ships?

<a href="https://divyanshrai.dev"><img alt="Portfolio" src="https://img.shields.io/badge/divyanshrai.dev-visit-007b7c?style=for-the-badge&logo=safari&logoColor=white&labelColor=0b1015"></a>
<a href="mailto:divyanshr988@gmail.com"><img alt="Email" src="https://img.shields.io/badge/divyanshr988@gmail.com-email%20me-c2410c?style=for-the-badge&logo=maildotru&logoColor=white&labelColor=0b1015"></a>

</div>
