from __future__ import division
import fileinput
import time
import github
import random
import re
import logging
from nltk.metrics import edit_distance

logging.basicConfig(filename='codetyper.log',level=logging.DEBUG)

def get_text():
    # this function and everything it calls smells like a dead fish
    file, extension = github.get_file()
    print extension
    text = file.split('\n')
    if '.py' in extension:
        start, indentation = get_method_start_python(text)
        print start, indentation
        end = get_method_end_python(start, indentation, text)
        print end
        selection = [line[indentation:] for line in text[start:end]]
        return selection
        
def get_method_end_python(start, indentation, text):
    #Walk down the file, looking for the first line at same indentation
    i = start + 1
    while True:
        if i == len(text):
            return None
        m = re.search('\w', text[i])
        if m:
            if indentation == m.start():
                return i - 1
        i += 1
    
    
def get_method_start_python(text):
    attempts = 0 # I think "for attempts in range(10):" might be better
    while True:
        i = random.randrange(len(text))
        # Convert to regex later to only match at start of line
        while 'def' not in text[i]:
            i -= 1
            if i == -1:
                break
        if attempts > 10:
            # give up
            return None
        if i == -1:
            attempts += 1
            continue
        # now we have the starting line
        m = re.search('\w', text[i])
        if m:
            indentation = m.start()
            return i, indentation
        # unless that line was only whitespace, in which case loop again

def evaluate_submission(text, response):
	first = '\n'.join(text)
	second = '\n'.join(response)
	return edit_distance(first, second)

def get_input(indentations, max_lines):
    input = []
    for indent in indentations:
        line = raw_input(' ' * indent)
        input.append(' ' * indent + line)
    return input


def run():
    text = get_text()
    indentations = []
    p = re.compile(r'\s*(?=\S)')
    for line in text:
        print line
        m = p.match(line)
        indentations.append(m.end() if m else 0)
    start_clock = time.clock()
    submission = get_input(indentations, len(text))
    end_clock = time.clock()
    error = evaluate_submission(text, submission)
    elapsed_time = round(end_clock - start_clock, 2)
    print "%d errors in %0.2f seconds" % (error, elapsed_time)
    print "average time per line:", elapsed_time / len(text)
    print "average errors per line:", error / len(text)

if __name__ == '__main__':
    run()
