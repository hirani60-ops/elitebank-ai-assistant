import streamlit as st
from mistralai import Mistral
import os
import html
from datetime import datetime

# Set page configuration with professional styling
st.set_page_config(
    page_title="Premier Banking AI Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "### Premier Banking AI Assistant\nPowered by Mistral AI\nYour premier financial intelligence platform"
    }
)

# Professional color scheme - Corporate Banking
PRIMARY_COLOR = "#0f172a"      # Dark navy blue
SECONDARY_COLOR = "#1e3a8a"    # Professional blue
ACCENT_COLOR = "#1d4ed8"       # Corporate blue
TEXT_COLOR = "#f1f5f9"         # Light text
GOLD_COLOR = "#fbbf24"         # Professional gold

# Custom CSS for professional, elegant design
st.markdown(f"""
    <style>
        * {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Main page styling */
        .main {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            color: {TEXT_COLOR};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            border-right: 3px solid {ACCENT_COLOR};
        }}
        
        /* Header styling */
        .header-container {{
            background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            padding: 3rem 2rem;
            border-radius: 12px;
            border-bottom: 3px solid {ACCENT_COLOR};
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }}
        
        .header-title {{
            color: {GOLD_COLOR};
            font-size: 2.8em;
            font-weight: 700;
            margin: 0;
            letter-spacing: 0.5px;
        }}
        
        .header-subtitle {{
            color: {TEXT_COLOR};
            font-size: 1.1em;
            margin-top: 0.8rem;
            opacity: 0.95;
            font-weight: 300;
        }}
        
        /* Chat container styling */
        .chat-container {{
            background: rgba(30, 58, 138, 0.3);
            border-radius: 12px;
            padding: 2rem;
            border: 1px solid {ACCENT_COLOR};
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            margin-bottom: 1.5rem;
        }}
        
        /* Message styling */
        .user-message {{
            background: linear-gradient(90deg, {ACCENT_COLOR}, {GOLD_COLOR});
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 0.75rem 0;
            margin-left: 2rem;
            border-left: 4px solid {GOLD_COLOR};
            box-shadow: 0 4px 12px rgba(29, 78, 216, 0.2);
            word-wrap: break-word;
        }}
        
        .assistant-message {{
            background: rgba(15, 23, 42, 0.6);
            color: {TEXT_COLOR};
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 0.75rem 0;
            margin-right: 2rem;
            border-left: 4px solid {ACCENT_COLOR};
            box-shadow: 0 4px 12px rgba(29, 78, 216, 0.1);
            line-height: 1.6;
        }}
        
        /* Input styling */
        .stTextInput input {{
            background: rgba(15, 23, 42, 0.8);
            color: {TEXT_COLOR};
            border: 2px solid {ACCENT_COLOR};
            border-radius: 10px;
            padding: 0.9rem 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }}
        
        .stTextInput input:focus {{
            border-color: {GOLD_COLOR};
            box-shadow: 0 0 12px rgba(251, 191, 36, 0.3);
            background: rgba(15, 23, 42, 0.95);
        }}
        
        .stTextInput input::placeholder {{
            color: {TEXT_COLOR};
            opacity: 0.6;
        }}
        
        /* Button styling */
        .stButton button {{
            background: linear-gradient(90deg, {ACCENT_COLOR}, {SECONDARY_COLOR});
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.85rem 2rem;
            font-weight: 700;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 6px 16px rgba(29, 78, 216, 0.3);
            letter-spacing: 0.5px;
        }}
        
        .stButton button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(29, 78, 216, 0.4);
            background: linear-gradient(90deg, {SECONDARY_COLOR}, {ACCENT_COLOR});
        }}
        
        .stButton button:active {{
            transform: translateY(-1px);
        }}
        
        /* Sidebar section styling */
        .sidebar-section {{
            background: rgba(30, 58, 138, 0.2);
            padding: 1.2rem;
            border-radius: 10px;
            margin: 1.2rem 0;
            border-left: 4px solid {ACCENT_COLOR};
        }}
        
        /* Metric cards */
        [data-testid="stMetricValue"] {{
            color: {GOLD_COLOR};
            font-size: 1.8em;
            font-weight: 700;
        }}
        
        /* Text styling */
        h1, h2, h3, h4, h5, h6 {{
            color: {GOLD_COLOR};
            font-weight: 700;
            letter-spacing: 0.3px;
        }}
        
        p {{
            color: {TEXT_COLOR};
            font-weight: 400;
        }}
        
        /* Divider */
        hr {{
            border-color: {ACCENT_COLOR};
            opacity: 0.3;
            margin: 2rem 0;
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {PRIMARY_COLOR};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {ACCENT_COLOR};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {GOLD_COLOR};
        }}
    </style>
""", unsafe_allow_html=True)

# Initialize Mistral AI client
@st.cache_resource
def get_mistral_client():
    api_key = st.secrets.get("mistral_api_key", os.getenv("MISTRAL_API_KEY", "nNKQYvoDfR3Z30ErVekiXoxClJQANBj2"))
    return Mistral(api_key=api_key)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Good day. I am your Premier Banking AI Assistant, specializing in comprehensive financial advisory services. How may I assist you with your banking and wealth management needs today?"
        }
    ]

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

