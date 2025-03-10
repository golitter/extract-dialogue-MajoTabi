from src.extract import system_prompt
from src.schema import novel_schema
from src.LLM import DeepseekChat
from src.utils import ReadFiles
from tqdm import tqdm
import json


file_path = './test/test.txt'
docs = ReadFiles(file_path).get_content(max_token_len=500, cover_content=0)

sys_prompt = system_prompt(novel_schema)

model = DeepseekChat()

file_name = file_path.split('/')[-1].split('.')[0]

for i in tqdm(range(len(docs))):
    response = model.chat(sys_prompt, docs[i])
    try:
        response = json.loads(response)
        for item in response:
            with open(f'{file_name}.jsonl', 'a', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
    except Exception as e:
        print(e)