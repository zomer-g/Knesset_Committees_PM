#create list of local files
files_list2 = open("urls.txt", "r")

files = []
for line in files_list2:
    s_line = line.replace('https://fs.knesset.gov.il//24/Committees/','').replace('https://fs.knesset.gov.il/24/Committees/','')
    files+=s_line.split()

files_list2.close()




#print(files)

from docx import Document

all_lists = []
titles = ['חברי הוועדה: ', 'חברי הכנסת:', 'חבר הוועדה: ', 'חבר הכנסת:', 'חברת הוועדה: ', 'חברת הכנסת:','חברות הוועדה: ', 'חברות הכנסת:']


# function that the input is the name of the local file and the name of the title of the relevant section in the text. The function finds the title in each file and starts writing the lines after until a blank line. The output is a dictionary with ther name of the file, name of the title and list of the lines after the title.
def name_list_f(f_file, titles):
    protocol_dict = {}
    protocol_dict['file'] = f_file
    doc = Document(f_file)

    colleting_names = False
    current_title = []
    names = []
    for p in doc.paragraphs:
        if p.text in titles:
            # new title found - move to collecting mode
            colleting_names = True
            names = []
            current_title = p.text
            continue  # no need to continue the loop
        if p.text == '' and colleting_names:
            # finished collecting names
            protocol_dict['title'] = current_title  # put the names in the dict
            protocol_dict['names'] = names
            # reset names and continue
            names = []
            colleting_names = False
        if colleting_names:
            # we are in collecting names mode
            names.append(p.text)

    return protocol_dict


# running the function on a list of files and titles  and write all the dicts on a list (each object in the list is dict with 3 keys: file, tittle, list of names/lines)
for file in files:

    all_lists.append(name_list_f(file, titles))



import csv

to_csv = all_lists

keys = to_csv[0].keys()

with open('PM_protocol_final.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(to_csv)






