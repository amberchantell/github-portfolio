import streamlit as st
import anthropic

st.set_page_config(
    page_title="Doc-Ops Workbench | Amber Rogers", 
    page_icon="📝", 
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #FAFAFA; }
    .main-header { font-size: 2.3rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em; margin-bottom: 4px; }
    .sub-header { font-size: 1.05rem; color: #64748B; font-weight: 400; margin-bottom: 20px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700; color: #1E293B; }
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    .ui-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
    }
    .badge-demo {
        background-color: #EEF2FF;
        color: #4338CA;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #C7D2FE;
        display: inline-block;
        margin-bottom: 12px;
    }
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 16px;
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border: none !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #4338CA !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class=\"main-header\">📝 Technical Writing Doc-Ops Workbench</div>", unsafe_allow_html=True)
st.markdown("<div class=\"sub-header\">AI-assisted gap analysis, release summaries, and doc change impact audits</div>", unsafe_allow_html=True)

with st.expander("💡 Why I Built This Workbench"):
    st.markdown("""
    In technical writing across hardware and software ecosystems, **discovery friction and doc maintenance** are major bottlenecks to on-time releases. 
    Writers spend hours parsing ambiguous sync transcripts, hunting down unassigned API schemas, or manually auditing existing guides when engineering changes occur. 
    
    I created this workbench to automate **pre-drafting gap analysis**, **release note drafting**, and **doc change impact audits**, enabling writers to focus on high-impact technical deliverable design.
    """)

SAMPLE_NOTES = """[Meeting Notes: Auth Service v2 Upgrade]
Attendees: Alex (DevOps), Priya (Backend Lead), Jordan (Tech Writer)

Discussion Points:
- Upgrading OAuth2 provider to support short-lived JWT access tokens (15-min expiration) and refresh tokens (7-day rotation).
- Need to update endpoint POST /v2/auth/refresh.
- Priya mentioned rate limits will be enforced on login attempts. 5 failed attempts per IP per minute triggers HTTP 429.
- Alex working on Docker base image updates. Need to verify if breaking changes exist for legacy self-hosted clients.
- Open question: Who owns documenting error payloads for rate limits?
- Next release targeting next Tuesday."""

SAMPLE_JIRA = """[Resolved Tickets - Release 4.12]
- AUTH-304: Implemented rate-limiting middleware for auth endpoints (5 attempts/min max).
- AUTH-310: Deprecated GET /v1/user/profile in favor of POST /v2/user/profile-details.
- AUTH-315: Added PKCE support for mobile client authorization flows.
- DOC-102: Added telemetry hooks for error tracking during token refresh."""

SAMPLE_EXISTING_DOC = """# User Profile & Auth API Reference

## Authentication Overview
Clients authenticate using bearer tokens obtained from `POST /v1/auth/login`. Tokens remain valid for 24 hours.

## User Endpoints
### Get User Profile
`GET /v1/user/profile`
Returns the user's profile details including email, full name, and assigned permissions.

### Rate Limits
There are currently no enforced rate limits on authentication attempts, but client applications are expected to back off on 5xx errors."""

SAMPLE_CHANGELOG = """- Deprecated GET /v1/user/profile; replaced with POST /v2/user/profile-details.
- Access token lifespan reduced from 24 hours to 15 minutes with 7-day refresh token rotation.
- Rate limiting added: 5 failed attempts per IP per minute yields HTTP 429."""

SAMPLE_GAP_OUTPUT = """### 📋 Pre-Drafting Clarification Checklist

#### 🚨 Critical Blockers
- [ ] **Error Schema:** Need exact JSON payload structure for `HTTP 429 Too Many Requests` response.
- [ ] **Ownership:** Confirm whether Backend or DevOps maintains the error domain documentation.

#### ⚡ Technical Details Needed
- [ ] **Refresh Token Rotation:** Clarify behavior when a client sends an invalidated/expired refresh token.
- [ ] **Legacy Compatibility:** Specify explicit migration path for self-hosted clients affected by Docker base updates.

#### 👥 Stakeholder Sign-Offs
- [ ] **Priya (Backend):** Review rate-limiting parameters.
- [ ] **Alex (DevOps):** Verify environment variables required for token configuration."""

SAMPLE_RELEASE_OUTPUT = """### 📣 Executive Release Summary
Release 4.12 enhances platform security by implementing rate-limiting middleware across authentication endpoints and adding PKCE support for mobile clients. Note that `GET /v1/user/profile` is now officially deprecated in favor of `POST /v2/user/profile-details`.

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

SAMPLE_IMPACT_OUTPUT = """### 🔄 Impact & Change Analysis Report

#### ⚠ Outdated Sections Identified
1. **Token Lifespan:** Existing doc specifies 24-hour token validity. Update to 15-minute access tokens + 7-day refresh token rotation.
2. **Deprecated Endpoint:** `GET /v1/user/profile` is deprecated. Replace reference with `POST /v2/user/profile-details`.
3. **Rate Limits:** Section states "no enforced rate limits". Update with 5 attempts/min per IP threshold and HTTP 429 error behavior.

---

#### ✏️ Proposed Document Revisions

```markdown
## Authentication Overview
Clients authenticate using short-lived JWT access tokens (15-minute expiration) obtained via `POST /v2/auth/refresh` alongside a 7-day refresh token rotation policy.

## User Endpoints
### Get Profile Details (v2)
`POST /v2/user/profile-details`
*Note: `GET /v1/user/profile` is deprecated.* Returns user profile details, including email, full name, and permissions.

### Rate Limits
Authentication attempts are rate-limited to **5 failed attempts per IP per minute**. Exceeding this limit returns an `HTTP 429 Too Many Requests` status code.
```"""

with st.sidebar:
    st.header("⚙️ Configuration")
    
    app_mode = st.radio(
        "Execution Mode",
        ["Demo Mode (Pre-loaded)", "Live Mode (Anthropic API)"],
        help="Use Demo Mode to test instantly without an API key, or Live Mode to call Claude live."
    )
    
    style_guide = st.selectbox(
        "Documentation Style Guide Rule",
        ["Standard Technical Writing", "Google Developer Documentation Style", "Microsoft Writing Style Guide"],
        help="Instructs Claude to tailor recommendations to specific organizational style guidelines."
    )
    
    export_format = st.selectbox(
        "Output Format",
        ["Markdown (.md)", "Jira Markup (.txt)"],
        help="Select output formatting dialect."
    )
    
    anthropic_key = ""
    if app_mode == "Live Mode (Anthropic API)":
        anthropic_key = st.text_input("Anthropic API Key", type="password", help="Enter your API key starting with sk-ant-...")
    
    st.markdown("---")
    st.markdown("### 👩‍💻 Built by Amber Rogers")
    st.caption("Senior Technical Writer and DocOps Advocate specializing in hardware and software documentation, API reference development, and AI-driven workflow integration.")
    st.markdown("[🔗 LinkedIn Profile](https://www.linkedin.com/in/ambercrogers/) | [🐙 GitHub Portfolio](https://github.com/amberchantell)")

tab1, tab2, tab3 = st.tabs([
    "🔍 Pre-Drafting: Gap Analysis", 
    "📊 Release Summaries & Outlines", 
    "🔄 Impact & Change Analysis"
])

# TAB 1: GAP ANALYSIS
with tab1:
    st.subheader("Identify Technical Gaps in Raw Notes")
    st.write("Convert raw meeting transcripts or engineering sync notes into structured checklists of missing technical details.")
    
    if app_mode == "Demo Mode (Pre-loaded)":
        st.markdown(f"<div class=\"badge-demo\">⚡ Demo Mode Active • Style: {style_guide} • Format: {export_format}</div>", unsafe_allow_html=True)
    
    notes_input = st.text_area("Raw Engineering Notes", value=SAMPLE_NOTES if app_mode == "Demo Mode (Pre-loaded)" else "", height=200)
    
    if st.button("Run Gap Analysis", type="primary", key="btn_gap"):
        if app_mode == "Demo Mode (Pre-loaded)":
            st.success("Analysis Complete (Demo Output)")
            m1, m2, m3 = st.columns(3)
            m1.metric("Critical Gaps", "2")
            m2.metric("Technical Items", "2")
            m3.metric("Sign-Offs Needed", "2")
            
            st.markdown("<div class=\"ui-card\">", unsafe_allow_html=True)
            st.markdown(SAMPLE_GAP_OUTPUT)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Checklist",
                data=SAMPLE_GAP_OUTPUT,
                file_name="gap_analysis_checklist.md" if export_format == "Markdown (.md)" else "gap_analysis_checklist.txt",
                mime="text/plain"
            )
        else:
            if not notes_input:
                st.warning("Please enter meeting notes to analyze.")
            elif not anthropic_key:
                st.warning("Please enter your Anthropic API Key in the sidebar.")
            else:
                with st.spinner("Claude is analyzing notes for technical gaps..."):
                    try:
                        client = anthropic.Anthropic(api_key=anthropic_key)
                        prompt = f"You are an expert senior technical writer adhering strictly to the {style_guide}. Analyze these engineering meeting notes and output a crisp checklist categorizing missing technical details, unspecified API schemas, edge cases, and required stakeholder sign-offs. Format output using {export_format}:\n\n{notes_input}"
                        response = client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1000,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        output_text = response.content[0].text
                        st.success("Analysis Complete!")
                        
                        st.markdown("<div class=\"ui-card\">", unsafe_allow_html=True)
                        st.markdown(output_text)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.download_button(
                            label="📥 Download Checklist",
                            data=output_text,
                            file_name="gap_analysis_checklist.md" if export_format == "Markdown (.md)" else "gap_analysis_checklist.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error executing request: {e}")

# TAB 2: RELEASE SUMMARIES
with tab2:
    st.subheader("Generate Release Summaries & Doc Outlines")
    st.write("Synthesize completed Jira tickets and release specs into executive updates and structured documentation outlines.")
    
    if app_mode == "Demo Mode (Pre-loaded)":
        st.markdown(f"<div class=\"badge-demo\">⚡ Demo Mode Active • Style: {style_guide} • Format: {export_format}</div>", unsafe_allow_html=True)
    
    jira_input = st.text_area("Resolved Jira Tickets / Release Specs", value=SAMPLE_JIRA if app_mode == "Demo Mode (Pre-loaded)" else "", height=200)
    
    if st.button("Generate Summary & Outline", type="primary", key="btn_rel"):
        if app_mode == "Demo Mode (Pre-loaded)":
            st.success("Synthesis Complete (Demo Output)")
            
            st.markdown("<div class=\"ui-card\">", unsafe_allow_html=True)
            st.markdown(SAMPLE_RELEASE_OUTPUT)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Summary & Outline",
                data=SAMPLE_RELEASE_OUTPUT,
                file_name="release_summary.md" if export_format == "Markdown (.md)" else "release_summary.txt",
                mime="text/plain"
            )
        else:
            if not jira_input:
                st.warning("Please enter release specs or Jira details.")
            elif not anthropic_key:
                st.warning("Please enter your Anthropic API Key in the sidebar.")
            else:
                with st.spinner("Claude is synthesizing release notes..."):
                    try:
                        client = anthropic.Anthropic(api_key=anthropic_key)
                        prompt = f"You are an expert technical writer adhering strictly to the {style_guide}. Synthesize these feature specs/Jira summaries into two sections using {export_format}:\n1. Executive Release Summary\n2. Proposed Documentation Outline\n\n{jira_input}"
                        response = client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1000,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        output_text = response.content[0].text
                        st.success("Synthesis Complete!")
                        
                        st.markdown("<div class=\"ui-card\">", unsafe_allow_html=True)
                        st.markdown(output_text)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.download_button(
                            label="📥 Download Summary & Outline",
                            data=output_text,
                            file_name="release_summary.md" if export_format == "Markdown (.md)" else "release_summary.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error executing request: {e}")

# TAB 3: IMPACT & CHANGE ANALYSIS
with tab3:
    st.subheader("Document Audit & Update Assistant")
    st.write("Compare new engineering changes against existing documentation to pinpoint outdated sections and draft updated content.")
    
    if app_mode == "Demo Mode (Pre-loaded)":
        st.markdown(f"<div class=\"badge-demo\">⚡ Demo Mode Active • Style: {style_guide} • Format: {export_format}</div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        doc_input = st.text_area("Existing Documentation", value=SAMPLE_EXISTING_DOC if app_mode == "Demo Mode (Pre-loaded)" else "", height=220)
    with col_b:
        change_input = st.text_area("Engineering Changes / Changelog", value=SAMPLE_CHANGELOG if app_mode == "Demo Mode (Pre-loaded)" else "", height=220)
    
    if st.button("Analyze Documentation Impact", type="primary", key="btn_impact"):
        if app_mode == "Demo Mode (Pre-loaded)":
            st.success("Audit Complete (Demo Output)")
            
            st.markdown("<div class=\"ui-card\">", unsafe_allow_html=True)
            st.markdown(SAMPLE_IMPACT_OUTPUT)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Audit & Proposed Edits",
                data=SAMPLE_IMPACT_OUTPUT,
                file_name="doc_impact_report.md" if export_format == "Markdown (.md)" else "doc_impact_report.txt",
                mime="text/plain"
            )
        else:
            if not doc_input or not change_input:
                st.warning("Please provide both existing documentation and engineering changes.")
            elif not anthropic_key:
                st.warning("Please enter your Anthropic API Key in the sidebar.")
            else:
                with st.spinner("Claude is auditing documentation for required updates..."):
                    try:
                        client = anthropic.Anthropic(api_key=anthropic_key)
                        prompt = f"You are an expert technical writer adhering strictly to the {style_guide}. Audit the existing documentation against the provided engineering changes. Format output using {export_format}:\n\n1. Outdated Sections Identified\n2. Proposed Document Revisions\n\nEXISTING DOCUMENTATION:\n{doc_input}\n\nENGINEERING CHANGES:\n{change_input}"
                        response = client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1200,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        output_text = response.content[0].text
                        st.success("Audit Complete!")
                        
                        st.markdown("<div class=\"ui-card\">", unsafe_allow_html=True)
                        st.markdown(output_text)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.download_button(
                            label="📥 Download Audit & Proposed Edits",
                            data=output_text,
                            file_name="doc_impact_report.md" if export_format == "Markdown (.md)" else "doc_impact_report.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error executing request: {e}")

st.markdown("---")
st.markdown(
    "<div style=\"text-align: center; color: #64748B; font-size: 0.85rem; padding-bottom: 20px;\">"
    "Technical Writing Doc-Ops Workbench • Engineered by <b>Amber Rogers</b> • Powered by Claude"
    "</div>",
    unsafe_allow_html=True
)
