import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Set the page configuration immediately after imports
st.set_page_config(page_title="Unit Converter by Shahroz", layout="wide")

if "history" not in st.session_state:  # Initialize history list in session state
    st.session_state.history = []

# ----------------------------
# Load API Key & Initialize AI
# ----------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API Key is missing! Add it to the .env file.")

genai.configure(api_key=API_KEY)
ai_model = genai.GenerativeModel("gemini-1.5-flash")

# ----------------------------
# Include Animate.css for Animations
# ----------------------------
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>',
    unsafe_allow_html=True,
)

# ----------------------------
# Premium Custom CSS with Light/Dark Mode Adjustments & Animations
# ----------------------------
premium_css = """
<style>
/* Modern Gradient Background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    font-family: 'Poppins', sans-serif;
    color: #333;
    padding-top: 0 !important;
}
/* Glassmorphism Effect for Containers */
.st-emotion-cache-1y4p8pa, .st-emotion-cache-1jicfl2, .st-emotion-cache-6qob1r {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
    padding: 25px !important;
    margin-bottom: 25px !important;
    transition: all 0.3s ease-in-out !important;
    color: #333;
}
/* Hover Effects */
.st-emotion-cache-1y4p8pa:hover, .st-emotion-cache-1jicfl2:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5) !important;
}
/* Modern Input Fields */
.stTextInput>div>div>input, .stNumberInput>div>div>input,
.stSelectbox>div>div>select, .stTextArea>div>textarea {
    border-radius: 15px !important;
    border: 2px solid #e0e0e0 !important;
    padding: 12px 20px !important;
    transition: all 0.3s ease !important;
    font-family: 'Poppins', sans-serif;
    color: #333;
}
.stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 15px rgba(102, 126, 234, 0.2) !important;
}
/* Gradient Buttons */
.stButton>button {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 30px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2) !important;
}
/* Animated Header */
header h1 {
    font-size: 2.5rem !important;
    color: white !important;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    margin-bottom: 30px !important;
    font-family: 'Poppins', sans-serif;
}
/* Pulse Animation for Convert Button */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
.convert-btn-animation {
    animation: pulse 2s infinite;
}
/* Result Display Animation */
@keyframes slideIn {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
.stSuccess {
    animation: slideIn 0.5s ease-out !important;
    border-left: 5px solid #667eea !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-weight: bold !important;
    background-color: #667eea !important;
    padding: 15px !important;
}
/* Text styling for markdown and alerts */
.stMarkdown, .stText, .stAlert, .stSuccess, .stError {
    color: white !important;
}
/* Custom Tabs Design */
[data-baseweb="tab-list"] {
    gap: 10px !important;
}
[data-baseweb="tab"] {
    padding: 12px 25px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    background: rgba(255, 255, 255, 0.95) !important;
    font-family: 'Poppins', sans-serif;
    color: #333;
}
[data-baseweb="tab"]:hover {
    background: white !important;
    transform: translateY(-2px);
}
[aria-selected="true"] {
    background: white !important;
    color: #667eea !important;
    font-weight: bold !important;
    border-bottom: 3px solid #667eea !important;
}
/* Footer Styling */
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 0px;
    font-family: 'Poppins', sans-serif;
    font-size: 14px;
    color: white;
    backdrop-filter: blur(10px);
}
@media (max-width: 768px) {
    header h1 {
        font-size: 1.8rem !important;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input,
    .stSelectbox>div>div>select, .stTextArea>div>textarea {
        padding: 10px 15px !important;
        font-size: 14px !important;
    }
    .stButton>button {
        padding: 10px 20px !important;
        font-size: 14px !important;
    }
    [data-baseweb="tab"] {
        padding: 10px 15px !important;
        font-size: 14px !important;
    }
    .footer {
        font-size: 12px !important;
    }
    .stSuccess {
        animation: slideIn 0.5s ease-out !important;
        border-left: 5px solid #667eea !important;
        border-radius: 12px !important;
        color: white !important;
        background-color: #667eea !important;
        padding: 15px !important;
    }
}
</style>
"""
st.markdown(premium_css, unsafe_allow_html=True)

# ----------------------------
# Manual Converter Setup
# ----------------------------
conversion_factors = {
    "Length": {
        "meter": 1, "kilometer": 0.001, "centimeter": 100, "millimeter": 1000,
        "mile": 0.000621371, "yard": 1.09361, "foot": 3.28084, "inch": 39.3701
    },
    "Weight": {
        "kilogram": 1, "gram": 1000, "milligram": 1e6, "pound": 2.20462, "ounce": 35.274
    },
    "Temperature": {
        "Celsius": lambda x: x,
        "Fahrenheit": lambda x: (x * 9/5) + 32,
        "Kelvin": lambda x: x + 273.15
    },
    "Volume": {
        "liter": 1, "milliliter": 1000, "gallon": 0.264172, "quart": 1.05669,
        "pint": 2.11338, "cup": 4.22675, "fluid ounce": 33.814
    },
    "Speed": {
        "meter per second": 1, "kilometer per hour": 3.6,
        "mile per hour": 2.23694, "knot": 1.94384
    },
    "Time": {
        "second": 1, "minute": 1/60, "hour": 1/3600, "day": 1/86400
    },
    "Area": {
        "square meter": 1, "square kilometer": 1e-6, "square mile": 3.861e-7,
        "square yard": 1.19599, "square foot": 10.7639, "acre": 0.000247105
    },
    "Data Storage": {
        "byte": 1, "kilobyte": 1/1024, "megabyte": 1/(1024**2),
        "gigabyte": 1/(1024**3), "terabyte": 1/(1024**4)
    }
}

