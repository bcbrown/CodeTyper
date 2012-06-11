import requests
import json
import base64
import random

domain = 'https://api.github.com'
def get_refs(user, repo):
    method = '/repos/' + user + '/' + repo + '/git/refs'
    r = requests.get(domain+method)
    return json.loads(r.content)
    
def get_commit(user, repo, sha):
    method = '/repos/' + user + '/' + repo + '/git/commits/' + sha
    return json.loads(requests.get(domain+method).content)
    
def get_tree(user, repo, sha):
    method = '/repos/' + user + '/' + repo + '/git/trees/' + sha + '?recursive=1'
    return json.loads(requests.get(domain+method).content)
    
def get_blob(user, repo, sha):
    method = '/repos/' + user + '/' + repo + '/git/blobs/' + sha
    return json.loads(requests.get(domain+method).content)
    
def get_text(user='bcbrown', repo='thinkpython-exercises'):
    # need to choose which ref, which tree
    # need to split a code file into 
    # at each stage choose randomly
    # if dead-end, loop to next 
    # via (if return is not None)
    # inside a for r in object
    # with a final return from inside innermost loop
    refs = get_refs(user, repo)
    ref_count = len(refs)
    i = random.randint(0, ref_count-1)
    sha = refs[i]['object']['sha']
    commit_sha = get_commit(user, repo, sha)['sha']
    tree = get_tree(user, repo, commit_sha)
    print 'trees:', len(tree['tree'])
    tree_sha = tree['tree'][0]['sha']
    tree_path = tree['tree'][0]['path']
    print 'path:', tree_path
    blob = get_blob(user, repo, tree_sha)
    text = base64.b64decode(blob['content'])
    return text