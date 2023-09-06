"""
    Fine-Tuning Script for Open AI

    This script reads in the (expanded, see expand_qa.py) Q&A text and
    generates the appropriate messages format for the JSONL data we need
    to feed to OpenAI.

    Note that whenever we ask OpenAI to upload a file or perform a tuning,
    it can take a bit of time to complete asynchronously.  So we implement
    a wait loop after each step where we loop in a poll/sleep cycle until
    the task is done.
"""
import os
import json
import openai
from io import BytesIO
import time
from readdocs import readdocs


#   Get all the Q&As in a parsed format
qa_list = readdocs('expanded_qa.txt')

#   Build up the JSONL file for OpenAI
tune_data = ""
for qa in qa_list:
    d = {
            "messages": [
                {"role": "system", "content": "You are an expert at building GPT applications that work with Salesforce"},
                {"role": "user", "content": qa['q']},
                {"role": "assistant", "content": qa['a']}
            ]
        }
    tune_data += json.dumps(d) + '\n'

#   Now we have a string to upload...let's upload the data!

openai.api_key = os.getenv("OPENAI_API_KEY")

#   The call wants an opened file, not a string.  So instead of writing this
#   to a scratch file we use an in-memory buffer that looks like a file.
bf = BytesIO(bytes(tune_data, 'utf-8'))
bf.name = 'mydata.jsonl'

#   This does the upload
r = openai.File.create(
  file=bf,
  purpose='fine-tune'
)

print(f'Created file {r["id"]}')

# Before we use the file for tuning, we have to wait for it to be fully processed
while True:
    status = openai.File.retrieve(r["id"])
    if status['status'] == 'processed':
        break
    print(f'Waiting for completion.  Status={status["status"]}')
    time.sleep(30)

# Now, let's use the file for fine-tuning.  This is going to take a while,
# so let's track the time it takes to complete...
start_time = time.time()

r_t = openai.FineTuningJob.create(training_file=r['id'], model="gpt-3.5-turbo", hyperparameters={"n_epochs":10})

# Ugly, but gives us info about the task we just kicked uoff
print(r_t)

# Now we wait ... and wait ... and wait for the fine-tuning job to finish.
# We don't really have to, as OpenAI sends an email when it's done (so you
# know it's not a fast process).
while True:
    r_s = openai.FineTuningJob.retrieve(r_t['id'])
    print(f'{time.time() - start_time}: {r_s["status"]}')
    if r_s['status'] != 'pending' and r_s['status'] != 'running':
        break
    time.sleep(60)

# Report the final status
print(r_s)
