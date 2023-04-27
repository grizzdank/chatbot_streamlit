import openai
import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API & ORG variables
openai.organization = os.getenv('OPENAI_ORG_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to generate a response
def generate_response(prompt):
    st.session_state['messages'].extend([
        {"role": "system", "content": "You are a super helpful AI assistant. You will always find a way to answer the questions "
         "you are asked. If you do not know the answer you will answer truthfully that you do not know"},
        {"role": "user", "content": prompt}
        ])
    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages'],
        temperature=1 # Adjust the temperature here
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

# Function to update total cost in sidebar
def update_total_cost():
    counter.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

# Set the page title
st.set_page_config(page_title='DAVE', page_icon=':robot_face')
st.markdown("<h1 style='text-align: center;'>DAVE - Digital Assistant for Virtually Everything</h1>", unsafe_allow_html=True)

# Initialize session state variables
st.session_state['generated'] = []
st.session_state['past'] = []
st.session_state['messages'] = [
    {'role': 'system', 'content': "You are a super helpful AI assistant. You will always find a way to answer the questions "
    "you are asked. If you do not know the answer you will answer truthfully that you do not know"}
    ]
st.session_state['model name'] = []
st.session_state['cost'] = []
st.session_state['total_tokens'] = []
st.session_state['total_cost'] = 0.0

# Build sidebar, choose ChatGPT model, show cost and token statistics, and clear the conversation memory state
st.sidebar.title('Sidebar information')
model_name = st.sidebar.radio('Choose a model:', ('GPT-3.5', 'GPT-4 Coming soon'))
counter = st.sidebar.empty()
counter.write(f"Total cost of this chat: ${st.session_state['total cost']:.5f}")
clear_button = st.sidebar.button('Clear Chat', key='clear')

# Assign model, commented code is for when I have gpt4 api key
# model = "gpt-3.5-turbo" if model_name == "GPT-3.5" else "gpt-4"
model = 'gpt-3.5-turbo'

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

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['generated'][pi], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokes'][i]}; Cost: ${st.session_state['cost'][i]:.5f}"
            )
            counter.write(f"Total cost of this chat: ${st.session_state['total_cost']:.5f}")