import streamlit as st
import sys
import io
from contextlib import redirect_stdout
import threading
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DeepDigest",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Background */
.stApp {
    background-color: #0c0e14;
    color: #e2e8f0;
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding: 2rem 3rem 4rem 3rem;
    max-width: 1100px;
}

/* ── Header ── */
.dd-header {
    text-align: center;
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #1e2535;
    margin-bottom: 2.5rem;
}
.dd-logo {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    color: #4ade80;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.dd-title {
    font-size: 3rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.1;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.03em;
}
.dd-title span {
    color: #4ade80;
}
.dd-subtitle {
    font-size: 1rem;
    color: #64748b;
    font-weight: 400;
    margin: 0;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background-color: #141720 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #4ade80 !important;
    box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.08) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #334155 !important;
}
.stTextInput label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
.stButton > button {
    background-color: #4ade80 !important;
    color: #0c0e14 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    padding: 0.8rem 2rem !important;
    width: 100% !important;
    text-transform: uppercase;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background-color: #86efac !important;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0px);
}

/* ── Pipeline steps ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #1e2535;
    border-radius: 10px;
    overflow: hidden;
    margin: 1.5rem 0;
}
.step-cell {
    background: #141720;
    padding: 1rem 0.85rem;
    text-align: center;
}
.step-cell.active {
    background: #0f1a14;
}
.step-cell.done {
    background: #0d1a12;
}
.step-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #1e2535;
    letter-spacing: 0.1em;
    margin-bottom: 0.35rem;
}
.step-num.active { color: #4ade80; }
.step-num.done { color: #22c55e; }
.step-icon {
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
}
.step-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #334155;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.step-label.active { color: #4ade80; }
.step-label.done { color: #86efac; }

/* ── Result cards ── */
.result-card {
    background: #141720;
    border: 1px solid #1e2535;
    border-radius: 10px;
    margin: 1rem 0;
    overflow: hidden;
}
.result-card-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.85rem 1.2rem;
    border-bottom: 1px solid #1e2535;
    background: #0f111a;
}
.result-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    background: rgba(74,222,128,0.1);
    color: #4ade80;
}
.result-card-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.result-card-body {
    padding: 1.2rem;
    font-size: 0.92rem;
    color: #cbd5e1;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
}
.result-card-body::-webkit-scrollbar { width: 4px; }
.result-card-body::-webkit-scrollbar-track { background: #0c0e14; }
.result-card-body::-webkit-scrollbar-thumb { background: #1e2535; border-radius: 2px; }

/* ── Final report ── */
.final-report-wrapper {
    background: linear-gradient(135deg, #0d1a12 0%, #0f111a 100%);
    border: 1px solid #22c55e40;
    border-radius: 12px;
    margin: 1.5rem 0;
    overflow: hidden;
}
.final-report-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #22c55e30;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.final-dot {
    width: 8px; height: 8px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 8px #4ade80;
}
.final-report-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #4ade80;
    text-transform: uppercase;
}
.final-report-body {
    padding: 1.5rem;
    font-size: 0.95rem;
    color: #e2e8f0;
    line-height: 1.85;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Critic card ── */
.critic-wrapper {
    background: #0e131c;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    margin: 1rem 0;
    overflow: hidden;
}
.critic-header {
    padding: 0.85rem 1.2rem;
    border-bottom: 1px solid #1e3a5f;
    background: #0c1017;
}
.critic-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #60a5fa;
    text-transform: uppercase;
}
.critic-body {
    padding: 1.2rem;
    font-size: 0.9rem;
    color: #93c5fd;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Status bar ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.7rem 1rem;
    background: #0f111a;
    border: 1px solid #1e2535;
    border-radius: 8px;
    margin: 1rem 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #64748b;
}
.pulse {
    width: 7px; height: 7px;
    background: #4ade80;
    border-radius: 50%;
    animation: pulse 1.4s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}
.divider {
    border: none;
    border-top: 1px solid #1e2535;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dd-header">
    <div class="dd-logo">🔬 Multi-Agent System</div>
    <h1 class="dd-title">Deep<span>Digest</span></h1>
    <p class="dd-subtitle">Search · Scrape · Report · Critique — automated research, end to end</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "running" not in st.session_state:
    st.session_state.running = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "error" not in st.session_state:
    st.session_state.error = None

# ── Helper: extract plain text from any agent output format ──────────────────
def extract_text(content) -> str:
    """
    Handles all the formats an agent message .content can come in:
      - plain str
      - list of dicts like [{'type':'text','text':'...'}, {'type':'reference',...}]
      - LangChain AIMessage / objects with a .content attr
    """
    if isinstance(content, str):
        return content
    if hasattr(content, "content"):          # AIMessage etc.
        return extract_text(content.content)
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content)

# ── Pipeline step renderer ────────────────────────────────────────────────────
def render_pipeline(current_step=0):
    steps = [
        ("01", "🔍", "Search"),
        ("02", "🕸️", "Scrape"),
        ("03", "📝", "Report"),
        ("04", "🎯", "Critique"),
    ]
    cells = ""
    for i, (num, icon, label) in enumerate(steps):
        s_idx = i + 1
        if s_idx < current_step:
            cls = "done"
        elif s_idx == current_step:
            cls = "active"
        else:
            cls = ""
        cells += f"""
        <div class="step-cell {cls}">
            <div class="step-num {cls}">{num}</div>
            <div class="step-icon">{icon}</div>
            <div class="step-label {cls}">{label}</div>
        </div>"""
    st.markdown(f'<div class="pipeline-grid">{cells}</div>', unsafe_allow_html=True)

# ── Input section ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1], gap="small")
with col1:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs 2024",
        label_visibility="visible",
        disabled=st.session_state.running,
    )
