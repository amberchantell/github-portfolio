# 🏗️ Technical Writing Doc-Ops Workbench — System Architecture

This document outlines the system design, data flow, and security considerations for the **Doc-Ops Workbench** Streamlit application.

## 🔐 Security & Privacy
- **Client-Side Keys:** Anthropic API keys are collected via password-masked UI inputs and passed directly to the Anthropic client instance in runtime memory.
- **Zero Storage:** No user prompts, meeting transcripts, or API credentials are logged, saved to disk, or stored in database systems.
