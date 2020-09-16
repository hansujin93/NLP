def frequency_analysis(tokens):
    freq = nltk.FreqDist(tokens)
    for key,val in freq.most_common(20):
        print(key,val,sep="\t")

    freq.plot(20, cumulative=False)
    
def save_tokens(tokens, outfile):
    with open(outfile, 'w', encoding="utf-8") as f:
        for token in tokens: #iterate tokens and output to file.
            f.write(token + '\n')
        f.write(f"Total: {len(tokens)} tokens")
        
def tokenise_file(textfile, tokenise):
    with open(textfile, encoding="utf-8") as f:
        tokens = []
        lines = f.readlines()
        for line in lines:
            line_tokens = tokenise(line.strip())
            tokens.extend(line_tokens)
    return tokens

def custom_tokenise_forum(text):
    URL = "www\.\S*|https?:\S*" #this is one possible URL pattern, more complicated patterns that catch different URLs are possible.
#     word = "\w+"
    seq_punc = "[^\w\s]{2,}" # includes emoticons like :-)
    hashtag_mention = "[#@]\w+"
    hyphen = "[-\w]+"
    apos = "[\w]+['’`][\w]+"
    money = "[$£]\S+"
    emoticon = "[:;X\<].?[\)|\(|\\D\p|\d]"
    leftover = "\w+"
    patterns = (apos, URL, emoticon, money, hyphen, seq_punc, hashtag_mention, leftover)
    joint_patterns = '|'.join(patterns) #the patterns are split with | for alternation.
    p = re.compile(r'(?:{})'.format(joint_patterns)) # format is used to build the pattern, surrounding with (?:...) for non-captured grouping for alternation.
    return p.findall(text)
    
tokens = tokenise_file("mumsnet.txt", custom_tokenise_forum)
print_tokens(tokens)
save_tokens(tokens,"mumsnet_tok.txt")
frequency_analysis(tokens)