with col2:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run_btn = st.button(
        "▶ Run",
        disabled=st.session_state.running or not topic,
        use_container_width=True,
    )

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn and topic and not st.session_state.running:
    st.session_state.running = True
    st.session_state.results = None
    st.session_state.error = None
    st.session_state.current_step = 0
    st.rerun()

if st.session_state.running:
    render_pipeline(st.session_state.current_step)

    status_placeholder = st.empty()
    step_placeholder = st.empty()

    try:
        from agents import critic_chain, report_chain, bulid_search_agent, scrap_agent

        state = {}

        # ── Step 1: Search ──
        st.session_state.current_step = 1
        status_placeholder.markdown(
            '<div class="status-bar"><div class="pulse"></div>Step 1 — Search agent scanning the web…</div>',
            unsafe_allow_html=True,
        )
        search_agent = bulid_search_agent()
        searchResult = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["searchResult"] = extract_text(searchResult["messages"][-1].content)

        with step_placeholder.container():
            st.markdown("""
            <div class="result-card">
                <div class="result-card-header">
                    <span class="result-badge">Done</span>
                    <span class="result-card-title">🔍 Search Results</span>
                </div>
            </div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="result-card"><div class="result-card-body">{state["searchResult"]}</div></div>', unsafe_allow_html=True)

        # ── Step 2: Scrape ──
        st.session_state.current_step = 2
        status_placeholder.markdown(
            '<div class="status-bar"><div class="pulse"></div>Step 2 — Scraping deep content from sources…</div>',
            unsafe_allow_html=True,
        )
        scrapAgent = scrap_agent()
        scrapResult = scrapAgent.invoke({
            "messages": [("user",
                f"Based on the following search result about '{topic}',"
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search result:\n{state['searchResult'][:800]}")]
        })
        state["scrapResult"] = extract_text(scrapResult["messages"][-1].content)

        with step_placeholder.container():
            st.markdown(f'<div class="result-card"><div class="result-card-body">{state["scrapResult"]}</div></div>', unsafe_allow_html=True)

        # ── Step 3: Report ──
        st.session_state.current_step = 3
        status_placeholder.markdown(
            '<div class="status-bar"><div class="pulse"></div>Step 3 — Synthesising the final report…</div>',
            unsafe_allow_html=True,
        )
        combinedReport = (
            f"webResearch:{state['searchResult']}\n\n"
            f"scrapeResearch: {state['scrapResult']}"
        )
        report_result = report_chain.invoke({
            "topic": topic,
            "research": combinedReport
        })
        state["finalReport"] = extract_text(report_result)

        # ── Step 4: Critic ──
        st.session_state.current_step = 4
        status_placeholder.markdown(
            '<div class="status-bar"><div class="pulse"></div>Step 4 — Critic agent reviewing the report…</div>',
            unsafe_allow_html=True,
        )
        state["criticResult"] = extract_text(critic_chain.invoke({
            "report": state["finalReport"]
        }))

        st.session_state.results = state
        st.session_state.running = False
        st.session_state.current_step = 5  # all done
        st.rerun()

    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.running = False
        st.session_state.current_step = 0
        st.rerun()

# ── Error display ─────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"**Pipeline error:** {st.session_state.error}")
    st.caption("Make sure all dependencies are installed and your API keys are configured.")

# ── Results display ───────────────────────────────────────────────────────────
if st.session_state.results:
    state = st.session_state.results
    render_pipeline(5)

    st.markdown('<div class="status-bar">✅ &nbsp;Research complete</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Tabs for results
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Final Report", "🎯 Critic Review", "🔍 Search Data", "🕸️ Scraped Data"])

    with tab1:
        final_text = state.get("finalReport", "")
        st.markdown(f"""
        <div class="final-report-wrapper">
            <div class="final-report-header">
                <div class="final-dot"></div>
                <div class="final-report-title">Final Research Report — {topic}</div>
            </div>
            <div class="final-report-body">{final_text}</div>
        </div>""", unsafe_allow_html=True)
        st.download_button(
            label="⬇ Download Report (.txt)",
            data=final_text,
            file_name=f"deepdigest_{topic[:40].replace(' ','_')}.txt",
            mime="text/plain",
        )

    with tab2:
        critic_text = state.get("criticResult", "")
        st.markdown(f"""
        <div class="critic-wrapper">
            <div class="critic-header">
                <div class="critic-title">🎯 Critic Agent Review</div>
            </div>
            <div class="critic-body">{critic_text}</div>
        </div>""", unsafe_allow_html=True)

    with tab3:
        search_text = state.get("searchResult", "")
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-header">
                <span class="result-badge">Raw</span>
                <span class="result-card-title">Web Search Output</span>
            </div>
            <div class="result-card-body">{search_text}</div>
        </div>""", unsafe_allow_html=True)

    with tab4:
        scrap_text = state.get("scrapResult", "")
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-header">
                <span class="result-badge">Raw</span>
                <span class="result-card-title">Scraped Content</span>
            </div>
            <div class="result-card-body">{scrap_text}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    if st.button("🔄 New Research"):
        st.session_state.results = None
        st.session_state.error = None
        st.session_state.current_step = 0
        st.rerun()

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.running and not st.session_state.results and not st.session_state.error:
    render_pipeline(0)
    st.markdown("""
    <div style="text-align:center; padding: 2.5rem 1rem; color: #334155;">
        <div style="font-size: 2rem; margin-bottom: 0.75rem;">🔬</div>
        <div style="font-size: 0.85rem; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase;">
            Enter a topic above and hit Run to start the research pipeline
        </div>
    </div>
    """, unsafe_allow_html=True)