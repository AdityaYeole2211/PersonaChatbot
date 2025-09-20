from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import random
from prompt import BIGB_SYSTEM_PROMPT


load_dotenv()
#streamlit pagr config
st.set_page_config(
    page_title="Amitabh Bachchan AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# SOME CSS 

# Custom CSS for dark theme and animations
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #f59e0b;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --border-color: #334155;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit header and footer */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .stApp > footer {
        display: none;
    }
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
        animation: slideDown 0.8s ease-out;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Chat container */
    .chat-container {
        background: var(--bg-card);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        animation: fadeInUp 0.6s ease-out;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Message styles */
    .user_message {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        animation: slideInRight 0.5s ease-out;
        font-weight: 500;
        word-wrap: break-word;
    }
    
    .ai_message {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 85%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        animation: slideInLeft 0.5s ease-out;
        line-height: 1.6;
        word-wrap: break-word;
    }
    
    .ai_message::before {
        content: "👨‍💻 Amitabh Bachchan";
        display: block;
        font-weight: 600;
        color: var(--accent-color);
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Stats cards */
    .stats-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Quote section */
    .quote-section {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
        border-left: 4px solid var(--primary-color);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem 0;
        animation: fadeIn 1s ease-out;
    }
    
    .quote-text {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-style: italic;
        line-height: 1.6;
    }
    
    .quote-author {
        color: var(--text-secondary);
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Welcome message */
    .welcome-message {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: var(--text-secondary);
        margin: 2rem 0;
        animation: fadeIn 1.2s ease-out;
    }
    
    .welcome-message h3 {
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    /* Animations */
    @keyframes slideDown {
        from { transform: translateY(-30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
</style>
""", unsafe_allow_html=True)


# Initialize OpenAI client
@st.cache_resource
def init_openai_client():
    try:
        return OpenAI(
            api_key=GEMINI_API_KEY,
            base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
        )
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {str(e)}")
        st.error("Please make sure your OPENAI_API_KEY is set in your .env file")
        return None

client = init_openai_client()

# client = OpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
# )

SYSTEM_PROMPT = BIGB_SYSTEM_PROMPT

#---------------------------------------####
#STREAMLIT APPLICATION
#---------------------------------------####

#SESSION VARIABLES
if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role' : 'system', 'content' : SYSTEM_PROMPT}
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "processing" not in st.session_state:
    st.session_state.processing = False

#HEADER 
st.markdown('''
     <div class = 'main_header'>
        <h1> Amitabh Bachchan AI </h1>
        <p> Aapka saathi, aapka salaahkaar - Big B ki awaaz mein </p>
     </div>       
            ''', unsafe_allow_html=True)


#messages exchanged  stat card
st.markdown(f"""
<div style="display: flex; justify-content: center; margin: 1rem 0;">
    <div style="
        background: #f8fafc; 
        padding: 1.5rem 2rem; 
        border-radius: 1rem; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
        text-align: center; 
        width: 250px;">
        <div style="font-size: 2.5rem; font-weight: bold; color: #2563eb;">
            {st.session_state.message_count}
        </div>
        <div style="font-size: 1rem; color: #64748b;">
            Messages Exchanged
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

#Quote section 
quotes = [
    ('Lehron se darkar nauka paar nahi hoti,Koshish karne walon ki kabhi haar nahi hoti.', 'Amitabh Bachchan'),
    ('Tu khud ki khoj mein nikal, tu kis liye hataash hai,Tu chal, tere wajood ki samay ko bhi talaash hai.', 'Amitabh Bachchan'),
    ('Maana ki mushkil bahut hai, magar waqt hi toh hai,Guzar jaayega, guzar jaayega.', 'Amitabh Bachchan')
]

random_quote = random.choice(quotes)
st.markdown(f"""
<div class="quote-section">
    <div class="quote-text">"{random_quote[0]}"</div>
    <div class="quote-author">— {random_quote[1]}</div>
</div>
""", unsafe_allow_html=True)


#chat container
container = st.container()

with container:
    # st.markdown('<div class = "chat-container">')
    if not st.session_state.chat_history:
        #display welcome message 
        st.markdown("""
        <div class="welcome-message">
            <h3>🙏 Deviyon aur Sajjano, aapka swagat hai</h3>
            <p>Aapke mann mein koi sawaal ho, ya aap bas kuch guftagoo karna chahte hon, main yahan aapke saath hoon.</p>
            <p><strong>Aazmaiye poochhna:</strong> "Koi kavita sunaiye", "Zindagi ke anubhav se kuch bataiye", ya "Aaj ka gyaan kya hai?"</p>
        </div>
        """, unsafe_allow_html=True)
    
    #display chat history 
    for i, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            st.markdown(f"<div class = 'user_message'>{message['content']}</div>", unsafe_allow_html=True)
        elif message['role'] == 'assistant':
            st.markdown(f"<div class = 'ai_message'>{message['content']}</div>", unsafe_allow_html=True)
    
    
    
    #input section 
    st.markdown("---")
    
    #create form so that enter key submiison is valid
    with st.form(key='chat-form', clear_on_submit=True):
        col1, col2 = st.columns([5,1])
        
        with col1:
            user_input = st.text_input(
                "user_input",
                placeholder="Type your query and press Enter",
                label_visibility='collapsed',
                disabled=st.session_state.processing
            )
        with col2:
            send_button = st.form_submit_button(
                "Send 🚀",
                use_container_width=True,
                disabled=st.session_state.processing
            )
    
    #handle submisson 
    if send_button and user_input.strip() and not st.session_state.processing:
        if client is None:
            st.error("Client not configured, Check settings.")
        else:
            st.session_state.processing = True #set prcoseing state
            #add to session history 
            st.session_state.chat_history.append({'role': 'user', 'content' : user_input.strip()})
            st.session_state.messages.append({'role': 'user', 'content' : user_input.strip()})
            st.session_state.message_count += 1
            
            #get response
            try:
                with st.spinner("BigB is Thinking...."):
                    response = client.chat.completions.create(
                        model='gemini-2.5-flash-lite',
                        messages=st.session_state.messages,
                    )
                    ai_response = response.choices[0].message.content.strip()
                    # print(ai_response)
                    
                    #add ai repsonse to session sate
                    st.session_state.chat_history.append({'role': 'assistant', 'content' : ai_response})
                    st.session_state.messages.append({'role': 'assistant', 'content' : ai_response})
                    st.session_state.message_count += 1
                
            except Exception as e:
                st.error(f"❌ OOPS! Something went wrong: {str(e)}" )
            
            finally:
                #reset processsing state
                st.session_state.processing = False
            
            #rerun 
            st.rerun()
    
    #action butons 
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.chat_history and st.button("Clear Chat", help="Start a new conversation"):
            st.session_state.chat_history = []
            st.session_state.messages = [
                {'role' : 'system', 'content' : SYSTEM_PROMPT }
            ]
            st.session_state.message_count = 0
            st.rerun()
            
    with col2:
        if st.button("💡 Example Questions: ", help="Get some conversation starters"):
            st.info("""
        **Aap poochh sakte hain:**
        - "Apne struggle ke dino ke baare mein kuch bataiye."
        - "Zindagi mein safalta ka kya mantra hai?"
        - "Film industry mein newcomers ke liye aapki kya salaah hai?"
        """)