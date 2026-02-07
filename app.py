import streamlit as st
from mistralai import Mistral
import os
import html
from datetime import datetime

# Mobile-responsive page configuration
st.set_page_config(
    page_title="Premier Banking AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional corporate colors
PRIMARY_COLOR = "#0f172a"
SECONDARY_COLOR = "#1e3a8a"
ACCENT_COLOR = "#1d4ed8"
TEXT_COLOR = "#f1f5f9"
GOLD_COLOR = "#fbbf24"

# Responsive CSS styling with mobile support
st.markdown(f"""
    <style>
        * {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            box-sizing: border-box;
        }}
        
        html, body {{
            margin: 0;
            padding: 0;
        }}
        
        .main {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            color: {TEXT_COLOR};
            padding: 0 !important;
        }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            border-right: 3px solid {ACCENT_COLOR};
        }}
        
        .header-container {{
            background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            padding: 2rem 1.5rem;
            border-radius: 8px;
            border-bottom: 3px solid {ACCENT_COLOR};
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }}
        
        .header-title {{
            color: {GOLD_COLOR};
            font-size: clamp(1.8em, 5vw, 2.8em);
            font-weight: 700;
            margin: 0;
            letter-spacing: 0.5px;
            word-break: break-word;
        }}
        
        .header-subtitle {{
            color: {TEXT_COLOR};
            font-size: clamp(0.9em, 3vw, 1.1em);
            margin-top: 0.5rem;
            opacity: 0.95;
            font-weight: 300;
        }}
        
        .user-message {{
            background: linear-gradient(90deg, {ACCENT_COLOR}, {GOLD_COLOR});
            color: white;
            padding: clamp(0.75rem, 2vw, 1rem) clamp(1rem, 3vw, 1.5rem);
            border-radius: 8px;
            margin: 0.5rem 0;
            margin-left: clamp(0.5rem, 2vw, 2rem);
            border-left: 3px solid {GOLD_COLOR};
            box-shadow: 0 2px 8px rgba(29, 78, 216, 0.2);
            word-wrap: break-word;
            font-size: clamp(0.9em, 2vw, 1em);
        }}
        
        .assistant-message {{
            background: rgba(15, 23, 42, 0.6);
            color: {TEXT_COLOR};
            padding: clamp(0.75rem, 2vw, 1rem) clamp(1rem, 3vw, 1.5rem);
            border-radius: 8px;
            margin: 0.5rem 0;
            margin-right: clamp(0.5rem, 2vw, 2rem);
            border-left: 3px solid {ACCENT_COLOR};
            box-shadow: 0 2px 8px rgba(29, 78, 216, 0.1);
            line-height: 1.5;
            word-wrap: break-word;
            font-size: clamp(0.9em, 2vw, 1em);
        }}
        
        .stTextInput input {{
            background: rgba(15, 23, 42, 0.8) !important;
            color: {TEXT_COLOR} !important;
            border: 2px solid {ACCENT_COLOR} !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            font-size: clamp(0.95em, 2vw, 1rem) !important;
            min-height: 44px !important;
        }}
        
        .stTextInput input:focus {{
            border-color: {GOLD_COLOR} !important;
            box-shadow: 0 0 12px rgba(251, 191, 36, 0.3) !important;
        }}
        
        .stButton button {{
            background: linear-gradient(90deg, {ACCENT_COLOR}, {SECONDARY_COLOR}) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            font-weight: 700 !important;
            font-size: clamp(0.9em, 2vw, 1rem) !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3) !important;
            min-height: 44px !important;
            cursor: pointer !important;
        }}
        
        .stButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(29, 78, 216, 0.4) !important;
        }}
        
        .stButton button:active {{
            transform: translateY(0) !important;
        }}
        
        .sidebar-section {{
            background: rgba(30, 58, 138, 0.2);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 3px solid {ACCENT_COLOR};
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {GOLD_COLOR};
            font-weight: 700;
        }}
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {{
            .main {{
                padding: 0.5rem !important;
            }}
            
            .header-container {{
                padding: 1.5rem 1rem;
                margin-bottom: 1rem;
                border-radius: 6px;
            }}
            
            .user-message {{
                margin-left: 0.25rem;
                padding: 0.65rem 0.9rem;
            }}
            
            .assistant-message {{
                margin-right: 0.25rem;
                padding: 0.65rem 0.9rem;
            }}
            
            .stButton button {{
                padding: 0.65rem 0.8rem !important;
                min-height: 40px !important;
            }}
            
            .stTextInput input {{
                min-height: 40px !important;
            }}
        }}
        
        @media (max-width: 480px) {{
            .header-title {{
                font-size: 1.5em;
            }}
            
            .header-subtitle {{
                font-size: 0.85em;
            }}
            
            .user-message {{
                margin-left: 0;
                padding: 0.6rem 0.8rem;
            }}
            
            .assistant-message {{
                margin-right: 0;
                padding: 0.6rem 0.8rem;
            }}
        }}
        
        /* Form styling */
        .stForm {{
            padding: 0 !important;
        }}
        
        /* Prevent zoom on input focus (iOS) */
        input, button, select, textarea {{
            font-size: 16px !important;
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

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏦 Premier Banking AI</h1>
        <p class="header-subtitle">Financial Intelligence & Advisory Services</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with services
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-section">
            <h3 style="color: {GOLD_COLOR}; margin-top: 0;">📊 Session Info</h3>
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
            <h3 style="color: {GOLD_COLOR}; margin-top: 0;">✨ Quick Services</h3>
        </div>
    """, unsafe_allow_html=True)
    
    services = [
        ("💼 Portfolio", "Tell me about portfolio strategy and optimization"),
        ("📈 Market", "Provide market analysis and intelligence"),
        ("💰 Wealth", "Discuss wealth management strategies"),
        ("🏦 Banking", "Explain banking solutions available"),
        ("📊 Investment", "Help with investment planning"),
        ("🔐 Risk", "Perform risk assessment analysis")
    ]
    
    for service_name, service_prompt in services:
        if st.button(service_name, use_container_width=True, key=f"service_{service_name}"):
            st.session_state.messages.append({"role": "user", "content": service_prompt})
            st.rerun()
    
    st.divider()
    
    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Good day. I am your Premier Banking AI Assistant, specializing in comprehensive financial advisory services. How may I assist you with your banking and wealth management needs today?"
            }
        ]
        st.rerun()
    
    st.markdown(f"""
        <div class="sidebar-section" style="margin-top: 2rem; font-size: 0.8em;">
            <p style="opacity: 0.8; margin: 0;">
                <strong>Powered by:</strong> Mistral AI<br>
                <strong>Security:</strong> Enterprise Grade
            </p>
        </div>
    """, unsafe_allow_html=True)

