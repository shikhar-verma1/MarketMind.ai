import os
import json

class Datasetbuilder:
    def __init__(self,output_dir = "./data"):
        self.output_dir = output_dir
       
    def generate_jsonl(self,raw_text_list,filename = "finetune_data.jsonl"):
        file_path = f"{self.output_dir}/{filename}"
        print(f"opening {file_path} for writing")

        with open(file_path,"wb") as f:
            for text_chunks in raw_text_list:
                data_point = {
                    "instruction": "What is the main feature which driving the revenue,profit or is the reason of the loss",
                    "context": text_chunks,
                    "response": "the main driving feature of the revenue ,profit or loss is the demand of that company of which that stock belongs",
                }
                f.write(json.dumps(data_point)+"\n")
        print("dataset successfully generated ")

