import jsonlines
import os
import shutil
import json
def postprocessing(output_path):
    directory = "./tempDir2/"
    data_list = os.listdir(directory)
    
    f = open("./sage_research_methods.json", "r", encoding='utf-8')
    method_json = json.load(f)
    f.close()
    
    method = []

    for data_file in data_list:
        for information in method_json['@graph']:
            if 'skos:prefLabel' in information:
                method.append(information['skos:prefLabel']['@value'])
            else:
                method.append(information['rdfs:label'])
        
        result = []
        with open(directory+data_file, 'r') as f:
            for item in jsonlines.Reader(f):
                best_five = []
                best_five_score = []
                dic = {}
                method_dic = {}

                srls = item['srl']
                sentences = item['sentences']
                doc = item['doc_key'].split('.')[0]
                length_inf = 0
                for i in range(0, len(srls)):
                    if srls[i] != []:
                        for srl in srls[i]:
                            st = srl[1]
                            en = srl[2]

                            method_token = ""
                            #print(sentences[i])
                            for j in range(st, en+1):
                                #print(sentences[i][j-length_inf])
                                method_token += sentences[i][j-length_inf] + " "
                            method_token = method_token[:-1]
                            if method_token == "":
                                continue
 
                            if method_token.lower() not in dic:
                                dic[method_token.lower()] = 1
                            else:
                                dic[method_token.lower()] += 1
                    length_inf += len(sentences[i])
                for k in dic.keys():
                    for method_v in method_dic.keys():
                        if method_v.lower() == k:
                            method_dic[k] = dic[k]
                            del dic[k]
                sorted_dic = sorted(dic.items(), key = lambda k: k[1])
                sorted_method_dic = sorted(method_dic.items(), key = lambda k: k[1])

                if sorted_dic == []:
                    sorted_dic = {}
                if sorted_method_dic == []:
                    sorted_method_dic = {}
                best_five = []
                best_five_score = []
                if len(sorted_method_dic) > 5:
                    for temp in sorted_method_dic[-5:]:
                       best_five.append(temp[0])
                       best_five_score.append(temp[1])
                else:
                    for temp in sorted_method_dic:
                        best_five.append(temp[0])
                        best_five_score.append(temp[1])
                    i = -1
                    while len(best_five) <= 5:
                        if i < -len(sorted_dic):
                            break
                        best_five.append(sorted_dic[i][0])
                        best_five_score.append(sorted_dic[i][1])
                        i += -1
                total_method = len(sorted_dic) + len(sorted_method_dic)


                for i in range(0, len(best_five)):
                    score = float(best_five_score[i]) / float(total_method)
                    if score > 1.0:
                        score = 1.0
                    result.append({"publication_id": doc, "method": best_five[i], "score" : score})
    with open(output_path+"methods.json", 'w', encoding='utf-8') as make_file:
        json.dump(result, make_file, ensure_ascii=False, indent='\t')
    shutil.rmtree('./tempDir')
    shutil.rmtree('./tempDir2')        
