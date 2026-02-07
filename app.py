import streamlit as st
from mistralai.client import MistralClient
import os
from datetime import datetime

# Set page configuration with professional styling
st.set_page_config(
    page_title="EliteBank AI Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "### EliteBank AI Assistant\nPowered by Mistral AI\nYour premier financial intelligence platform"
    }
)

# Professional color scheme for elite professionals
PRIMARY_COLOR = "#1a2332"  # Dark navy blue
SECONDARY_COLOR = "#0f3460"  # Deep blue
ACCENT_COLOR = "#e94560"  # Sophisticated red
TEXT_COLOR = "#e0e0e0"  # Light gray
GOLD_COLOR = "#d4af37"  # Executive gold

# Custom CSS for professional, elegant design
st.markdown(f"""
    <style>
        :root {{
            --primary-color: {PRIMARY_COLOR};
            --secondary-color: {SECONDARY_COLOR};
            --accent-color: {ACCENT_COLOR};
            --text-color: {TEXT_COLOR};
            --gold-color: {GOLD_COLOR};
        }}
        
        /* Main page styling */
        .main {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            color: {TEXT_COLOR};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            border-right: 2px solid {GOLD_COLOR};
        }}
        
        /* Header styling */
        .header-container {{
            background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            padding: 2rem;
            border-radius: 10px;
            border-left: 5px solid {GOLD_COLOR};
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        
        .header-title {{
            color: {GOLD_COLOR};
            font-size: 2.5em;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        
        .header-subtitle {{
            color: {TEXT_COLOR};
            font-size: 1em;
            margin-top: 0.5rem;
            opacity: 0.9;
        }}
        
        /* Chat container styling */
        .chat-container {{
            background: rgba(15, 52, 96, 0.4);
            border-radius: 10px;
            padding: 1.5rem;
            border: 1px solid {GOLD_COLOR};
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 1.5rem;
        }}
        
        /* Message styling */
        .user-message {{
            background: linear-gradient(90deg, {SECONDARY_COLOR}, {ACCENT_COLOR});
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            margin-left: 2rem;
            border-left: 4px solid {GOLD_COLOR};
            box-shadow: 0 2px 8px rgba(233, 69, 96, 0.2);
        }}
        
        .assistant-message {{
            background: rgba(26, 35, 50, 0.6);
            color: {TEXT_COLOR};
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            margin-right: 2rem;
            border-left: 4px solid {GOLD_COLOR};
            box-shadow: 0 2px 8px rgba(212, 175, 55, 0.1);
        }}
        
        /* Input styling */
        .stTextInput input {{
            background: rgba(26, 35, 50, 0.8);
            color: {TEXT_COLOR};
            border: 2px solid {GOLD_COLOR};
            border-radius: 8px;
            padding: 0.75rem;
            font-size: 1rem;
        }}
        
        .stTextInput input:focus {{
            border-color: {ACCENT_COLOR};
            box-shadow: 0 0 10px rgba(233, 69, 96, 0.3);
        }}
        
        /* Button styling */
        .stButton button {{
            background: linear-gradient(90deg, {ACCENT_COLOR}, #ff6b7a);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(233, 69, 96, 0.3);
        }}
        
        .stButton button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(233, 69, 96, 0.4);
        }}
        
        /* Sidebar section styling */
        .sidebar-section {{
            background: rgba(15, 52, 96, 0.3);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 3px solid {GOLD_COLOR};
        }}
        
        /* Info boxes */
        .info-box {{
            background: rgba(15, 52, 96, 0.3);
            border-left: 4px solid {GOLD_COLOR};
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: {TEXT_COLOR};
        }}
        
        /* Text styling */
        h1, h2, h3, h4, h5, h6 {{
            color: {GOLD_COLOR};
        }}
        
        p {{
            color: {TEXT_COLOR};
        }}
        
        /* Metric cards */
        [data-testid="stMetricValue"] {{
            color: {GOLD_COLOR};
        }}
        
        /* Divider */
        hr {{
            border-color: {GOLD_COLOR};
            opacity: 0.3;
        }}
    </style>
""", unsafe_allow_html=True)

