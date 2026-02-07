import streamlit as st
from mistralai import Mistral
import os
import html
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Premier Banking AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional corporate colors
PRIMARY_COLOR = "#0f172a"
SECONDARY_COLOR = "#1e3a8a"
ACCENT_COLOR = "#1d4ed8"
TEXT_COLOR = "#f1f5f9"
GOLD_COLOR = "#fbbf24"

# Professional CSS styling
st.markdown(f"""
    <style>
        * {{
            font-family: 'Segoe UI', sans-serif;
        }}
        
        .main {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            color: {TEXT_COLOR};
        }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            border-right: 3px solid {ACCENT_COLOR};
        }}
        
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
        
        .user-message {{
            background: linear-gradient(90deg, {ACCENT_COLOR}, {GOLD_COLOR});
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 0.75rem 0;
            margin-left: 2rem;
            border-left: 4px solid {GOLD_COLOR};
            box-shadow: 0 4px 12px rgba(29, 78, 216, 0.2);
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
        
        .stTextInput input {{
            background: rgba(15, 23, 42, 0.8) !important;
            color: {TEXT_COLOR} !important;
            border: 2px solid {ACCENT_COLOR} !important;
            border-radius: 10px !important;
            padding: 0.9rem 1rem !important;
        }}
        
        .stTextInput input:focus {{
            border-color: {GOLD_COLOR} !important;
            box-shadow: 0 0 12px rgba(251, 191, 36, 0.3) !important;
        }}
        
        .stButton button {{
            background: linear-gradient(90deg, {ACCENT_COLOR}, {SECONDARY_COLOR}) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.85rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 16px rgba(29, 78, 216, 0.3) !important;
        }}
        
        .stButton button:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 20px rgba(29, 78, 216, 0.4) !important;
        }}
        
        .sidebar-section {{
            background: rgba(30, 58, 138, 0.2);
            padding: 1.2rem;
            border-radius: 10px;
            margin: 1.2rem 0;
            border-left: 4px solid {ACCENT_COLOR};
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {GOLD_COLOR};
            font-weight: 700;
        }}
    </style>
""", unsafe_allow_html=True)

# Initialize Mistral client
@st.cache_resource
def get_mistral_client():
    api_key = st.secrets.get("mistral_api_key", os.getenv("MISTRAL_API_KEY", "nNKQYvoDfR3Z30ErVekiXoxClJQANBj2"))
    return Mistral(api_key=api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Good day. I am your Premier Banking AI Assistant, specializing in comprehensive financial advisory services. How may I assist you with your banking and wealth management needs today?"
        }
    ]

if "submit" not in st.session_state:
    st.session_state.submit = False

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏦 Premier Banking AI Assistant</h1>
        <p class="header-subtitle">Advanced Financial Intelligence & Strategic Advisory Services</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
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
        st.metric("Session", str(datetime.now().timestamp())[-6:])
    with col3:
        st.metric("Status", "🟢 Active")
    
    st.divider()
    
    st.markdown(f"""
        <div class="sidebar-section">
            <h3 style="color: {GOLD_COLOR}; margin-top: 0;">✨ Core Services</h3>
        </div>
    """, unsafe_allow_html=True)
    
    services = [
        ("💼 Portfolio Strategy", "Tell me about portfolio strategy and optimization"),
        ("📈 Market Intelligence", "Provide market analysis and intelligence"),
        ("💰 Wealth Management", "Discuss wealth management strategies"),
        ("🏦 Banking Solutions", "Explain banking solutions available"),
        ("📊 Investment Planning", "Help with investment planning"),
        ("🔐 Risk Assessment", "Perform risk assessment analysis")
    ]
    
    for service_name, service_prompt in services:
        if st.button(service_name, use_container_width=True, key=f"service_{service_name}"):
            st.session_state.messages.append({"role": "user", "content": service_prompt})
            st.rerun()
    
    st.divider()
    
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

# Display messages
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

st.divider()

# Input section with form for Enter key support
with st.form(key="message_form", clear_on_submit=True):
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        user_input = st.text_input(
            "Message:",
            placeholder="Type your financial question or inquiry...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.form_submit_button("Send", use_container_width=True)

# Process input
if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("💭 Analyzing your request..."):
        client = get_mistral_client()
        
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
        "1. Structure responses with clear sections using markdown formatting\n"
        "2. Provide specific, actionable insights\n"
        "3. Include relevant metrics and percentages\n"
        "4. Use professional but accessible language\n"
        "5. Break down complex strategies into clear steps\n"
        "6. Always recommend consulting certified financial advisors for critical decisions\n"
        "7. Be data-driven and fact-based\n"
        "8. Address both opportunities and risks\n"
        "9. Maintain discretion and confidentiality\n"
        "10. Maintain professional tone\n\n"
        "Provide comprehensive yet concise responses.")
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                *st.session_state.messages[:-1],
                {"role": "user", "content": user_input}
            ]
            
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            
            assistant_message = response.choices[0].message.content
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            st.rerun()
            
        except Exception as e:
            st.error(f"⚠️ Service Error: {str(e)}")
            st.session_state.messages.pop()

# Footer
st.divider()
footer = f"""<div style='text-align: center; padding: 2rem 1rem; opacity: 0.75; font-size: 0.9em; color: {TEXT_COLOR};'>
    <p style='margin: 0.5rem 0;'><strong>Premier Banking AI Assistant</strong> | Confidential | For Authorized Use Only</p>
    <p style='margin: 0.5rem 0; font-size: 0.9em;'>Advanced financial technology powered by Mistral AI</p>
    <p style='margin: 0.5rem 0; font-size: 0.85em;'>For critical financial decisions, consult with qualified professionals.</p>
    <p style='margin: 0.5rem 0; font-size: 0.85em;'>Copyright 2026 Premier Banking. All rights reserved. | hirani60@gmail.com</p>
</div>"""
st.markdown(footer, unsafe_allow_html=True)