if "user_input_key" not in st.session_state:
    st.session_state.user_input_key = 0

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏦 Premier Banking AI Assistant</h1>
        <p class="header-subtitle">Advanced Financial Intelligence & Strategic Advisory Services</p>
    </div>
""", unsafe_allow_html=True)

# Main layout with sidebar
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-section">
            <h3 style="color: {GOLD_COLOR}; margin-top: 0;">📊 Session Analytics</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        session_num = str(datetime.now().timestamp())[-6:]
        st.metric("Session", session_num)
    with col3:
        st.metric("Status", "🟢 Active")
    
    st.divider()
    
    st.markdown(f"""
        <div class="sidebar-section">
            <h3 style="color: {GOLD_COLOR}; margin-top: 0;">✨ Core Services</h3>
        </div>
    """, unsafe_allow_html=True)
    
    services = [
        "💼 Portfolio Strategy",
        "📈 Market Intelligence",
        "💰 Wealth Management",
        "🏦 Banking Solutions",
        "📊 Investment Planning",
        "🔐 Risk Assessment"
    ]
    for service in services:
        st.write(f"• {service}")
    
    st.divider()
    
    # Clear chat button
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Good day. I am your Premier Banking AI Assistant, specializing in comprehensive financial advisory services. How may I assist you with your banking and wealth management needs today?"
            }
        ]
        st.rerun()
    
    st.markdown(f"""
        <div class="sidebar-section" style="margin-top: 2rem;">
            <p style="font-size: 0.85em; opacity: 0.85; margin: 0;">
                <strong>Technology:</strong> Mistral AI<br>
                <strong>Model:</strong> Large Language Model<br>
                <strong>Updated:</strong> {datetime.now().strftime('%B %d, %Y')}<br>
                <strong>Security:</strong> Enterprise Grade
            </p>
        </div>
    """, unsafe_allow_html=True)

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong><br>{message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            escaped_content = html.escape(message["content"])
            st.markdown(f"""
                <div class="assistant-message">
                    <strong>Banking AI Assistant:</strong>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(escaped_content)

# Chat input and processing
st.divider()

col1, col2 = st.columns([0.85, 0.15])

with col1:
    user_input = st.text_input(
        "Message:",
        placeholder="Type your financial question or inquiry...",
        label_visibility="collapsed",
        key=f"user_input_{st.session_state.user_input_key}"
    )

with col2:
    send_button = st.button("Send", use_container_width=True, key="send_btn")

# Process user input (both button click and Enter key)
if (send_button or user_input) and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Show typing indicator
    with st.spinner("💭 Analyzing your request..."):
        client = get_mistral_client()
        
        # Professional system prompt
        system_prompt = ("You are a professional financial advisor and banking specialist for institutional and high-net-worth clients.\n\n"
        "Your expertise includes:\n"
        "- Portfolio management and wealth optimization\n"
        "- Investment strategy and market analysis\n"
        "- Banking and financial services\n"
        "- Risk management and asset allocation\n"
        "- Regulatory and compliance matters\n"
        "- Premium banking solutions\n"
        "- Tax-efficient wealth management\n"
        "- Estate planning and succession strategies\n"
        "- International finance and multi-currency management\n\n"
        "RESPONSE GUIDELINES:\n"
        "1. Structure responses with clear sections using markdown formatting (##, bullet points, numbered lists)\n"
        "2. Provide specific, actionable insights backed by financial principles\n"
        "3. Include relevant metrics, percentages, or ranges when applicable\n"
        "4. Use professional but accessible language\n"
        "5. For complex strategies, break down into clear steps\n"
        "6. Always emphasize consulting with certified financial advisors for critical decisions\n"
        "7. Be data-driven and fact-based in all recommendations\n"
        "8. Address both opportunities and risks comprehensively\n"
        "9. Maintain discretion and confidentiality\n"
        "10. Maintain professional tone appropriate for institutional clients\n\n"
        "Provide comprehensive yet concise responses directly relevant to the inquiry.")
        
        try:
            # Build messages list
            messages = [
                {"role": "system", "content": system_prompt},
                *st.session_state.messages[:-1],
                {"role": "user", "content": user_input}
            ]
            
            # Call Mistral AI API
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            st.session_state.conversation_count += 1
            st.session_state.user_input_key += 1
            st.rerun()
            
        except Exception as e:
            st.error(f"⚠️ Service Error: {str(e)}")
            st.session_state.messages.pop()

# Professional footer
st.divider()
footer_content = f"""<div style='text-align: center; padding: 2rem 1rem; opacity: 0.75; font-size: 0.9em; color: {TEXT_COLOR};'>
    <p style='margin: 0.5rem 0;'><strong>Premier Banking AI Assistant</strong> | Confidential | For Authorized Use Only</p>
    <p style='margin: 0.5rem 0; font-size: 0.9em;'>Advanced financial technology powered by Mistral AI</p>
    <p style='margin: 0.5rem 0; font-size: 0.85em;'>For critical financial decisions, please consult with qualified financial professionals.</p>
    <p style='margin: 0.5rem 0; font-size: 0.85em;'>Copyright 2026 Premier Banking. All rights reserved. | Contact: hirani60@gmail.com</p>
</div>"""
st.markdown(footer_content, unsafe_allow_html=True)
