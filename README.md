# Paper-Radar

A RAG system for scientific literature, built with n8n. Every day it fetches new arXiv papers on general AI, AI in society, AI in medicine, computational neuroscience, neurotech & BCI, has Claude rate and summarize them and send a weekly digest grouped by topic via Telegram. A chat workflow answers questions about the stored papers in a chat, with sources.

![Chat answer with sources](docs/chat.png)

## Architecture

```mermaid
flowchart TB
    subgraph A[Paper-Radar Import, daily]
        A0[Code in JavaScript<br/>5 topic queries, last 7 days] --> A1[arXiv abrufen<br/>3 s pause per query]
        A1 --> A2[XML to JSON<br/>In Papers splitten<br/>Felder aufräumen]
        A2 --> A3[Remove Duplicates<br/>Nur neue Papers]
        A3 --> A4[Relevanz einordnen<br/>Claude Haiku]
        A4 --> A5[Edit Fields<br/>Insert row]
        A5 --> A6[Nur relevante<br/>score 7 or higher]
    end
    A5 --> T[(Data Table papers<br/>all papers)]
    A6 --> Q[(Qdrant papers<br/>one vector per paper)]
    E[Embeddings Ollama<br/>nomic-embed-text] -.-> Q
    subgraph B[Weekly Digest, Mondays 9 am]
        B1[Relevante Papers holen<br/>Nur diese Woche<br/>Alle zusammenfassen] --> B2[Digest schreiben<br/>Claude Haiku] --> B3[Digest senden<br/>Telegram]
    end
    subgraph C[Paper-Radar Chat]
        C1[Chat] --> C2[Paper-Assistent<br/>Claude Sonnet + Simple Memory]
    end
    T --> B1
    Q -->|Tool: paper_suche| C2
```

Node names are in German, as in the workflow files.

| Workflow | File | Screenshot |
| --- | --- | --- |
| Paper-Radar Import | `workflows/import.json` | [docs/import.png](docs/import.png) |
| Weekly Digest | `workflows/digest.json` | [docs/digest.png](docs/digest.png) |
| Paper-Radar Chat | `workflows/chat.json` | [docs/chat.png](docs/chat.png) |

### Weekly digest in Telegram

<img src="docs/telegram.png" alt="Weekly digest in Telegram" width="360">


## Setup

1. n8n runs in Docker as a container named `n8n`.
2. Start Qdrant and Ollama: `bash docker/setup.sh`
3. Create credentials in n8n: Qdrant (`http://qdrant:6333`), Ollama (`http://ollama:11434`), Anthropic, Telegram (your own bot via `@BotFather`).
4. Create a Data Table `papers` with the columns `arxiv_id`, `titel`, `autoren`, `veroeffentlicht`, `link`, `score` (Number), `kategorie`, `zusammenfassung`, `erfasst`, `abstract`.
5. Import the three workflows from `workflows/` ("…" → "Import from File"), assign credentials and the Data Table, and replace `DEINE_CHAT_ID` in "Digest senden" with your Telegram chat ID.
6. Activate Import and Digest. Use the chat via "Open chat" in the "Paper-Radar Chat" workflow.

The prompts and the code for the topic queries are also available as files in `prompts/`.

## Limitations

- Abstracts only, no full texts.
- For large categories such as cs.AI, each query returns at most 40 papers.
- The relevance rating relies on LLM judgement.

## Data

Metadata and abstracts come from [arXiv](https://arxiv.org/). The repository contains no stored papers, only the workflows.

Thank you to arXiv for use of its open access interoperability.
