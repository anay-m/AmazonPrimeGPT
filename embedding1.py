import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import NLTKTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import (create_vectorstore_agent, VectorStoreToolkit, VectorStoreInfo)
import streamlit as st
import pinecone
#### PRELIMINARY ####

# initialize key
load_dotenv()
OpenAI.api_key = os.environ['OPENAI_API_KEY']

# sets llm **creativity**
llm = OpenAI(temperature=0.5, verbose=True)
embeddings = OpenAIEmbeddings()

# loads cleaned text file
file_path = 'C:\\Users\\devmp\\Desktop\\AmazonPrimeGPT\\info.json'

# Load JSON data
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Initialize Pinecone client
pinecone_api_key = os.environ['PINECONE']
pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')
index = pinecone.index('gptprime')

# Initialize lists to store embeddings
reviews_embeddings = []
# Iterate through each item in the JSON data
for item in json_data:
    # Extract "Price," "Description," and "Reviews"
    price = item.get('Price', '')
    description = item.get('Description', '')
    average_rating = item.get('Rating', '')
    reviews = item.get('Reviews', '')
    asin = item.get('ASIN', '')

    # Generate embeddings for each section
    # price_embedding = embeddings.vectorize_text(price)
    description_embedding = embeddings.vectorize_text(description)
    # rating_embedding = embeddings.vectorize_text(average_rating)
    reviews_embeddings = [embeddings.vectorize_text(review) for review in reviews]

    # Append the embeddings to the respective lists
    

