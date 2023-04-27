import openai
import streamlit as st
from streamlit_chat import message

# Function to generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

# Function to update total cost in sidebar
def update_total_cost():
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

# Setting page title and header
st.set_page_config(page_title="AVA", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>AVA - a totally harmless chatbot 😬</h1>", unsafe_allow_html=True)

# Set org ID and API key
openai.organization = "<YOUR_OPENAI_ORG_ID>"
openai.api_key = "<YOUR_OPENAI_API_KEY>"

# Initialize session state variables
st.session_state['generated'] = st.session_state.get('generated', [])
st.session_state['past'] = st.session_state.get('past', [])
st.session_state['messages'] = st.session_state.get('messages', [{"role": "system", "content": "You are a helpful assistant."}])
st.session_state['model_name'] = st.session_state.get('model_name', [])
st.session_state['cost'] = st.session_state.get('cost', [])
st.session_state['total_tokens'] = st.session_state.get('total_tokens', [])
st.session_state['total_cost'] = st.session_state.get('total_cost', 0.0)

# Sidebar
st.sidebar.title("Sidebar")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
update_total_cost()
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
model = "gpt-3.5-turbo" if model_name == "GPT-3.5" else "gpt-4"

# Reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_tokens'] = []
    st.session_state['total_cost'] = 0.0
    update_total_cost()

# Main chat loop
response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # Calculate cost
        cost = total_tokens * .002 / 1000
        st.session_state['cost'].append(cost)
        st.session_state['total_cos+'] += cost
        
