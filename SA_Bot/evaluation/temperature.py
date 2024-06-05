import os
import openai
from openai import OpenAI
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

class sabot:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        self.encoder = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L12-v2', model_kwargs={'device': "cpu"})
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L12-v2")
        self.vector_db = None  # Initialize vector_db as None

    def generate(self, question: str, context: str = None, temperature: float = 0.2):
        if context:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Using the information contained in the context, give a detailed answer to the question. Context: {context}. Question: {question}"}
            ]
        else:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Give a detailed answer to the following question. Question: {question}"}
            ]

        # Generate with a slightly higher max_tokens limit
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=400,  # Slightly higher than the desired max_tokens
            n=1,
            temperature=temperature,
        )

        text = response.choices[0].message.content.strip()
        return text

# Initialize the Sabot class
sabot_instance = sabot()

# Define the questions to test
questions = [
    "What are the benefits of using renewable energy sources?",
    "Explain the theory of relativity in simple terms.",
    "What is the impact of climate change on polar bears?"
]

# Define the temperature values to test
temperatures = [0.2, 0.5, 0.7, 1.0, 1.2]

# Collect responses
results = []

for question in questions:
    for temp in temperatures:
        response = sabot_instance.generate(question, temperature=temp)
        results.append({"Question": question, "Temperature": temp, "Response": response})

# Convert results to a DataFrame for easy manipulation
results_df = pd.DataFrame(results)

# Calculate the length of each response as a simple metric for analysis
results_df['Response Length'] = results_df['Response'].apply(len)

# Plot the results
plt.figure(figsize=(14, 8))

for question in questions:
    subset = results_df[results_df['Question'] == question]
    plt.plot(subset['Temperature'], subset['Response Length'], marker='o', label=question)

plt.title('Effect of Temperature on Response Length')
plt.xlabel('Temperature')
plt.ylabel('Response Length')
plt.legend()
plt.grid(True)
plt.show()

# Save the DataFrame to an Excel file
results_df.to_excel('results_df.xlsx', index=False)

# Display the DataFrame for reference
display(results_df)