# Display chat messages
st.markdown(f"<div style='padding: 0 0.5rem;'>", unsafe_allow_html=True)
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
                <strong>AI:</strong>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(escaped_content)
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# Input section with form for Enter key support
with st.form(key="message_form", clear_on_submit=True):
    col1, col2 = st.columns([0.78, 0.22])
    
    with col1:
        user_input = st.text_input(
            "Message:",
            placeholder="Ask anything...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.form_submit_button("Send", use_container_width=True)

# Process input
if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("💭 Processing..."):
        client = get_mistral_client()
        
        system_prompt = ("You are a professional financial advisor and banking specialist for institutional and high-net-worth clients.\n\n"
        "Your expertise includes: Portfolio management, Investment strategy, Banking services, Risk management, Tax-efficient wealth management, Estate planning, and International finance.\n\n"
        "RESPONSE GUIDELINES:\n"
        "1. Structure responses clearly with sections\n"
        "2. Provide specific, actionable insights\n"
        "3. Include relevant metrics and percentages\n"
        "4. Use professional but accessible language\n"
        "5. Break down complex strategies into steps\n"
        "6. Always recommend consulting certified advisors\n"
        "7. Be data-driven and fact-based\n"
        "8. Address both opportunities and risks\n"
        "9. Maintain professionalism and confidentiality\n\n"
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
            st.error(f"Service Error: {str(e)}")
            st.session_state.messages.pop()

# Footer
st.divider()
st.markdown(f"""
    <div style='text-align: center; padding: 1.5rem 0.5rem; opacity: 0.7; font-size: clamp(0.75em, 2vw, 0.85em); color: {TEXT_COLOR};'>
        <p style='margin: 0.3rem 0;'><strong>Premier Banking AI</strong> | Confidential</p>
        <p style='margin: 0.3rem 0; font-size: 0.9em;'>Advanced financial technology powered by Mistral AI</p>
        <p style='margin: 0.3rem 0; font-size: 0.9em;'>hirani60@gmail.com</p>
    </div>
""", unsafe_allow_html=True)
