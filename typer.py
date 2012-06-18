import fileinput
import time
import github
import random
import re
import logging
from __future__ import division

logging.basicConfig(filename='codetyper.log',level=logging.DEBUG)

def evaluate_line(master, submission):
    if master == submission:
        return 0
    if not master:
        return len(submission)
    if not submission:
        return len(master)
    error = 0
    m = 0
    s = 0
    logging.debug("master[%d]: %s", len(master), master)
    logging.debug("submission[%d]: %s", len(submission), submission)
    while True:
        # There's a bug here
        # master:     if not master:
        # submission: if not master:
        # m: 0, s: 0
        # m: 1, s: 3
        # m: 2, s: 7
        # m: 3, s: 15
        # The algorithm as written will match master[0] to submission[2]
        # 1 to 6, ie matching the spaces
        # this causes s to go past the end of the string
        logging.debug("m: %d, s: %d", m, s)
        # Use enumerate for the various index argument logic?
        # Exit condition. Special-case the last matchup
        if len(master) - 1 == m or len(submission) - 1 == s:
            if master[m] != submission[s]:
                error += 1
            # one of these will be zero, but easier to add both
            # than figure out which one to add
            error += len(master[m + 1:])
            error += len(submission[s + 1:])
            break
        if master[m] != submission[s]:
            # the simple case
            if master[m + 1] == submission[s + 1]:
                error += 1
            else:
                mm = m
                ss = s
                # calculate the number of typoes assuming under-typing
                while len(master) > mm:
                    if master[mm] == submission[s]:
                        break
                    mm += 1
                # calculate the number of typoes assuming over-typing
                while len(submission) > ss:
                    if master[m] == submission[ss]:
                        break
                    ss += 1
                # find out which one was smaller and use it
                if (mm - m) < (ss - s):
                    error += mm - m
                    m = mm
                elif (mm - m) > (ss - s):
                    error += ss - s
                    s = ss
                else:
                    # equality implies a miss-hit key, not too many or too few
                    # different from the 'simple case' above in that
                    # this handles a multiple-typo case, such as switching two
                    # letters, and that handles the single-typo case.
                    error += mm - m
                    m = mm
                    s = ss
        m += 1
        s += 1
    return error


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
    if text == response:
        return 0
    if not text:
        return len(response)
    if not response:
        return len(text)
    error = 0
    t = 0
    r = 0
    while True:
        if len(text) - 1 == t or len(response) - 1 == r:
            error += evaluate_line(text[t], response[r])
            # one of these will be zero
            error += sum([len(x) for x in response[r + 1:]])
            error += sum([len(x) for x in text[t + 1:]])
            return error
        else:
            error += evaluate_line(text[t], response[r])
            t += 1
            r += 1


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
