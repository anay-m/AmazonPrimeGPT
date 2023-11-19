import pinecone
import requests
import os
import json
from pprint import pprint
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

api_key = os.environ.get('RAINFOREST_KEY')

pinecone.init(api_key=os.environ.get('PINECONE'), environment="gcp-starter")

def fetch_product_data(url):
    params = {
        'api_key' : api_key,
        'type': 'product',
        'url' : url,
        'include_summarization_attributes' : 'true'
    }
    response = requests.get("https://api.rainforestapi.com/request", params)
    return response.json()


# Function to fetch Q&A using URL
def fetch_questions(asin):
    params = {
        'api_key' : api_key,
        'type' : 'questions',
        'url' : 'https://www.amazon.com/ask/questions/asin/' + asin + '/',
        'max_page' : 1,
        'sort_by' : 'most_helpful'
    }
    response = requests.get("https://api.rainforestapi.com/request", params)
    return response.json()


def fetch_all_reviews(url):
    params = {
        'api_key' : api_key,
        'type' : 'reviews',
        'url' : url + "/product-reviews/",
        'output' : 'json',
        'max_page' : 1,
        'sort_by' : 'most_recent',
        'global_reviews' : 'false'
    }

    response = requests.get("https://api.rainforestapi.com/request", params)
    return response.json()


def format_product(url):
    # file_path = "dollhouse.json"
    # with open(file_path, 'r') as json_file:
    #     doll = json.load(json_file)
    doll = fetch_product_data(url)

    vec = {
        'id' : doll["product"]["asin"] + '-P',
        'metadata' : {
                'asin' : doll["product"]["asin"]
            }
    }

    if doll["product"].get("feature_bullets") is not None:
        features = " ".join(doll["product"]["feature_bullets"])
        response = client.embeddings.create(
            input="Title: " + doll["product"]["title"] + "\n" + "Description: " + features + "\n" + "Specifications: " + doll["product"]["specifications_flat"],
            model="text-embedding-ada-002"
        )
        vec['values'] = response.data[0].embedding
        vec['metadata']['text'] = "Title: " + doll["product"]["title"] + ", Description: " + features + ", Price: " + str(doll["product"]["buybox_winner"]["price"]["value"]) + ", Rating: " + str(doll["product"]["rating"]) + ", Specifications: " + doll["product"]["specifications_flat"]

    else:
        response = client.embeddings.create(
            input="Title: " + doll["product"]["title"] + "\n" + "Specifications: " + doll["product"]["specifications_flat"],
            model="text-embedding-ada-002"
        )
        vec['values'] = response.data[0].embedding
        vec["metadata"]['text'] = "Title: " + doll["product"]["title"] + ", Price: " + str(doll["product"]["buybox_winner"]["price"]["value"]) + ", Rating: " + str(doll["product"]["rating"]) + ", Specifications: " + doll["product"]["specifications_flat"]
        

    if doll["product"].get("summarization_attributes") is not None:
        vec["product"]["text"] += "Attribute Summarization: " + ", ".join([att["name"] + ": " + str(att["value"]) + "/5.0" for att in doll["product"]["summarization_attributes"]])
    # pprint(vec)
    return vec

def format_reviews(url, asin):
    # file_path = "review_result_lebron.json"
    # with open(file_path, 'r') as json_file:
    #     doll = json.load(json_file)
    doll = fetch_all_reviews(url)
    vectors = []
    
    for v in doll["reviews"]:
        response = client.embeddings.create(
            input="Title: " + v["title"] + "\n" + "Review Body: " + v["body"],
            model="text-embedding-ada-002"
        )
        vec = {
            'id' : asin + "-" + str(v["page"]) + "-" + str(v["position"]) + "-R",
            'values' : response.data[0].embedding,
            'metadata' : {
                'asin' : asin,
                'text' : "Title: " + v["title"] + ", Review Body: " + v["body"] + ", Rating: " + str(v["rating"]) + "/5"
            }
        }

        vectors.append(vec)

    # pprint(vectors)
    return vectors

def format_qa(asin):
    # file_path = "qa_result.json"
    # with open(file_path, 'r') as json_file:
    #     doll = json.load(json_file)
    doll = fetch_questions(asin)

    vectors = []
    
    for v in doll["questions"]:
        if v.get("answer") is not None:
            response = client.embeddings.create(
                input="Question: " + v["question"] + "\n" + "Answer: " + v["answer"],
                model="text-embedding-ada-002"
            )

            vec = {
                'id' : doll["product"]["asin"] + "-" + str(v["page"]) + "-" + str(v["position"]) + "-Q",
                'values' : response.data[0].embedding,
                'metadata' : {
                    'asin' : doll["product"]["asin"],
                    'text' : "Question: " + v["question"] + ", Answer: " + v["answer"]
                }
            }

        vectors.append(vec)

    # pprint(vectors)
    return vectors

index = pinecone.Index("gptprime")
def checkForAsin(asin):
    vectorx = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    value_to_check = asin
    data = index.query(
        vector= vectorx,
        filter={
            'ASIN': value_to_check
        },
        top_k=1,
        include_metadata=True
    )
    if not data['matches']:
        return False
    else:
        return True

def main(data):
    #data = request.get_json()
    url = data.get('URL')
    asin = data.get("ASIN")
    if checkForAsin(asin=asin) is False:
        vectors = format_qa(asin)
        vectors.extend(format_reviews(url, asin))
        vectors.append(format_product(url))

        # index.upsert(vectors)

    return {}

stuff = {
    'URL': 'https://www.amazon.com/TORRAS-iPhone-15-Protection-Translucent/dp/B0CB5VCQWZ/?_encoding=UTF8&pd_rd_w=prMly&content-id=amzn1.sym.90e25839-c59e-4792-a597-79315d5273b3&pf_rd_p=90e25839-c59e-4792-a597-79315d5273b3&pf_rd_r=WPXNAMB5G91RB2P3E5QW&pd_rd_wg=Rt6J1&pd_rd_r=f4511a34-04af-4611-bc77-7860046780b4&ref_=pd_gw_dealz_cs&th=1',
    'ASIN': 'B0CB5VCQWZ'
}

main(stuff)
