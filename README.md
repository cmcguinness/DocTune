# DocTune: Fine-Tune GPT-3.5 with a Q&A Document

This is a collection of utilities to support the process of fine-tuning gpt-3.5-turbo (and cleaning up afterwards).

The three utilities (in the order you'll use them) are:

| Name         | Use                                                          |
| ------------ | ------------------------------------------------------------ |
| expand_qa.py | Takes our input Q&A document and generates variations of the questions to produce an enriched and more robust training set. |
| tuner.py     | Performs the actual fine-tuning                              |
| Cleanup.py   | Deletes all files and models in your OpenAI account.  ¡Muy Peligroso! |

In addition to these files, there are some supporting files

| Name             | Use                                                |
| ---------------- | -------------------------------------------------- |
| QandA.txt        | The source of our Q&A                              |
| readdocs.py      | Reads and parses a Q&A style document              |
| requirements.txt | List of Python libraries that need to be insalled. |

## Usage

The first step is to run `expand_qa.py`.  This will generate `expanded_qa.txt` which holds our new (and *expanded* Q&A).

Next, run `tuner.py` Make sure you have the environment variable `OPENAI_API_KEY` set to the value of the key you want to use to access OpenAI services.  This process can take a long time; it took over 20 minutes for me.

When you're all done with everything and want to delete everything on OpenAI, you can run `Cleanup.py`.



