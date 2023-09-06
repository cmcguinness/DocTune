import os
import json
import openai
from io import BytesIO
import time
from readdocs import readdocs

qa_list = readdocs()

tune_data = ""

for qa in qa_list:
    d = {
            "messages": [
                {"role": "system", "content": "You are an expert at building GPT applications"},
                {"role": "user", "content": qa['q']},
                {"role": "assistant", "content": qa['a']}
            ]
        }
    tune_data += json.dumps(d) + '\n'

# Note that you'll need to have this environment variable set to run the project

openai.api_key = os.getenv("OPENAI_API_KEY")

bf = BytesIO(bytes(tune_data, 'utf-8'))
bf.name = 'mydata.jsonl'

r = openai.File.create(
  file=bf,
  purpose='fine-tune'
)

r_t = openai.FineTuningJob.create(training_file=r['id'], model="gpt-3.5-turbo")

print(r_t)

while True:
    r_s = openai.FineTuningJob.retrieve(r_t['id'])
    if r_s['status'] != 'pending' and r_s['status'] != 'running':
        break
    time.sleep(5)

print(r_s)

x = 0
