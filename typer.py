import fileinput
import time
import github
import random

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
    while True:
        # Exit condition. Special-case the last matchup
        if len(master) - 1 == m or len(submission) - 1 == s:
            if master[m] != submission[s]:
                error += 1
            # one of these will be zero, but easier to add both 
            # than figure out which one to add
            error += len(master[m+1:])
            error += len(submission[s+1:])
            break
        if master[m] != submission[s]:
            # the simple case
            if master[m+1] == submission[s+1]:
                error += 1
            else:
                mm = m
                ss = s
                # calculate the number of typoes assuming under-typing
                while len(master) > mm:
                    if master[mm] == submission[s]:
                        break;
                    mm += 1
                # calculate the number of typoes assuming over-typing
                while len(submission) > ss:
                    if master[m] == submission[ss]:
                        break;
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
    file, extension = github.get_file()
    text = file.split('\n')
    if '.py' in extension:
        # pick a random line in the text
        # search upwords for the last function def, and note the indentation
        # search downards for the next line at the same indentation
        while True:
            i = random.randrange(len(text))
            # Convert to regex later
            while 'def' not in text[i]:
                i -= 1
                if i = -1:
                    break
            if i = -1:
                # add max-redos functionality
                break
            # now we have the starting line
            indentation = 

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
            error += sum([len(x) for x in response[r+1:]])
            error += sum([len(x) for x in text[t+1:]])
            return error
        else:
            error += evaluate_line(text[t], response[r])
            t += 1
            r += 1
    
def get_input(max_lines=-1):
    input = []
    line = raw_input()
    while line:
        input.append(line)
        if len(input) == max_lines:
            break;
        line = raw_input()
    return input
    
def run():
    text = get_text()
    for line in text:
        print line
    start_clock = time.clock()
    submission = get_input(len(text))
    end_clock = time.clock()
    error = evaluate_submission(text, submission
    time = round(end_clock - start_clock, 2)
    print error
    print time
    
if __name__ == '__main__':
    run()