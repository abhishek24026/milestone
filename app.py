import streamlit as st

st.set_page_config(page_title="Groww | HDFC MF Assistant", page_icon="📈", layout="centered")

# Custom CSS matching INDmoney / Abhay Garg style
st.markdown("""
<style>
    .main-card {
        background-color: #0f172a;
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        border: 1px solid #1e293b;
    }
    .badge {
        background-color: #334155;
        color: #94a3b8;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 6px;
    }
    .disclaimer {
        color: #ef4444;
        font-size: 13px;
        margin-top: 15px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Top Header Card
st.markdown("""
<div class="main-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <span style="font-weight: 700; color: #00d09c; font-size: 18px;">Groww <span style="color: #94a3b8; font-weight: 400; font-size: 14px;">· Mutual Fund Assistant</span></span>
        <span class="badge">Knowledge Base: 19 Sources</span>
    </div>
    <h2 style="color: white; margin-top: 0; font-size: 26px;">Know your HDFC fund before you invest in it.</h2>
    <p style="color: #cbd5e1; font-size: 15px; margin-bottom: 12px;">
        Ask about expense ratios, exit loads, lock-in periods, benchmarks and fund facts. Every answer links back to the official page it came from.
    </p>
    <div style="margin-bottom: 10px;">
        <span class="badge">HDFC Mutual Fund</span>
        <span class="badge">SEBI</span>
        <span class="badge">AMFI</span>
    </div>
    <div class="disclaimer">🔒 Facts only. This assistant does not give investment advice.</div>
</div>
""", unsafe_allow_html=True)

# Knowledge Base (Grounding with Claude's verified HDFC sources)
FACTS = [
    {
        "keywords": ["expense ratio", "ter", "charges", "fees", "flexi cap"],
        "answer": "The Net Expense Ratio for HDFC Flexi Cap Fund (Direct Plan) is approximately 0.78% as per official factsheets. Regular plans have higher expense ratios to account for distributor commissions.",
        "link": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct",
        "date": "October 2026"
    },
    {
        "keywords": ["lock in", "elss", "lock-in", "tax", "tax saver"],
        "answer": "HDFC ELSS Tax Saver Fund has a statutory mandatory lock-in period of 3 years from the date of allotment of each unit. Investments qualify for tax deductions under Section 80C.",
        "link": "https://www.hdfcfund.com/product-solutions/overview/hdfc-elss-tax-saver/direct",
        "date": "October 2026"
    },
    {
        "keywords": ["capital gains", "statement", "download", "cas", "tax statement"],
        "answer": "To download your Capital Gains statement, visit the HDFC Mutual Fund Account Statement portal or generate your Consolidated Account Statement (CAS) via CAMS/KFintech.",
        "link": "https://www.hdfcfund.com/account-statement",
        "date": "October 2026"
    },
    {
        "keywords": ["exit load", "redemption fee", "large cap"],
        "answer": "For HDFC Large Cap Fund, an exit load of 1% is applicable if units are redeemed or switched out within 1 year from the date of allotment. Nil exit load applies thereafter.",
        "link": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct",
        "date": "October 2026"
    },
    {
        "keywords": ["mid cap", "midcap", "benchmark", "riskometer"],
        "answer": "HDFC Mid Cap Fund (formerly HDFC Mid Cap Opportunities Fund) is benchmarked against NIFTY Midcap 150 TRI and is categorized as 'Very High Risk' on the scheme riskometer.",
        "link": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-mid-cap-fund/regular",
        "date": "October 2026"
    }
]

REFUSALS = ["should i buy", "should i sell", "best fund", "recommend", "advice", "which is better", "portfolio", "returns comparison"]
PII_TERMS = ["pan", "aadhaar", "phone", "email", "otp", "account number", "bank"]

def get_answer(query):
    q = query.lower()
    
    # 1. PII Guardrail
    if any(p in q for p in PII_TERMS) and ("my" in q or "is" in q):
        return "⚠️ Please do not share any personal or sensitive information (PAN, Aadhaar, account details, OTP). This assistant only answers general fund facts."
    
    # 2. Advice Refusal Guardrail
    if any(r in q for r in REFUSALS):
        return (
            "I only provide verified scheme facts and cannot offer investment advice, recommendations, or portfolio reviews. "
            "Please consult a SEBI-registered advisor or review mutual fund fundamentals at [AMFI Investor Corner](https://www.amfiindia.com/uploads/AMFI_Understanding_Mutual_Funds_IAP_Booklet_Final_Website_version_860a5b77aa.pdf)."
        )
    
    # 3. Fact Matching
    match = None
    max_k = 0
    for f in FACTS:
        k_count = sum(1 for kw in f["keywords"] if kw in q)
        if k_count > max_k:
            max_k = k_count
            match = f
            
    if match and max_k > 0:
        return f"{match['answer']}\n\n**Source:** [{match['link']}]({match['link']})\n\n*Last updated from sources: {match['date']}*"
    return "This query is outside the current indexed scope. Please verify directly via the [HDFC Mutual Fund Official Portal](https://www.hdfcfund.com/)."

# Preset Buttons like Abhay's UI
st.write("**Try asking:** *Tap a question to start*")
c1, c2, c3 = st.columns(3)
selected_query = None

if c1.button("What is the expense ratio of HDFC Flexi Cap Fund?"):
    selected_query = "What is the expense ratio of HDFC Flexi Cap Fund?"
if c2.button("How do I download my capital gains statement?"):
    selected_query = "How do I download my capital gains statement?"
if c3.button("What is the ELSS lock-in period?"):
    selected_query = "What is the ELSS lock-in period?"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Ask anything about HDFC mutual funds...")
final_query = selected_query or user_query

if final_query:
    st.session_state.chat_history.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.markdown(final_query)
        
    ans = get_answer(final_query)
    st.session_state.chat_history.append({"role": "assistant", "content": ans})
    with st.chat_message("assistant"):
        st.markdown(ans)
