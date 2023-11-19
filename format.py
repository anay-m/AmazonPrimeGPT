import os
import json
from pprint import pprint
from openai import OpenAI
client = OpenAI()

def format_product():
    file_path = "dollhouse.json"
    with open(file_path, 'r') as json_file:
        doll = json.load(json_file)

    # print(doll["product"]["asin"])

    # response = client.embeddings.create(
    #     input="Title: " + doll["product"]["title"] + "\n" + "Description: " + doll["product"]["description"] + "\n" + "Specifications: " + doll["product"]["specifications_flat"],
    #     model="text-embedding-ada-002"
    # )


    vec = {
        'id' : 'something goes here',
        'values' : [],
        'metadata' : {
            'asin' : doll["product"]["asin"],
            'title' : doll["product"]["title"],
            'description' : doll["product"]["description"],
            'price' : doll["product"]["buybox_winner"]["price"]["value"],
            'rating' : doll["product"]["rating"],
            # 'specifications' : [spec["name"] + ": " + spec["value"] for spec in doll["product"]["specifications"]]
            'specifications' : doll["product"]["specifications_flat"],
            # 'summarization_attributes' : [att["name"] + ": " + att["value"] + "/5.0" for att in doll["product"]["summarization_attributes"]]
        }
    }

    # pprint(vec)
    pprint("Title: " + doll["product"]["title"] + ", Description: " + doll["product"]["description"] + ", Specifications: " + doll["product"]["specifications_flat"])

format_product()
