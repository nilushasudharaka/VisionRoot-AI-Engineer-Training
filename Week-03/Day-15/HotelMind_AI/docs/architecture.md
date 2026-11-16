# Architecture and failures

```
API client -> FastAPI -> security checks -> orchestrator
                                    |-> SQLite vector retrieval (hashing embeddings)
                                    |-> allowlisted read-only tools
                                    |-> optional OpenAI Chat Completions LLM
                           -> redacted answer + source references
```

## Components
- **Ingestion:** Administrator-approved PDF, TXT, DOCX <=2 MB; parse and chunk; indexes into SQLite.
- **Vector store:** SQLite contains normalized hashed word/bi-gram vectors; dot product similarity finds top 3 passages. This is a small-project vector database design, not scalable ANN retrieval or semantic transformer embeddings.
- **Orchestrator:** answer uses passages only; clearly labels fallback as `extractive-demo` when API key is absent. Optional LLM receives untrusted source excerpts.
- **Tools:** exactly 3 read-only tools, checked by allowlist. No shell/database writes exposed to the AI.
- **Security:** admin upload key, size/ext restriction, validation, redaction, allowlisted tools, limited output size. Pattern-based prompt-injection detection is not foolproof.

## Failure behavior
- **Missing vector index:** no-evidence response, not a fabricated answer.
- **Unsupported/corrupt upload:** 415/422 response; does not enter index.
- **Wrong admin key:** 401; no upload.
- **Prompt injection in question:** known patterns rejected, but novel attacks may pass.
- **Provider not configured:** deterministic extractive-demo mode; no false claim of LLM generation.
- **Provider fails:** generic provider-error; no credentials or stack traces returned.
- **Search misses relevant content:** indicates no evidence; needs evaluation and better embeddings.

## Important limitations
- Local training prototype, not production hardened: no HTTPS termination, rate limits, malware scanning, real identity provider, audit trail, tenant-level authorization, secrets manager, durable multiuser operations, or comprehensive injection defenses.
- Approval here means possession of the admin upload key, not human content review. Do not upload unapproved or sensitive documents.
- Hashed vector similarity is lexical, not truly semantic embeddings. For larger production workloads switch to sentence-transformer/provider embeddings and a proper vector index.
