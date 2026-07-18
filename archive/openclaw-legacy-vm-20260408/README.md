# OpenClaw Legacy VM — Sanitized Design Delta

This repository branch is a recovery checkpoint for historical design context only. It carries no runtime authority and must not activate legacy agents, hooks, workflows, schedulers, model routing, or credentials.

- Sources: immutable `a7f6… → e92f…` changed blobs, `ec656…` workspace blobs, one hash-verified untracked sentinel, and selected `.xuzhi_custom` docs/scripts.
- Safety: runtime/control paths excluded; credential-shaped values redacted; active filenames and executable source extensions neutralized with `.source.txt`.
- Storage: identical sanitized content is stored once; `manifest.json` maps every original path and SHA-256.
- Restore: inspect `manifest.json`, verify hashes, and copy only the specific design document needed. Do not execute archived source directly.
