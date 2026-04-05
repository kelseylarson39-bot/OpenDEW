# Copilot Instructions for OpenDEW

## 🧭 About this repository
This repo contains **GNU Radio Companion (.grc) flowgraphs**. Each `.grc` file is an XML representation of a signal-processing flow graph that is typically edited in the GNU Radio Companion GUI and can be generated into Python by `grcc`.

There is no traditional build/test system; this repo is primarily a set of signal-processing configurations that are interpreted by GNU Radio.

## ✅ What an AI agent should do here
- Treat `.grc` files as structured XML. Prefer making changes by understanding the logic rather than indiscriminately reformatting.
- When asked to add new functionality, prefer adding or updating blocks inside existing flowgraphs instead of rewriting the full file unless the change clearly benefits from it.
- When asked to create new examples, create a new `.grc` file with a clear name and include comments/metadata where appropriate.

## 🛠️ How to run / validate changes
- Open `.grc` files in **GNU Radio Companion** (usually invoked with `gnuradio-companion` on Linux; on Windows it may be installed as part of a GNU Radio bundle).
- In GNU Radio Companion, you can generate/run a Python flowgraph; build artifacts are not committed.
- For quick XML sanity checks, ensure the file remains valid XML and respects the GRC schema (e.g., only supported block keys and params).

## 🧩 Project conventions & patterns
- Each `.grc` file represents a top-level flow graph. Don’t assume there are any helper scripts in this repo.
- Preserve existing `run_command` and `run_options` settings unless you understand how GNU Radio Companion uses them.
- Prefer descriptive variable names for `variable` blocks (e.g., `samp_rate`, `freq`, `gain`).

## 📌 When you’re unsure
If you need to modify or extend a flowgraph but lack domain context, ask the user for:
1. The intended signal chain or use case (e.g., “What radio standard or source/sink are you targeting?”)
2. Expected input/output types (sample rate, modulation, device, file vs. hardware).

## 🧠 How this impacts copilot/chat behavior
- Keep responses focused and actionable (e.g., “To add an FM demodulator, add a WBFM receiver block and connect it to an audio sink.”)
- Avoid speculative changes; if uncertain, ask a clarifying question.
- Do not introduce external dependencies or build tools unless explicitly requested.
