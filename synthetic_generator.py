import json
import os
from openai import OpenAI 

class SyntheticDataGenerator:
    def __init__(self,api_key,output_dir = "./data"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(self.output_dir)
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")

        self.client = OpenAI(api_key= api_key)

    def get_response(self,context_text):
        system_prompt = "You are an expert hedge fund analyst. Extract the primary financial driver from the provided text in one sentence."
        try:
            response = self.client.chat.completions.create(
                model = "gpt-4o-mini",
                messages =[
                {"role":"system","content":system_prompt},
                {"role":"user","content":context_text}
                ],
                temperature= 0.2
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("ERROR : failed to generate the response{e}")
            return "ERROR: Failed to generate response."
        
    def generate_jsonl(self,raw_text_list,filename="synthetic_dataset.jsonl"):
        file_path = f"{self.output_dir}/{filename}"

        with open(file_path,"w") as f:
            for text_chunk in raw_text_list:
                ai_analysis = self.get_response(text_chunk)
                data_points = {"instruction":"Extract the primary financial driver from the provided text.",
                               "context":text_chunk,
                               "response":ai_analysis
                               }
                f.write(json.dumps(data_points)+"\n")

        print("Synthetic Data generation is Successful")

