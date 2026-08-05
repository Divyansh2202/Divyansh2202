<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Divyansh2202/Divyansh2202/main/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Divyansh2202/Divyansh2202/main/banner-light.svg">
  <img alt="Divyansh Rai — AI Engineer. LLM/VLM fine-tuning, multi-agent systems, RAG, production GenAI. Available for hire." src="https://raw.githubusercontent.com/Divyansh2202/Divyansh2202/main/banner-light.svg" width="100%">
</picture>

<br/>

**[divyanshrai.dev](https://divyanshrai.dev)** · [Email](mailto:divyanshr988@gmail.com) · [LinkedIn](https://linkedin.com/in/divyanshrai01) · [Resume](https://divyanshrai.dev/resume)

</div>

---

I take GenAI features from a notebook to production — fine-tuned LLMs and VLMs,
multi-agent orchestration, and RAG pipelines that stay fast, cheap, and
debuggable under real traffic.

**Available now** · Remote, hybrid or on-site · Open to relocating · IST, full overlap with EU and mornings with US East

---

## Shipped to production

Three systems serving real users at **TapHealth** (Mar 2025 – Jul 2026), not demos.

| System | What it does | What it took |
|---|---|---|
| **Multimodal macro-nutrient pipeline** | Logs meals from speech, text or a photo | ASR + NLP + Vision over a 10K-recipe / 30K-alias store. ~2s on the DB path, 3–5s on LLM fallback, ~90% accuracy |
| **AI Coach** | Conversational health agent | Rebuilt the orchestration onto a bounded tool-calling loop over 13 steps, driven by 16+ Kafka event domains |
| **Qwen3-VL-2B fine-tune** | Food recognition at the edge | 300K+ samples curated; 6GB → 1.9GB INT4 GGUF (68% smaller) with accuracy held; ≤6s on-device |

---

## Open source

### [mnemos](https://github.com/Divyansh2202/mnemos) — a memory layer for AI assistants

Assistants forget everything between sessions. mnemos extracts facts from
conversations, embeds them with `bge-m3`, and injects the relevant ones before
each new message — invisibly, across ChatGPT and Claude. Memories are stored per
user rather than per platform, so context follows the person instead of resetting
with the tool.

`FastAPI` · `PostgreSQL + pgvector` · `Ollama` · `Chrome Extension (MV3)` · `MCP`

### [toolcontract](https://pypi.org/project/toolcontract/) — contract testing for LLM tool calls

`pip install toolcontract`

---

## Research

- **AECA** — whether an agent can learn *when* to keep a memory raw, compress it
  to a skill, or crystallise it into a rule, instead of using one fixed
  compression level for everything.
- **RLVR-TTT** — pairing test-time training with verifiable rewards, so a weight
  update is kept only when it measurably helps.
- **ICICES 2023 (IET DAVV)** — published: data science for precision agriculture.

---

## Stack

**Models** &nbsp;PyTorch · Unsloth · TRL · LoRA / QLoRA · GGUF · INT4 · llama.cpp · vLLM
**Agents** &nbsp;Vercel AI SDK · LangGraph · LangChain · MCP · tool-calling
**Retrieval** &nbsp;pgvector · FAISS · embeddings · hybrid search · reranking
**Platform** &nbsp;Python · TypeScript · FastAPI · PostgreSQL · Redis · Kafka · ClickHouse · Docker
**Observability** &nbsp;Langfuse · OpenTelemetry · trace, cost and latency budgets

---

<div align="center">

Building something that needs an AI engineer who ships?

**[divyanshrai.dev](https://divyanshrai.dev)** · **[divyanshr988@gmail.com](mailto:divyanshr988@gmail.com)**

</div>
