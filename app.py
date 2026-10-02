import streamlit as st
import anthropic

# Page Configuration
st.set_page_config(
    page_title="Doc-Ops Workbench | Tech Writing AI Tool", 
    page_icon="📝", 
    layout="wide"
)

# Custom Styling for Portfolio Polish
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E293B; 
margin-bottom: 0px; }
    .sub-header { font-size: 1rem; color: #64748B; margin-bottom: 25px; }
    .stMetric { background-color: #F8FAFC; border: 1px solid #E2E8F0; 
padding: 12px; border-radius: 8px; }
</style>
""", unsafe_allow_html=unsafe_allow_html)

st.markdown('<div class="main-header">📝 Technical Writing Doc-Ops 
Workbench</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-assisted pre-drafting gap analysis 
& post-drafting release synthesis</div>', unsafe_allow_html=True)

# Sample Data for One-Click Portfolio Demos
SAMPLE_NOTES = """[Meeting Notes: Auth Service v2 Upgrade - Oct 2026]
Attendees: Alex (DevOps), Priya (Backend Lead), Jordan (Tech Writer)

Discussion Points:
- Upgrading OAuth2 provider to support short-lived JWT access tokens 
(15-min expiration) and refresh tokens (7-day rotation).
- Need to update endpoint POST /v2/auth/refresh.
- Priya mentioned rate limits will be enforced on login attempts. 5 failed 
attempts per IP per minute triggers HTTP 429.
- Alex working on Docker base image updates. Need to verify if breaking 
changes exist for legacy self-hosted clients.
- Open question: Who owns documenting error payloads for rate limits?
- Next release targeting next Tuesday."""

SAMPLE_JIRA = """[Resolved Tickets - Release 4.12]
- AUTH-304: Implemented rate-limiting middleware for auth endpoints (5 
attempts/min max).
- AUTH-310: Deprecated GET /v1/user/profile in favor of POST 
/v2/user/profile-details.
- AUTH-315: Added PKCE support for mobile client authorization flows.
- DOC-102: Added telemetry hooks for error tracking during token 
refresh."""

SAMPLE_GAP_OUTPUT = """### 📋 Pre-Drafting Clarification Checklist

#### 🚨 Critical Blockers
- [ ] **Error Schema:** Need exact JSON payload structure for `HTTP 429 
Too Many Requests` response.
- [ ] **Ownership:** Confirm whether Backend or DevOps maintains the error 
domain documentation.

#### ⚡ Technical Details Needed
- [ ] **Refresh Token Rotation:** Clarify behavior when a client sends an 
invalidated/expired refresh token.
- [ ] **Legacy Compatibility:** Specify explicit migration path for 
self-hosted clients affected by Docker base updates.

#### 👥 Stakeholder Sign-Offs
- [ ] **Priya (Backend):** Review rate-limiting parameters.
- [ ] **Alex (DevOps):** Verify environment variables required for token 
configuration."""

SAMPLE_RELEASE_OUTPUT = """### 📣 Executive Release Summary
Release 4.12 enhances platform security by implementing rate-limiting 
middleware across authentication endpoints and adding PKCE support for 
mobile clients. Note that `GET /v1/user/profile` is now officially 
deprecated in favor of `POST /v2/user/profile-details`.

---

### 📚 Proposed Documentation Outline
1. **Overview & Migration Notes**
   - Key changes in Authentication v2
   - Deprecation timeline for v1 endpoints
2. **API Specification**
   - `POST /v2/auth/refresh` endpoint details
   - PKCE setup guide for mobile SDKs
3. **Security & Rate Limits**
   - Rate limit thresholds (5 requests/min per IP)
   - `HTTP 429` error payload handling
4. **Troubleshooting & FAQs**"""

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    app_mode = st.radio(
        "Execution Mode",
        ["Demo Mode (Pre-loaded)", "Live Mode (Anthropic API)"],
        help="Use Demo Mode to test instantly without an API key, or Live 
Mode to call Claude 3.5 Sonnet live."
    )
    
    anthropic_key = ""
    if app_mode == "Live Mode (Anthropic API)":
        anthropic_key = st.text_input(
            "Anthropic API Key", 
            type="password", 
            help="Enter your API key starting with sk-ant-..."
        )
    
    st.markdown("---")
    st.markdown("**About This App**")
    st.caption("Built to streamline technical writer discovery workflows. 
Uses Claude 3.5 Sonnet to convert unstructured technical communications 
into actionable documentation deliverables.")

# Navigation Tabs
tab1, tab2 = st.tabs(["🔍 Pre-Drafting: Gap Analysis", "📊 Post-Drafting: 
Release Summary"])

# TAB 1: Gap Analysis
with tab1:
    st.subheader("Identify Technical Gaps in Raw Notes")
    st.write("Convert raw meeting transcripts or engineering sync notes 
into structured checklists of missing technical details.")
    
    if app_mode == "Demo Mode (Pre-loaded)":
        st.info("💡 **Demo Mode Active:** Click below to run analysis on 
sample engineering notes without an API key.")
    
    notes_input = st.text_area("Raw Engineering Notes", value=SAMPLE_NOTES 
if app_mode == "Demo Mode (Pre-loaded)" else "", height=200)
    
    if st.button("Run Gap Analysis", type="primary", key="btn_gap"):
        if app_mode == "Demo Mode (Pre-loaded)":
            st.success("Analysis Complete (Demo Output)")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Critical Gaps", "2", delta_color="inverse")
            m2.metric("Technical Items", "2")
            m3.metric("Sign-Offs Needed", "2")
            
            st.markdown(SAMPLE_GAP_OUTPUT)
            st.download_button(
                label="📥 Download Checklist (.md)",
                data=SAMPLE_GAP_OUTPUT,
                file_name="gap_analysis_checklist.md",
                mime="text/markdown"
            )
        else:
            if not notes_input:
                st.warning("Please enter meeting notes to analyze.")
            elif not anthropic_key:
                st.warning("Please enter your Anthropic API Key in the 
sidebar.")
            else:
                with st.spinner("Claude is analyzing notes for technical 
gaps..."):
                    try:
                        client = 
anthropic.Anthropic(api_key=anthropic_key)
                        prompt = f"""You are an expert senior technical 
writer. Analyze these engineering meeting notes and output a crisp 
Markdown checklist categorizing missing technical details, unspecified API 
schemas, edge cases, and required stakeholder sign-offs:

{notes_input}"""
                        
                        response = client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1000,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        
                        output_text = response.content[0].text
                        st.success("Analysis Complete!")
                        st.markdown(output_text)
                        
                        st.download_button(
                            label="📥 Download Checklist (.md)",
                            data=output_text,
                            file_name="gap_analysis_checklist.md",
                            mime="text/markdown"
                        )
                    except Exception as e:
                        st.error(f"Error executing request: {e}")

# TAB 2: Release Synthesis
with tab2:
    st.subheader("Generate Release Summaries & Doc Outlines")
    st.write("Synthesize completed Jira tickets and release specs into 
executive updates and structured documentation outlines.")
    
    if app_mode == "Demo Mode (Pre-loaded)":
        st.info("💡 **Demo Mode Active:** Click below to generate a 
release summary from sample specs without an API key.")
    
    jira_input = st.text_area("Resolved Jira Tickets / Release Specs", 
value=SAMPLE_JIRA if app_mode == "Demo Mode (Pre-loaded)" else "", 
height=200)
    
    if st.button("Generate Summary & Outline", type="primary", 
key="btn_rel"):
        if app_mode == "Demo Mode (Pre-loaded)":
            st.success("Synthesis Complete (Demo Output)")
            st.markdown(SAMPLE_RELEASE_OUTPUT)
            
            st.download_button(
                label="📥 Download Summary & Outline (.md)",
                data=SAMPLE_RELEASE_OUTPUT,
                file_name="release_summary_and_outline.md",
                mime="text/markdown"
            )
        else:
            if not jira_input:
                st.warning("Please enter release specs or Jira details.")
            elif not anthropic_key:
                st.warning("Please enter your Anthropic API Key in the 
sidebar.")
            else:
                with st.spinner("Claude is synthesizing release 
notes..."):
                    try:
                        client = 
anthropic.Anthropic(api_key=anthropic_key)
                        prompt = f"""You are an expert technical writer. 
Synthesize these feature specs/Jira summaries into two clean markdown 
sections:
1. Executive Release Summary (a high-level executive overview for internal 
stakeholders)
2. Proposed Documentation Outline (a detailed numbered outline for 
end-user documentation)

{jira_input}"""
                        
                        response = client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1000,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        
                        output_text = response.content[0].text
                        st.success("Synthesis Complete!")
                        st.markdown(output_text)
                        
                        st.download_button(
                            label="📥 Download Summary & Outline (.md)",
                            data=output_text,
                            file_name="release_summary_and_outline.md",
                            mime="text/markdown"
                        )
                    except Exception as e:
                        st.error(f"Error executing request: {e}")
