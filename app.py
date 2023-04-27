import openai
import streamlit as st
from streamlit_chat import message
import os


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
        temperature=temp # Adjust the temperature in the sidebar
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response, completion.usage

# Function to update total cost in sidebar
def update_total_cost(counter):
    counter.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

# Function to reset the session state variables
def reset_state(counter):
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {'role': 'system', 'content': "You are a helpful AI assistant. You will always find a way to answer the questions "
        "you are asked. If you do not know the answer you will answer truthfully that you do not know"}
        ]
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_tokens'] = []
    st.session_state['total_cost'] = 0.0
    update_total_cost(counter)

# Set the page title
st.set_page_config(page_title='DAVE', page_icon=':robot_face')
st.markdown("<h1 style='text-align: center;'>DAVE - Digital Assistant for Virtually Everything</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Powered by ChatGPT API</h3>", unsafe_allow_html=True)

# Initialize session state variables
counter = st.sidebar.empty()
if 'generated' not in st.session_state:
    reset_state(counter)

# Build sidebar, choose ChatGPT model, show cost and token statistics, and clear the conversation memory state
st.sidebar.title('Sidebar information')
model_name = st.sidebar.radio('Choose a model:', ('GPT-3.5', 'GPT-4 Coming soon'))
temp = st.sidebar.number_input(label='Choose the creativity of the AI, between 0 and 1:', min_value=0.0, max_value=1.0, value=1.0)
clear_button = st.sidebar.button('Clear Chat', key='clear')

# Assign model, commented code is for when I have gpt4 api key
# model = "gpt-3.5-turbo" if model_name == "GPT-3.5" else "gpt-4"
model = 'gpt-3.5-turbo'

# Reset everything
if clear_button:
    reset_state(counter)
 

# Main chat loop
response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, usage = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(usage.total_tokens)

        # Calculate cost
        cost = usage.total_tokens * .002 / 1000
        st.session_state['cost'].append(cost) 
        st.session_state['total_cost'] += cost

        # Update and display the cost in the sidebar
        counter.write(f"Total cost of this chat: ${st.session_state['total_cost']:.5f}")

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, avatar_style='adventurer', key=str(i) + '_user')
            message(st.session_state['generated'][i], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}"
            )
            counter.write(f"Total cost of this chat: ${st.session_state['total_cost']:.5f}")