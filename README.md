# wiig-summarize

Profile-driven summarization, taken from nlp_service (its `summarizer`
module). FastAPI on port 8000.

**It holds no model and needs no GPU.** A profile is a prompt plus the JSON
schema its answer must follow. The service trims long inputs with an extractive
pre-pass (sumy), asks Ollama (`ollama_high`, over wiig-net) to write, then
validates the answer and retries if it doesn't match the schema.

| From | URL |
|---|---|
| A container on `wiig-net` | `http://wiig-summarize:8000` |
| The host | None by default. `docker-compose.debug.yml` publishes `127.0.0.1:9907` while you debug |

| Endpoint | What it does |
|---|---|
| `POST /summarize` | `{"profile": "...", "fields": {...}}`: fills the profile from `fields` and returns its `result` |
| `GET /healthz`, `GET /readyz` | Liveness, readiness |

| Profile | Writes |
|---|---|
| `article` | headline and summary of a news article |
| `entity_desc`, `relation_desc` | a description of an entity or a relation, from its mentions |
| `requirement_desc`, `criterion_desc` | a description of a tender's requirement or award criterion |
| `criterion_formula` | an award criterion's scoring formula, as an expression with its variables (checked safe before it's returned) |
| `aggregate` | one text from several |

The profiles are tied to the projects that wrote them (news; procurement). A
new one is a prompt file in `nlp/summarizer/prompts/` plus an entry in
`nlp/summarizer/profiles.py`. The prompts are in Spanish. The model is
`OLLAMA_MODEL` in `.env`, pulled into `ollama_high`.

## Deploying

Part of the shared AI services on `wiig-net`. The network, the naming rules
and the server runbook are in
[wiig-ops](https://github.com/oeg-metacognition/wiig-ops).

```sh
cp .env.example .env    # adjust
docker compose up -d --build
```
