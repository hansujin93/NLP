import ftfy

def import_party_folder(party):
    folder = "mps/" + party
    textfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".txt")]
    for tf in textfiles:
        username = splitext(split(tf)[1])[0] #extract just username from filename.
        print("Processing " + username)
        doc = Document({'username': username, 'party': party}) #include metadata
        with open(tf) as f:
            tweets = f.readlines()
        doc.extract_features(tweets)
        yield doc
        
def merge_fqls(fqls):
    merged = Counter()
    for fql in fqls:
        merged += fql
    return merged
    
def log_ratio(corpus1, corpus1_size, corpus2, corpus2_size):
    return {term: log((corpus1[term]/corpus1_size)/((corpus2[term] if corpus2[term] else 0.5)/corpus2_size),2) for term in corpus1}
    
def tf(term, doc):
    return doc[term] / sum(doc.values()) #term freq / total terms (relative term freq)

def num_containing(term, corpus):
    return sum(1 for doc in corpus if term in doc) #counts docs in corpus containing term.

def idf(term, corpus):
    n_t = num_containing(term,corpus)
    return log((len(corpus)+1) / ((n_t) + 1))
    
def tfidf(term, doc, corpus):
    return tf(term, doc) * idf(term, corpus) 
    
def preprocess(text):
    text = text.encode('ascii','ignore').decode('utf-8')
    t = re.sub(r"#(\w+)", r'\1', text) #hashtagged word would be meaningful, so keep the text after '#' symbol
    t = re.sub(r"@(\w+)", r'\1', t) #would be meaningful so keep the text
    t = re.sub(r"[@#]\w+|www\.\S*|https?:\S*",'',t) #remove url
    tt = ftfy.fix_text(t)
    return tt

def custom_tokenise(text):
    seq_punc = "[^\w\s]{2,}" #sequences of punctuation
    hyphen = "[-\w]+"
    apos = "[\w]+['’`][\w]+"
    money = "[$£]\S+"
    leftover = "\w+" #no emojis, no special symbols
    patterns = (apos, money, hyphen, seq_punc, leftover)
    joint_patterns = '|'.join(patterns)
    p = re.compile(r'(?:{})'.format(joint_patterns)) 
    return p.findall(text)
    
corpus = []
corpus.extend(import_party_folder("labour"))
corpus.extend(import_party_folder("conservative"))
print(corpus)

import numpy as np
def avg_token_length(cp):
    ans = list()
    for p in cp:
        total_len_token_list = list()
        mp = p.meta['username']
        party = p.meta['party']
        tokens = [term for term in p.tokens_fql]
        for t in tokens:
            total_len_token = len(t)*p.tokens_fql[t]
            total_len_token_list.append(total_len_token)
#             print(total_len_token)
#             print(len(t), p.tokens_fql[t])
        ans.append([party, mp, round(sum(total_len_token_list)/sum(p.tokens_fql.values()),4)])
    ans = np.array(ans)
    return ans
ans = avg_token_length(corpus)
# print(ans)
print('highest: ', ans[np.argmax(ans[:,2])])



con_fql = merge_fqls([p.tokens_fql for p in corpus if p.meta['party']=='conservative'])
lab_fql = merge_fqls([p.tokens_fql for p in corpus if p.meta['party']=='labour'])
con_tag = merge_fqls([p.tag_fql for p in corpus if p.meta['party']=='conservative'])
lab_tag = merge_fqls([p.tag_fql for p in corpus if p.meta['party']=='labour'])
con_tag_size = sum(con_fql.values())
lab_tag_size = sum(lab_fql.values())
lab_lr = log_ratio(lab_tag, lab_tag_size, con_tag, con_tag_size)
sorted_tag = sorted(lab_lr.items(), key=lambda x:x[1], reverse = True)
for idx, v in sorted_tag[:5]:
    print(idx, round(v,4))



h_token = re.compile(r"#\w+")
def custom_tokenise(text):
    return h_token.findall(text)

h_cp = []
h_cp.extend(import_party_folder('labour'))
m = merge_fqls([doc.tokens_fql for doc in h_cp])
h_token = re.compile(r"#\w+")
def custom_tokenise(text):
    return h_token.findall(text)

h_cp = []
h_cp.extend(import_party_folder('labour'))
m = merge_fqls([doc.tokens_fql for doc in h_cp])
# for h in h_cp:
#     print(h.tokens_fql)

cp_fqls = merge_fqls([doc.tokens_fql for doc in h_cp])
for hcp in h_cp:
    sc = {term: tfidf(term, hcp.tokens_fql, cp_fqls) for term in hcp.tokens_fql if hcp.meta['username'] == 'jeremycorbyn'}
    sorted_t = sorted(sc.items(), key=lambda x:x[1],reverse = True)
    for term, value in sorted_t[:5]:
        print("\tToken: {}, TF-IDF: {}".format(term, round(value, 5)))
