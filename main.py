import streamlit as st
import json

def run():
    st.set_page_config(
        page_title="Wirksam Quiz",
        page_icon="❓",
    )

if __name__ == "__main__":
    run()

# Custom CSS for the buttons
st.markdown("""
<style>
div.stButton button{ display: block; margin: 0 auto; background:white }
div.stButton:visited button { display: block; margin: 0 auto; background:white }
div.stButton:focus button { display: block; margin: 0 auto; background:gray }
div.stButton:active button { display: block; margin: 0 auto; background:gray }
div.stButton::hover button{
    color: blue;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# Initialize session variables if they do not exist
default_values = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': [], 'answer_submitted': False}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data
with open('content/quiz_data.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = []
    st.session_state.answer_submitted = False
    
def isSelectedOptionTrue():
    #for i in enumerate(st.session_state.selected_option):
    return (st.session_state.selected_option == quiz_data[st.session_state.current_index]['answer'])

def submit_answer():

    # Check if an option has been selected
    if st.session_state.selected_option:
        # Mark the answer as submitted
        st.session_state.answer_submitted = True
        # Check if the selected option is correct
        #if st.session_state.selected_option == quiz_data[st.session_state.current_index]['answer']:
        if(isSelectedOptionTrue()):
            st.session_state.score += 10
    else:
        # If no option selected, show a message and do not mark as submitted
        st.warning("Please select an option before submitting.")

def next_question():
    st.session_state.current_index += 1
    st.session_state.selected_option = []
    st.session_state.answer_submitted = False

# Title and description
st.title("Wirksam Quiz")

# Progress bar
progress_bar_value = (st.session_state.current_index + 1) / len(quiz_data)
st.metric(label="Punkte", value=f"{st.session_state.score} / {len(quiz_data) * 10}")
st.progress(progress_bar_value)

# Display the question and answer options
question_item = quiz_data[st.session_state.current_index]
st.subheader(f"Frage {st.session_state.current_index + 1}")
st.title(f"{question_item['question']}")
st.write(question_item['information'])

st.markdown(""" ___""")

# Answer selection
options = question_item['options']
correct_answer = question_item['answer']

if st.session_state.answer_submitted:
    #for i, option in enumerate(options):
    #    label = option
    #    if option == correct_answer:
    #        st.success(f"{label} (Richtige Antwort)")
    #    elif option == st.session_state.selected_option:
    #        st.error(f"{label} (Falsche Antwort)")
    #    else:
    #        st.write(label)
    if(isSelectedOptionTrue()):
        st.success(f"(Richtige Antwort)")
    else:
        st.error(f"(Falsche Antwort)")
        
else:
    for i, option in enumerate(options):
        if st.button(option, key=i, use_container_width=True):
            st.session_state.selected_option.append(option)

st.markdown(""" ___""")

# Submission button and response logic
if st.session_state.answer_submitted:
    if st.session_state.current_index < len(quiz_data) - 1:
        st.button('Nächste', on_click=next_question)
    else:
        st.write(f"Quiz beendet! Dein Ergebnis ist: {st.session_state.score} / {len(quiz_data) * 10}")
        if st.button('Neu versuchen', on_click=restart_quiz):
            pass
else:
    if st.session_state.current_index < len(quiz_data):
        st.button('Antwort abgeben', on_click=submit_answer)