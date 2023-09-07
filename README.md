# DocTune: Fine-Tune GPT-3.5 with a Q&A Document

*Version 2*

This is a collection of utilities to support the process of fine-tuning gpt-3.5-turbo (and cleaning up afterward).

The three utilities (in the order you'll use them) are:

| Name         | Use                                                          |
| ------------ | ------------------------------------------------------------ |
| expand_qa.py | Takes our input Q&A document and generates variations of the questions to produce an enriched and more robust training set. |
| tuner.py     | Performs the actual fine-tuning                              |
| Cleanup.py   | Deletes all files and models in your OpenAI account.  ¡Muy Peligroso! |

In addition to these files, there are some supporting files

| Name             | Use                                                |
| ---------------- | -------------------------------------------------- |
| readdocs.py      | Reads and parses a Q&A style document              |
| requirements.txt | List of Python libraries that need to be insalled. |

The inputs to the process are held in the subdirectory "inputs" in a further subdirectory, one for each project.

In those project directories you'll find:

| Name              | Use                                                          |
| ----------------- | ------------------------------------------------------------ |
| QandA.txt         | The source of the questions and answers that we will use to fine-tune GPT-3.5 |
| OriginalQandA.txt | Optional, a set of Q&As that are to be "expanded" by generating variations before fine-tuning |
| SystemPrompt.txt  | The system prompt used by the project.                       |



## Usage

1. If you have an OriginalQandA.txt file to expand, run `expand_qa.py`.  This will generate `QandA.txt` which holds our new (and *expanded* Q&A). for Traning.
2. Next, run `tuner.py` Make sure you have the environment variable `OPENAI_API_KEY` set to the value of the key you want to use to access OpenAI services.  It will ask you which subdirectory of `inputs` holds the project you want to fine-tune.This process can take a long time; it took over 20 minutes for me.
3. Go into Playground to test out your newly fine-tuned custom model!

When you're all done with everything and want to delete **everything** on OpenAI, you can run `Cleanup.py`.  It's all or nothing, so if you want a better tool, you'll have to write it yourself, alas.



