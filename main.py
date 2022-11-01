import json
import os

files = os.listdir("data/publico")
files.sort()
print(files[-1])
# for file in files[0: 70_000: 1_000]:
#     with open(f"data/publico/{file}") as fin:
#         content = json.load(fin)
#
#     print(content["data"])
