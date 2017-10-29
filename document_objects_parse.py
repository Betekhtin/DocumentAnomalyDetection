import os
import time
from ContractStructure import *
from paths import *

total_time = time.time()

doc_time = time.time()
avg_time = 0
counter = 0

for file in os.listdir(doc_txt_folder):
    counter += 1
    cur_time = time.time()

    d = Document(os.path.join(doc_txt_folder, file))
    d.save(doc_obj_folder, file.replace('.txt', ''))

    avg_time += time.time() - cur_time
    print(file, ":", time.time() - cur_time)

#Doc time 1: 16734.323153734207
print("Doc Time: ", time.time() - doc_time)
#Average time doc 1: 44.270538678875674
print("Average time per doc: ", avg_time / counter)

docx_time = time.time()
avg_time = 0
counter = 0

for file in os.listdir(docx_txt_folder):
    counter += 1
    cur_time = time.time()

    d = Document(os.path.join(docx_txt_folder, file))
    d.save(docx_obj_folder, file.replace('.txt', ''))

    avg_time += time.time() - cur_time
    print(file, ":", time.time() - docx_time)

#Docx time 1: 16209.639958143234
print("Docx time: ", time.time() - docx_time)
#Average time docx 1: 38.32056362634573
print("Average time per docx: ", avg_time / counter)

#Total time 1: 32943.9636118412
print("Total time: ", time.time() - total_time)