# Initialize Mistral AI client
@st.cache_resource
def get_mistral_client():
    # Get API key from secrets (Streamlit Cloud) or environment variable
    api_key = st.secrets.get("mistral_api_key", os.getenv("MISTRAL_API_KEY", "nNKQYvoDfR3Z30ErVekiXoxClJQANBj2"))
    return MistralClient(api_key=api_key)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Good day. I am your EliteBank AI Assistant, specializing in premium financial advisory services. How may I assist you with your banking and wealth management needs today?"
        }
    ]

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏦 EliteBank AI Assistant</h1>
        <p class="header-subtitle">Premier Financial Intelligence & Advisory Services</p>
    </div>
""", unsafe_allow_html=True)

# Main layout with sidebar
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-section">
            <h3 style="color: {GOLD_COLOR};">📊 Session Overview</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Session ID", st.session_state.get("session_id", "ELITE001")[:8])
    with col3:
        st.metric("Status", "🟢 Active")
    
    st.divider()
    
    st.markdown(f"""
        <div class="sidebar-section">
            <h3 style="color: {GOLD_COLOR};">🛠️ Assistant Features</h3>
        </div>
    """, unsafe_allow_html=True)
    
    features = [
        "💼 Portfolio Management",
        "📈 Market Analysis",
        "💰 Wealth Planning",
        "🏦 Banking Services",
        "📊 Investment Strategy",
        "🔐 Risk Assessment"
    ]
    for feature in features:
        st.write(f"• {feature}")
    
    st.divider()
    
    # Clear chat button
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Good day. I am your EliteBank AI Assistant, specializing in premium financial advisory services. How may I assist you with your banking and wealth management needs today?"
            }
        ]
        st.rerun()
    
    st.markdown(f"""
        <div class="sidebar-section" style="margin-top: 2rem; border-left: 3px solid {GOLD_COLOR};">
            <p style="font-size: 0.85em; opacity: 0.8;">
                <strong>Powered by:</strong> Mistral AI Large Model<br>
                <strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
                <strong>Security Level:</strong> Enterprise Grade
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
            st.markdown(f"""
                <div class="assistant-message">
                    <strong>EliteBank AI:</strong><br>{message["content"]}
                </div>
            """, unsafe_allow_html=True)

# Chat input and processing
st.divider()

col1, col2 = st.columns([0.85, 0.15])

with col1:
    user_input = st.text_input(
        "Enter your inquiry:",
        placeholder="Ask about portfolios, investments, banking services, market analysis...",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("Send", use_container_width=True)

# Process user input
if send_button and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Show typing indicator
    with st.spinner("🤔 Analyzing your request..."):
        client = get_mistral_client()
        
        # System prompt for banking chatbot
        system_prompt = """You are an elite financial advisor and banking specialist for high-net-worth individuals and institutional clients. 
Your expertise includes:
- Portfolio management and wealth optimization
- Investment strategy and market analysis
- Banking and financial services
- Risk management and asset allocation
- Regulatory and compliance matters
- Premium banking solutions

Always provide professional, sophisticated advice with proper financial terminology. 
Maintain a professional tone appropriate for C-level executives and elite professionals.
Provide actionable insights and strategic recommendations.
When discussing sensitive financial matters, always emphasize the importance of consulting with certified financial advisors.
Your responses should be concise, insightful, and data-driven."""
        
        try:
            # Build messages list with system prompt
            messages = [
                {"role": "system", "content": system_prompt},
                *st.session_state.messages[:-1],  # Previous messages
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
            
            # Add assistant response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            st.session_state.conversation_count += 1
            st.rerun()
            
        except Exception as e:
            st.error(f"⚠️ Service Error: {str(e)}")
            # Remove the user message if API call failed
            st.session_state.messages.pop()

# Footer with professional branding
st.divider()
st.markdown(f"""
<div style="text-align: center; padding: 1.5rem; opacity: 0.7; font-size: 0.85em; color: {TEXT_COLOR};">
    <p><strong>EliteBank AI Assistant</strong> | Confidential | For Authorized Use Only</p>
    <p>This system is powered by advanced AI technology. For critical financial decisions, please consult with qualified financial professionals.</p>
    <p style="margin-top: 1rem; font-size: 0.8em;"><em>© 2026 EliteBank. All rights reserved. Enterprise Security Grade.</em></p>
    <p style="margin-top: 0.5rem; font-size: 0.8em;">📧 Contact: <strong>hirani60@gmail.com</strong></p>
</div>
""", unsafe_allow_html=True)
