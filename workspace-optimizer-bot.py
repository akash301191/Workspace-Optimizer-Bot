import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_workspace_setup_preferences():
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Column 1: Image Upload
    with col1:
        st.subheader("📸 Upload Workspace Photo")
        uploaded_image = st.file_uploader(
            "Upload a photo of your current workspace setup",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Ergonomic Preferences
    with col2:
        st.subheader("🪑 Ergonomic Preferences")

        focus_area = st.selectbox(
            "What would you like to focus on?",
            ["Posture Correction", "Desk Organization", "Full Ergonomic Assessment"]
        )

        improvement_goal = st.selectbox(
            "What's your primary improvement goal?",
            ["Reduce Strain", "Boost Productivity", "Create a Calmer Space", "Maximize Space Efficiency"]
        )

    return {
        "uploaded_image": uploaded_image,
        "focus_area": focus_area,
        "improvement_goal": improvement_goal
    }

def generate_workspace_report(user_workspace_preferences: dict):
    # Save uploaded image to a temporary file
    uploaded_image = user_workspace_preferences["uploaded_image"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    focus_area = user_workspace_preferences["focus_area"]
    improvement_goal = user_workspace_preferences["improvement_goal"]

    # Agent 1: Posture & Setup Analyzer
    posture_analyzer_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Posture & Setup Analyzer",
        role="Analyzes your workspace image to detect posture risks and ergonomic flaws.",
        description="Examines monitor height, chair position, hand placement, and general setup.",
        instructions=[
            "Study the uploaded desk setup photo.",
            "Identify ergonomic risks: slouched seating, low monitor, awkward arm positioning, cluttered workspace, etc.",
            "Provide findings using this format:\n\n"
            "### 🔍 Detected Ergonomic Issues\n\n"
            "| Area | Concern |\n|------|---------|\n| ... | ... |"
        ],
        markdown=True
    )
    posture_response = posture_analyzer_agent.run(
        "Analyze the desk image and report ergonomic issues.", 
        images=[Image(filepath=image_path)]
    )
    issue_section = posture_response.content

    # Agent 2: Ergonomic Risk Evaluator
    risk_evaluator_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Ergonomic Risk Evaluator",
        role="Assesses severity of ergonomic risks and prioritizes fixes.",
        description="Determines the physical toll and urgency of setup problems.",
        instructions=[
            "Review the identified ergonomic issues.",
            "Explain how each might affect physical health or productivity over time.",
            "Use markdown with the heading:\n\n"
            "### ⚠️ Risk Assessment & Priorities"
        ],
        markdown=True
    )
    risk_response = risk_evaluator_agent.run(issue_section)
    risk_section = risk_response.content

    # Agent 3: Fix Advisor
    fix_advisor_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Fix Advisor",
        role="Recommends specific changes based on posture and workspace issues.",
        description="Gives step-by-step advice to improve posture and ergonomics.",
        instructions=[
            "Using the analysis and user's selected focus/improvement goal, suggest step-by-step ergonomic fixes.",
            "Include actionable, low-cost and high-impact tips.",
            "Use the format:\n\n"
            "### 🛠️ Recommended Fixes\n\n"
            "- Adjust chair height to...\n- Reposition monitor to...\n- Add wrist support to..."
        ],
        markdown=True
    )
    fix_prompt = f"{issue_section}\n\nFocus: {focus_area}\nGoal: {improvement_goal}"
    fix_response = fix_advisor_agent.run(fix_prompt)
    fix_section = fix_response.content

    # Agent 4: Product Finder
    product_finder_agent = Agent(
        name="Workspace Product Finder",
        role="Finds relevant ergonomic products to enhance your workspace setup.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You recommend ergonomic accessories based on the user's desk setup issues and preferences.
            Include practical accessories such as monitor risers, footrests, wrist pads, lumbar cushions, etc.
        """),
        instructions=[
            "Based on the posture issues and ergonomic improvement goals, recommend 8–10 product links.",
            "Use `search_google` for real product URLs.",
            "Only include actual product links, no blogs or reviews.",
            "Format:\n\n"
            "### 🛍️ Product Recommendations\n\n"
            "> *Suggested tools to optimize your setup:*\n\n"
            "- [Footrest Cushion](https://example.com)\n- [Monitor Riser](https://example.com)"
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
        markdown=True
    )
    product_response = product_finder_agent.run(fix_prompt)
    product_section = product_response.content

    # Final remarks
    summary_comment = (
        "### 💬 Ergonomic Summary\n\n"
        "> “Your workspace has great potential. With just a few adjustments, you can improve posture, reduce fatigue, and make your setup truly ergonomic.”\n"
    )

    # Combine sections into a full report
    final_report = (
        "## 🪑 Workspace Optimization Report\n\n"
        f"{issue_section}\n\n---\n\n"
        f"{risk_section}\n\n---\n\n"
        f"{fix_section}\n\n---\n\n"
        f"{product_section}\n\n---\n\n"
        f"{summary_comment}"
    )

    return final_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Workspace Optimizer Bot", page_icon="🪑", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🪑 Workspace Optimizer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Workspace Optimizer Bot — a practical Streamlit assistant that scans your desk setup to detect alignment and posture issues, and guides you with actionable ergonomic tips and workspace enhancement products.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_workspace_preferences = render_workspace_setup_preferences()
    
    st.markdown("---")

    # UI button to trigger workspace optimization report generation
    if st.button("🪑 Generate Workspace Optimization Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        elif not user_workspace_preferences["uploaded_image"]:
            st.error("Please upload a workspace photo to proceed.")
        else:
            with st.spinner("Analyzing your workspace and preparing your ergonomic report..."):
                workspace_report = generate_workspace_report(user_workspace_preferences)

                # Save results to session state
                st.session_state.workspace_report = workspace_report
                st.session_state.uploaded_image = user_workspace_preferences["uploaded_image"]

    # Display result if available
    if "workspace_report" in st.session_state and "uploaded_image" in st.session_state:
        st.markdown("## 🖼️ Uploaded Workspace Photo")
        st.image(st.session_state.uploaded_image, use_container_width=False)

        st.markdown(st.session_state.workspace_report, unsafe_allow_html=True)

        st.markdown("---")

        st.download_button(
            label="📥 Download Workspace Report",
            data=st.session_state.workspace_report,
            file_name="workspace_optimization_report.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()