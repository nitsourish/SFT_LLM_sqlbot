
from datasets import load_dataset
from openai import OpenAI
import pandas as pd
from datasets import load_dataset
import pandas as pd
import streamlit as st
import numpy as np

client = OpenAI()
llm_model = "gpt-3.5-turbo"

sideBar = st.sidebar
finetune = sideBar.selectbox(
    "do you like to use fine-tuning?",
    ("yes", "no"))


def call_openai(system_prompt,prompt, model=llm_model):
	chat_completion = client.chat.completions.create(
		messages=[
			{
				"role": "system",
				"content": system_prompt
			},
			{
				"role": "user",
				"content": prompt,
			}
		],
		model=model,
	)
	return chat_completion.choices[0].message.content

def reformating_data(data):
	data['predicted_query'] = data['predicted_query'].apply(lambda x: re.sub(r'\s+', ' ',x))
	data['predicted_query'] = data['predicted_query'].str.lower()
	return data

def query_generator(question, is_finetuned=finetune):
    if is_finetuned:
        system_prompt = "agent knows how to do SQL query"
        prompt = question

        model = "ft:gpt-3.5-turbo-0125:personal::AEyiOkSI"    #placeholder to be replaced with the fine-tuned model from OpenAI
    else:
        system_prompt = "Follow the user commands."

        prompt = f"Translate the text command to SQL. Only output the SQL.\n" \
                    f"Text: Return all data from the customers table  SQL: Select * from customers ###\n"\
                    f"Text: Return all data from the customers table for customers' age > 60  SQL: Select * from customers where age > 60 ###\n"\
                    f"Translate the text command to SQL. Only output the SQL.\n"\
                    f"Text: {question} SQL: "	
        model = llm_model	
    result = call_openai(system_prompt,prompt, model)
    result = result.replace(";", "")
    return result

st.title('SQL Query Assistant')
#insert a image
st.image('streamlit/image.png', width=200)
question = st.text_input('Ask a question:')

if st.button('Submit'):
    response = query_generator(question, is_finetuned=finetune)
    st.write(response)
