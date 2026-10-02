# 📝 Technical Writing Doc-Ops Workbench

An AI-assisted documentation engineering application built with 
**Python**, **Streamlit**, and **Claude 3.5 Sonnet** (via the Anthropic 
API).

This tool streamlines two critical phases of the technical writing 
lifecycle:
1. **Pre-Drafting Gap Analysis:** Scans messy, unstructured engineering 
meeting transcripts and sync notes to identify missing API payload 
schemas, unspecified edge cases, and unassigned feature owners.
2. **Post-Drafting Release Synthesis:** Transforms resolved Jira ticket 
details and raw release specs into executive stakeholder summaries and 
structured documentation outlines.

---

## 🚀 Key Features

* **Instant Demo Mode:** Pre-loaded with realistic engineering meeting 
notes and specs for instant evaluation without requiring an API key.
* **Live LLM Integration:** Optional live execution powered by 
Anthropic's Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`).
* **Downloadable Deliverables:** One-click markdown exports (`.md`) for 
gap checklists and doc outlines.
* **Stateless & Secure:** Processing runs in-memory with client-side API 
key configuration—no credentials or private notes are stored.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Frontend/Framework:** Streamlit
* **AI Model:** Anthropic Claude 3.5 Sonnet
* **Deployment:** Streamlit Community Cloud

---

## 🏃 Local Setup Instructions

To run this application locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone 
[https://github.com/amberchantell/github-portfolio.git](https://github.com/amberchantell/github-portfolio.git)
   cd github-portfolio# 
github-portfolio
