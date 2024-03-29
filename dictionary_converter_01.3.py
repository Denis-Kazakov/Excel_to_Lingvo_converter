"""This program converts a TXT file (made from a glossary in Excel beforehand) into a DSL file that can be converted into
an LSD file by Lingvo converter and used as a Lingvo dictionary.
New in this version: removing quotation marks from headwords (added by a bug in Excel to TXT conversion)marks
"""

import sys

print('Enter the file name complete with the file path (e.g. D:/Current/gold_book.txt)')
original_filename = input()
original_file = open(original_filename, 'r')


print('Enter dictionary name. This name will be used by Lingvo. This is not file name')
dict_name = input()
print("Enter source language from Lingvo's language list. E.g. English, Russian")
source_lang = input()
print("Enter target language from Lingvo's language list. E.g. English, Russian")
tgt_lang = input()

#Lingvo tag definition depending on the dictionary type (bilinqual or monolingual)
if source_lang == tgt_lang:
    colnum = 5
    opening_tag = [None, '    [trn][i]', '    [trn]', '    [ex][c darkgray]', '    [com][c]']
    closing_tag = [None, '[/i][/trn]\n', '[/trn]\n', '[/c][/ex]\n', '[/c][/com]\n']
else:
    colnum = 6
    opening_tag = [None, '    [trn][i]', '    [trn]', '    [trn][i]', '    [ex][c darkgray]', '    [com][c]']
    closing_tag = [None, '[/i][/trn]\n', '[/trn]\n', '[/i][/trn]\n', '[/c][/ex]\n', '[/c][/com]\n'] 

converted_filename = original_filename[:-3] + 'dsl'
converted_file = open(converted_filename, 'w')

# Preprocessing and checking for errors.
# 1. If an entry has an abbreviated or alternative form of the headword,
# a new entry is created with the abbreaviated/alternative form as
# the headword.
# 2. Whitespaces at the beginning and end of the headword and abbreviation
# are deleted, as these whitespaces can result in errors in DSL-to-LSD conversion.
# 3. Deleting empty entries


entry=[line for line in original_file]
for i in entry:
#Checking for paragraph breaks within entry parts. There should be none, so there should be exactly 5 tabs
# in bilinqual dictionaries or 4 tabs in monolingual dictionaries).
    if i.count('\t') < colnum - 1:
        original_file.close()
        converted_file.close()
        error_mes = 'Error. Forbidden paragraph break in the following entry: ' + i
        sys.exit(error_mes)
    if i.count('\t') > colnum - 1:
        original_file.close()
        converted_file.close()
        sys.exit('Error: too many columns in the following entry: ' + i)
    i = i.replace('""', '"')  #Replacing double double quotes (generated by a bug in Excel to TXT conversion)
    i = i.split('\t')
    tmp = i[0]
    if tmp[0] == '"':
        i[0] = i[0].strip('"') #Removing unnecessary quotes from the headword
    i[0]=i[0].strip()
    newentry = i[0]
    for j in range(1, colnum):
        i[j]=i[j].strip()
        newentry = newentry + '\t' + i[j]
    if newentry != '\t' * (colnum - 1):  #Cheking for empty entries
        converted_file.write(newentry + '\n')
    #Adding a new entry for abbreviation/alternative form of the headword
    if i[1] != '':
        tmp2 = i[1]
        if tmp2[0] == '"':
            tmp2 = tmp2.strip('"')
        i[1] = i[0]
        i[0] = tmp2
        newentry = i[0]
        for j in range(1, colnum):
            newentry = newentry + '\t' + i[j]
        converted_file.write(newentry + '\n')
converted_file.close()

#Final conversion

#Alphabetic sorting
converted_file = open(converted_filename, 'r')
oldentry=[line for line in converted_file]
entry = sorted(oldentry)
converted_file.close()

converted_file = open(converted_filename, 'w')
diclen = len(entry)
k = 1
entry_num = -1

converted_file.write('#NAME "' + dict_name + " " + source_lang[:2] + '-' + tgt_lang[:2] + '"' + '\n')
converted_file.write('#INDEX_LANGUAGE "' + source_lang + '"' + '\n')
converted_file.write('#CONTENTS_LANGUAGE "' + tgt_lang + '"' + '\n')


for i in entry:
    entry_num = entry_num + 1
    i = i.rstrip('\n')
    i = i.split('\t')
    print(i[0])
    #Comparing headword with previous entries
    if entry_num > 0:
        prev_entry = entry[entry_num-k]
        prev_entry = prev_entry.split('\t')
        prev_headword = prev_entry[0]
        if i[0] == prev_headword:
            k = k + 1
        else:
            converted_file.write(i[0] + '\n')
            k = 1
    else:
        converted_file.write(i[0] + '\n')
    for j in range(1, colnum):
        i[j] = str(opening_tag[j]) + str(i[j]) + str(closing_tag[j])
        if i[j] == str(opening_tag[j]) + str(closing_tag[j]):
            i[j] = ''
        converted_file.write(i[j])
       

original_file.close()
converted_file.close()
