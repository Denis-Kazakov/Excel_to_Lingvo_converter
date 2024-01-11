"""
This program completes one step of preparing glossaries for conversion into the Lingvo format.
Specifically, it identifies abbreviated forms of headwords e.g. 'Work Breakdown Structure (WBS)'
and places them into the 2nd column (abbreviations). There should be no text in the second
column as it will be overwritten!
"""

print('Enter the file name complete with the file path (e.g. D:/Current/EPO.txt)/ \n There should be no text in the second column as it will be overwritten!')
original_filename = input()
original_file = open(original_filename, 'r')

converted_filename = original_filename[:-4] + '_with abbr separated.txt'
converted_file = open(converted_filename, 'w')


entry=[line for line in original_file]


for i in entry:
    i = i.split('\t')
    i[0]=i[0].strip()
    headword = i[0]
    print(headword)
    if headword[-1] == ')':
        headword = headword.rstrip(')')
        brk = headword.rfind('(')
        L = len(headword)
        i[0] = headword[:(brk - L)]
        i[0] = i[0].rstrip()
        i[1] = headword[(brk + 1):]
        i[1] = i[1].strip()
    new = ''
    for j in i:
        new = new + '\t' + j
        new = new.lstrip('\t')
    converted_file.write(new)

original_file.close()
converted_file.close()
        

            
            
