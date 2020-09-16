def ascii_encode_de(string):
    return string.encode('ascii', 'ignore').decode('utf-8')

with open("mumsnet.txt") as f:
    posts = f.read()
    posts = posts.replace('’',"'").replace('`',"'")
    posts = ascii_encode_de(posts)    
posts = re.sub('[@#]\w+|www\.\S*|https?:\S*','',posts)
print(posts)

# outputted as text file
with open('preprocessing_result.txt', 'w') as f:
    f.write(posts)
