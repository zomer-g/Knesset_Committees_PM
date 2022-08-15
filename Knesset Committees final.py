#In order to run the code, you need to download from KNESSET ODATA the table that includes the names of the protocol files (DOC)
#The list is here http://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_DocumentCommitteeSession

#After downloading the relevant files locally, create a text file that containing the file names (or the file names with the server address as write in the ODATA file) called urls.txt.
#The output is a CSV file PM_protocol.csv that includes the names of all the PMs for each protocol. Also, a CSV called P_to_p.csv that does not include a list, making it easier to analyze with Google Sheets.


#create list of local files
files_list2 = open("urls.txt", "r")

files = []
for line in files_list2:
    s_line = line.replace('https://fs.knesset.gov.il//24/Committees/','').replace('https://fs.knesset.gov.il/24/Committees/','')
    files+=s_line.split()

files_list2.close()


from docx import Document

all_lists = []
titles = ['חברי הוועדה: ', 'חברי הכנסת:', 'חבר הוועדה: ', 'חבר הכנסת:', 'חברת הוועדה: ', 'חברת הכנסת:','חברות הוועדה: ', 'חברות הכנסת:']


# function that the input is the name of the local file and the name of the title of the relevant section in the text. The function finds the title in each file and starts writing the lines after until a blank line. The output is a dictionary with ther name of the file, name of the title and list of the lines after the title.
def name_list_f(f_file, titles):
    protocol_dicts_list = []
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
            # finished collecting names - save to dictionary
            d = {}
            d['file'] = f_file
            d['title'] = current_title
            d['names'] = names
            protocol_dicts_list.append(d)
            # reset names and continue
            names = []
            colleting_names = False
        if colleting_names:
            # we are in collecting names mode
            names.append(p.text)

    return protocol_dicts_list




# running the function on a list of files and titles and write all the dicts on a list (each object in the list is dict with 3 keys: file, tittle, list of names/lines)
for file in files:

    all_lists += name_list_f(file, titles)

#export the list of protocols with the names of the PM as a list
import csv

to_csv = all_lists

keys = to_csv[0].keys()

with open('PM_protocol.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(to_csv)
    output_file.close()

#Convert the list of the names to new lines so it easier to analyze with Google Sheets.
P_to_p=[]
for i in all_lists:
    for j in i['names']:
        PM_to_protocol = {}
        #print(j)
        #print(i['file'])
        PM_to_protocol['file']=i['file']
        PM_to_protocol['title'] = i['title']
        PM_to_protocol['name'] = j
        P_to_p.append(PM_to_protocol)

keys = P_to_p[0].keys()

with open('P_to_p.csv', 'w', newline='', encoding='utf-8') as output_file3:
    dict_writer = csv.DictWriter(output_file3, keys)
    dict_writer.writeheader()
    dict_writer.writerows(P_to_p)
    output_file3.close()

