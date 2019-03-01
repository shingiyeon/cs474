
# coding: utf-8

# In[43]:


import nltk
import os
import jsonlines
import json


# In[44]:


def make_jsonlines(directory, data_list, methods, output_file):
    g = open(output_file, "w", encoding='utf-8')
    for data_file in data_list:
        f = open(directory + data_file, "r", encoding='utf-8')
        data = f.read()
        doc = {}
        doc["doc_key"] = data_file
        sentences = nltk.tokenize.sent_tokenize(data)
        SRL = []
        total_tokens = []
        sen_len = 0
        
        for sentence in sentences:
            temp = []
            tokens = nltk.tokenize.word_tokenize(sentence)
            pos_tags = nltk.pos_tag(tokens)
            
            SRL.append(temp)
            total_tokens.append(tokens)
        doc["srl"] = SRL
        doc["sentences"] = total_tokens
        g.write(json.dumps(doc))
        g.write("\n")
    g.close()        

# In[49]:

def preprocessing(directory):
    data_list = os.listdir(directory)
    os.mkdir('tempDir')
    method = []
    length = len(data_list)
    for i in range(0, length):
    	make_jsonlines(directory, data_list[i:i+1], method, "./tempDir/test.jsonlines"+str(i))
    #make_jsonlines(directory, data_list[length*10:], method, "./tempDir/test.jsonlines"+str(length))

