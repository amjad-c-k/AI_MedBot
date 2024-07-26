import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
import base64

# Function to decode the API key
def decode_api_key(encoded_api_key):
    decoded_bytes = base64.b64decode(encoded_api_key.encode('utf-8'))
    decoded_str = str(decoded_bytes, 'utf-8')
    return decoded_str

# Decode your API key
api_key = decode_api_key("QUl6YVN5QXpvdTdPZjh3ckhfaU84QUtVLV9mRzZYUmVFUVNHcFYw")

llm_config = {"model": "gemini-pro"}

llm = ChatGoogleGenerativeAI(
    **llm_config,
    temperature=1,
    max_output_tokens=1000,
    google_api_key=api_key
)

memory = ConversationBufferMemory()

if 'conversation' not in st.session_state:
    st.session_state.conversation = ConversationChain(llm=llm, verbose=True, memory=memory)

st.set_page_config(page_title="Enhanced ChatBot", layout="centered", page_icon=":hospital:")
st.title("Enhanced Medical ChatBot")

options = ["Symptom-Based Diagnosis", "General Medical Consultation"]  
selected_role = st.selectbox("Select LLM Role:", options)

if 'chat_history1' not in st.session_state:
    st.session_state.chat_history1 = []

if 'chat_history2' not in st.session_state:
    st.session_state.chat_history2 = []

user_input = st.chat_input("Your Input...")

if user_input:
    if selected_role == "Symptom-Based Diagnosis":
        system_instruction = ("You are a medical Doctor with 20 years of experience. Patient will describe their symptoms. "
                              "You should provide an accurate diagnosis, recommend medicines, recommend tests if needed, "
                              "suggest bed rest or dietary changes, and offer general health advice based on the given symptoms. "
                              "Also, remember everything you have been told. Never say that you are not a medical doctor etc. If asked about non-medical issues, just say "
                              "'I do not know about this.'")
        prompt = f"{system_instruction}\nUser: {user_input}\nBot:"
        response = st.session_state.conversation.predict(input=prompt)
        
        st.session_state.chat_history1.append(("You", user_input))
        st.session_state.chat_history1.append(("👨🏻‍⚕️", response))

        # Display current response and chat history
        with st.container():
            for role, text in st.session_state.chat_history1:
                if role == "You":
                    st.markdown(f"""
                    <div style='display: flex; justify-content: flex-end;'>
                        <div style='background-color:#e1f5fe;padding:10px;border-radius:10px;max-width:70%;'>
                             {text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='display: flex; justify-content: flex-start;'>
                        <div style='background-color:#fff9c4;padding:10px;border-radius:10px;max-width:70%;'>
                            {text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(" ")

    elif selected_role == "General Medical Consultation":
        system_instruction = ("You are a knowledgeable general practitioner. Users will ask you medical questions. "
                              "Provide comprehensive answers, recommend further actions if necessary, and maintain a "
                              "professional and empathetic tone. Also, remember everything you have been told. If asked "
                              "about non-medical issues, just say 'I do not know about this.'")
        prompt = f"{system_instruction}\nUser: {user_input}\nBot:"
        response = st.session_state.conversation.predict(input=prompt)
        
        st.session_state.chat_history2.append(( "You",user_input))
        st.session_state.chat_history2.append(("👨🏻‍⚕️", response))

        # Display current response and chat history
        with st.container():
            for role, text in st.session_state.chat_history2:
                if role == "You":
                    st.markdown(f"""
                    <div style='display: flex; justify-content: flex-end;'>
                        <div style='background-color:#e1f5fe;padding:10px;border-radius:10px;max-width:70%;'>
                            {text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='display: flex; justify-content: flex-start;'>
                        <div style='background-color:#fff9c4;padding:10px;border-radius:10px;max-width:70%;'>
                             {text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(" ")

    else:
        st.write("Please select a role for the LLM.")
