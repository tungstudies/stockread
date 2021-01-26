'''
result = set()
i = 'trading $aa $BB stock market info, $aa is $116 market is doing well $cc $ABC #CEO $US $CA #ABC XDC  Auper AXDC1'

tickers = {'AA', 'ABC', 'BB', 'XDC', 'Auper', 'AXDC1'}
nontickers = {'ABC', 'CEO'}
dollar_countries = {'US', 'CA', 'AU', 'NZ', 'SG', 'TW', 'HK'}

dict_list = [{'name': 'Leah', 'age': 10}, {'name': 'Haley', 'age': 8}]
dict_dict = dict()
for item_dict in dict_list:
    popped_key = item_dict.pop('name')
    popped_value = item_dict
    dict_dict[popped_key] = popped_value
    print(dict_dict)
'''

# son_tung
#
# print(list_s)

import re

def find_m(word):
    if re.match("[^aeiou]*[aeiou]*$",word):
        print("PASS: {}".format(word))
    else:
        print("FAIL: {}".format(word))


find_m("id")
find_m("sn")
find_m("tree")
find_m("y")
find_m("by")
find_m("trouble")
find_m("oats")
find_m("trees")
find_m("ivy")
find_m("aaabbbbaaa")