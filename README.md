# Groww · HDFC Mutual Fund Assistant (RAG Pipeline)

A facts-only, cited retrieval system built for retail investors on Groww to query HDFC Mutual Fund schemes. Every answer is grounded strictly on official AMC, SEBI, and AMFI documentation, capped at <= 3 sentences, contains exactly one primary source URL, and appends a deterministic date stamp. Subjective queries, recommendations, return projections, and PII are intercepted and refused prior to retrieval.

---

## Architecture & System Design

User Query
    │
    ▼
[Pre-Retrieval Guardrail] ──(PII / Advice / Performance)──► Polite Safe Refusal + AMFI Education Link
    │
    ▼ (Factual Query)
[Embedding Engine & Vector Store] (Cosine Top-k against Scheme Documents)
    │
    ▼
[Context Injection & LLM Orchestrator] (Strict Grounding: <=3 sentences + Official AMC URL)
    │
    ▼
Formatted Grounded Response + "Last updated from sources: October 2026"

### Core Components
- **Modular Pipeline:** Guardrails, retrieval logic, and generation templates are decoupled in `ragchat/`.
- **Corpus Ingestion:** Cleaned scheme documentation with front-matter metadata stored under `documents/`.
- **Deterministic Disclaimers:** Explicit guard against financial advisory violations under SEBI RA regulations.

---

## Two-Tier Refusal Architecture

1. **Pre-Retrieval Guardrails (`ragchat/guardrails.py`):**
   - **PII Shield:** Intercepts PAN, Aadhaar, account numbers, email addresses, and OTPs with a standard privacy caution before context lookup.
   - **Advisory Gate:** Intercepts subjective questions (*"Which fund gives the best return?"*, *"Should I buy Flexi Cap?"*) and routes the user to official investor education resources.
2. **Grounded Fact Retrieval (`ragchat/retriever.py`):**
   - Answers must match official fund attributes (Expense Ratio, Exit Load, Statutory ELSS Lock-in, Benchmark & Riskometer).
   - Unverified or out-of-scope inquiries are declined cleanly rather than hallucinated.

---

## Scope & Selected Corpus

- **Host Product:** Groww
- **Target AMC:** HDFC Mutual Fund
- **Core Schemes Covered:**
  1. HDFC Large Cap Fund (Equity Large Cap)
  2. HDFC Flexi Cap Fund (Equity Flexi Cap)
  3. HDFC ELSS Tax Saver Fund (Equity ELSS)
  4. HDFC Mid-Cap Fund (Equity Mid Cap)

Official indexed sources are detailed in [`sources.csv`](./sources.csv).

---

## Setup & How to Run

### 1. Hosted Web App (Streamlit)
Access the live deployment directly via the [Streamlit Cloud Prototype](https://milestone-terbj7w3cprkfxgppgmrtd.streamlit.app/).

### 2. Local Installation
```bash
git clone [https://github.com/abhishek24026/milestone.git](https://github.com/abhishek24026/milestone.git)
cd milestone
pip install -r requirements.txt
streamlit run app.py
---

## Verification & Sample Q&A

| Category | Input Query | System Response | Citation |
| :--- | :--- | :--- | :--- |
| **Expense Ratio** | What is the expense ratio of HDFC Flexi Cap Fund? | The Net Expense Ratio for HDFC Flexi Cap Fund (Direct Plan) is approximately 0.78% as per official factsheets. Regular plans carry additional distribution expenses. | [HDFC Flexi Cap Scheme Page](https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct) |
| **Lock-in Period** | What is the lock-in period for ELSS Tax Saver? | HDFC ELSS Tax Saver Fund has a statutory mandatory lock-in period of 3 years from the date of allotment of each unit. Investments qualify for tax deductions under Section 80C. | [HDFC ELSS Scheme Page](https://www.hdfcfund.com/product-solutions/overview/hdfc-elss-tax-saver/direct) |
| **Account Docs** | How do I download my capital gains statement? | To download your Capital Gains statement, visit the HDFC Mutual Fund Account Statement portal or generate your Consolidated Account Statement (CAS) via CAMS/KFintech. | [HDFC Statements Guide](https://www.hdfcfund.com/account-statement) |
| **Advisory Refusal** | Which fund should I buy for the highest return? | I only provide verified scheme facts and cannot offer investment advice, recommendations, or portfolio reviews. Please consult a SEBI-registered advisor or review mutual fund fundamentals at AMFI Investor Corner. | [AMFI Knowledge Center](https://www.amfiindia.com/uploads/AMFI_Understanding_Mutual_Funds_IAP_Booklet_Final_Website_version_860a5b77aa.pdf) |
| **PII Shield** | My PAN is ABCDE1234F, check my portfolio. | ⚠️ Please do not share any personal or sensitive information (PAN, Aadhaar, account details, OTP). This assistant only answers general fund facts. | *Intercepted pre-retrieval* |

---

## Known Limits & Boundaries
- Restricted exclusively to public equity factsheet parameters; does not compute forward CAGR or portfolio overlaps.
- Only official public AMC/SEBI/AMFI pages are indexed. No third-party financial blogs or unofficial platforms.
- Completely stateless user sessions with zero database persistence of user prompts.
