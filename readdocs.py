"""
    readdocs:

    Read in the snippets we're going to use to fine tune the model.

    This is a simple implementation where we expect a text file that is
    formatted like the following:

        # Q
        The user question
        # A
        The answer GPT should give

    Questions and answers can span multiple lines, and this preserves
    the line breaks in the text for very simplistic formatting.

    This implements a very simple state model to process the lines of text:

    BEGIN → QUESTION ←→ ANSWER → END

    The # Q and # A are used to trigger a state transition.

    Returns an array of dictionaries, each dictionary having the keys
    "q" and "a" with values of the associated text.

"""


def readdocs():

    # Read in the entire set of q & a documents as a series of lines of text
    with open('QandA.txt', 'r') as f:
        qa_text = f.readlines()

    # I expect that the first line of the file will be a # Q, but this allows
    # me to tolerate lines at the beginning of the file that are not
    # (presumably blank lines)
    state = 'BEGIN'

    q_n_a = []          # What we will ultimately return
    current = None      # The "current" Q and A that is a WIP

    for line in qa_text:
        line = line.rstrip()            # Get rid of the \n at the end of the line
        if line.upper() == '# Q':
            if current is not None:
                q_n_a.append(current)
            current = {'q': '', 'a': ''}
            state = 'QUESTION'
            continue
        if line.strip().upper() == '# A':
            state = 'ANSWER'
            continue

        if state == 'QUESTION':
            current['q'] = current['q'] + line + '\n'

        if state == 'ANSWER':
            current['a'] = current['a'] + line + '\\n'

    # The only way it is None is if the file is blank, but might as well test...
    if current is not None:
        q_n_a.append(current)

    return q_n_a
