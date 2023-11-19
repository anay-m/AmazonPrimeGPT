import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import tiktoken
import json

# Initialize Pinecone
pinecone_key = '36ca9ad8-6b5e-4b0e-92d9-d355a6cb652d'
env = 'gcp-starter'
pinecone.init(api_key=pinecone_key, environment=env)
index = pinecone.Index('gptprime')

# Initialize OpenAI Embeddings
openai_apikey = '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'
model_name = 'text-embedding-ada-002'
embedding = OpenAIEmbeddings(model=model_name, openai_api_key=openai_apikey)

# Setup Vectorstore and Chat Model
text_field = 'text'
vectorstore = Pinecone(index, embedding.embed_query, text_field)
llm = ChatOpenAI(openai_api_key=openai_apikey, model_name='gpt-3.5-turbo', temperature=0.0)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

# Define the Cloud Function
def main_function(request):
    query = request['query']
    filt = request.get('filter', {})
    result = qa.run(query=query)
    return {'response': result}


stuff = {
    'query':"You have been given a list of product reviewers. Please be my virtual assistant and tell me what is this product about",
    'filter': {"asin": "B0CB5VCQWZ"}
}
print(main_function(stuff))