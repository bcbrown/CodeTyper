import requests
import json
import base64
import random

_domain = 'https://api.github.com'
_extensions = ['.py', '.c', '.cpp', '.h', '.rb', '.js', '.cs']

def get_refs(user, repo):
    method = '/repos/' + user + '/' + repo + '/git/refs'
    r = requests.get(_domain+method)
    return json.loads(r.content)
    
def get_commit(user, repo, sha):
    method = '/repos/' + user + '/' + repo + '/git/commits/' + sha
    return json.loads(requests.get(_domain + method).content)
    
def get_tree(user, repo, sha):
    method = '/repos/' + user + '/' + repo + '/git/trees/' + sha + '?recursive=1'
    return json.loads(requests.get(_domain + method).content)
    
def get_blob(user, repo, sha):
    method = '/repos/' + user + '/' + repo + '/git/blobs/' + sha
    return json.loads(requests.get(_domain + method).content)    
    
def get_file(user='bcbrown', repo='CodeTyper'):
    refs = get_refs(user, repo)
    # error when repo is empty:
    # >>> t = github.get_file() #returning 
    # number of refs: 1
    # ref: 0
    # >>> t
    # (0, {u'message': u'Git Repository is empty.'})
    ref_indices = range(len(refs))
    random.shuffle(ref_indices)
    print "number of refs:", len(refs)
    for ref in ref_indices:
        print "ref:", ref
        # return ref, refs
        sha = refs[ref]['object']['sha']
        commit_sha = get_commit(user, repo, sha)['sha']
        tree = get_tree(user, repo, commit_sha)
        print 'number of blobs', len(tree['tree'])
        # choose blobs at random, returning the first non-empty blob
        tree_indices = range(len(tree['tree']))
        random.shuffle(tree_indices)
        for t in tree_indices:
            print 'blob:', t
            tree_sha = tree['tree'][t]['sha']
            tree_path = tree['tree'][t]['path']
            print 'path:', tree_path
            # whitelist the extension:
            if any([x in tree_path for x in _extensions]):
                blob = get_blob(user, repo, tree_sha)
                text = base64.b64decode(blob['content'])
                if text:
                    # TODO: replace slice with a regex
                    return text, tree_path[:4] 
    return None