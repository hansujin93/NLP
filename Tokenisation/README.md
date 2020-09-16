The aim of tokenisation is to separate the text into meaningful components that are useful for future analysis (e.g. counting or annotating). 
Often the most logical token is a "word" (e.g. for "bag-of-words" based methods), but deciding what constitutes a word is not straight-forward. 
At other times, punctuation should be maintained (e.g. for part of speech annotation). 
\
\
Build a tokeniser for the mumsnet forum data(mumsnet.txt) by building on the custom_tokenise method.\
Tokenise the text with the following rules:\
* all punctuation separated as individual tokens, unless sequences of punctuation (e.g. !!!), which should be combined to a single token.
* URLs, hashtags, and mentions as separate tokens
* hyphenated words as a single token
* words with apostrophes to mark concatenation and possessive s should be a single token (e.g. don't, I'm and 1940's)
* emoticons separated as separate tokens (e.g. :-))