def convert_units(value, from_unit, to_unit, category):
    if category == "Temperature":
        celsius_value = conversion_factors[category][from_unit](value)
        return conversion_factors[category][to_unit](celsius_value)
    return value * (conversion_factors[category][to_unit] / conversion_factors[category][from_unit])

# ----------------------------
# AI Converter Functions
# ----------------------------
def is_roman_urdu(query):
    query_lower = query.lower()
    # If the query contains any actual Urdu script letters, it's not Roman Urdu.
    for char in query:
        if '\u0600' <= char <= '\u06FF':
            return False
    # Use only keywords that are unique to Roman Urdu conversation.
    roman_urdu_keywords = ["kitne", "hotay", "hain", "kaise", "kya", "badlo"]
    for keyword in roman_urdu_keywords:
        if keyword in query_lower:
            return True
    return False

def determine_language(user_query):
    # If the query contains any Urdu script, consider it Urdu (and then reject it).
    if any('\u0600' <= c <= '\u06FF' for c in user_query):
        return "Urdu"
    # If uniquely Roman Urdu keywords are found, treat it as Roman Urdu.
    elif is_roman_urdu(user_query):
        return "Roman Urdu"
    else:
        return "English"

def ai_response(user_query):
    language_mode = determine_language(user_query)

    # Only allow English or Roman Urdu
    if language_mode == "Urdu":
        return "❌ I only answer unit conversion questions in English or Roman Urdu. Please use one of these languages."

    if language_mode == "Roman Urdu":
        prompt = f"""
You are a smart unit converter assistant created by Muhammad Shahroz. Your sole purpose is to perform unit conversions.
You must understand and process natural language queries accurately, even if they include minor spelling mistakes or informal language.
When provided with a query that asks for a unit conversion, parse the query intelligently, correct minor mistakes if necessary, and respond with the correct conversion result using proper spelling for all unit names.
Instructions:
- Respond in Roman Urdu using Latin characters only.
- Correct any minor spelling mistakes in your response (e.g., "mityer" should become "meter").
- If the query is ambiguous or contains excessive errors, respond with: "❌ Please use correct spelling for a better response."
- If the query is off-topic, respond with: "❌ I only answer unit conversion questions in Roman Urdu. Please ask a valid unit conversion question."
- If the user expresses gratitude, respond with "JazakAllah....."
- If the user asks about your creation, state: "Mujhe Muhammad Shahroz ne banaya hai."
Examples:
- "1 miter me kitne cm hain" → "1 miter me 100 cm hotay hain"
- "2 kg ko gram mein badlo" → "2 kg 2000 gram hotay hain"
Now answer the following question: {user_query}
"""
    else:  # English
        prompt = f"""
You are a smart unit converter assistant created by Muhammad Shahroz. Your sole purpose is to perform unit conversions.
You must understand and process natural language queries accurately, even if they include minor spelling mistakes or informal language.
When provided with a query that asks for a unit conversion, parse the query intelligently, correct minor mistakes if necessary, and respond with the correct conversion result using proper spelling for all unit names.
Instructions:
- Respond in English.
- Correct any minor spelling mistakes in your response (e.g., "centemeter" should become "centimeter").
- If the query is ambiguous or contains excessive errors, respond with: "❌ Please use correct spelling for a better response."
- If the query is off-topic, respond with: "❌ I only answer unit conversion questions in English. Please ask a valid unit conversion question."
- If the user expresses gratitude, respond with "You're welcome!"
- If the user asks about your creation, state: "I was created by Muhammad Shahroz."
Examples:
- "1 meter in cm" → "1 meter = 100 cm"
- "2 kg to gram" → "2 kg = 2000 gram"
Now answer the following question: {user_query}
"""
    response = ai_model.generate_content(prompt)
    return response.text.strip()

# ----------------------------
# Streamlit App Layout Using Tabs at the Top
# ----------------------------
st.markdown("<header class='animate__animated animate__fadeInDown'><h1>Advance Unit Converter</h1></header>", unsafe_allow_html=True)

tabs = st.tabs(["Manual Converter", "AI Unit Converter"])

with tabs[0]:
    st.subheader("Manual Unit Converter")
    st.write("Convert between different units easily!")
    categories = list(conversion_factors.keys())
    category = st.selectbox("Select Category", categories)
    if category:
        units = list(conversion_factors[category].keys())
        col1, col2, col3 = st.columns(3)
        with col1:
            from_unit = st.selectbox("From Unit", units)
        with col2:
            to_unit = st.selectbox("To Unit", units)
        with col3:
            value = st.number_input("Enter Value", min_value=0.0, value=1.0, step=0.1)
        if st.button("Convert", key="manual_convert"):
            result = convert_units(value, from_unit, to_unit, category)
            st.success(f"**{value:.4f} {from_unit} = {result:.4f} {to_unit}**")
            conversion_text = f"{value:.4f} {from_unit} = {result:.4f} {to_unit}"
            st.session_state.history.append(conversion_text)

    if st.session_state.history:
        st.subheader("Conversion History")
        for item in st.session_state.history:
            st.markdown(f"- {item}")

with tabs[1]:
    st.subheader("AI Unit Converter")
    st.write("Ask your unit conversion question in natural language (English or Roman Urdu).")
    user_query = st.text_area("Enter your query here")
    if st.button("Ask AI", key="ai_convert"):
        if user_query.strip() == "":
            st.error("Please enter a valid query.")
        else:
            with st.spinner("Generating response..."):
                answer = ai_response(user_query)
                st.markdown(f"**Answer:** {answer}")

# ----------------------------
# Footer Aligned at the Bottom
# ----------------------------
footer = """
    <div class="footer">
        Made with ❤️ by Muhammad Shahroz
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
