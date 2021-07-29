import csv
import constants as cs

def delete(id):
    a_file = open(cs.PROJECT_FILE_PATH, "r")
    lines = a_file.readlines()
    a_file.close()
    #supprimer ligne
    del lines[find(id)]
    #reecrir fichier apres suppression ligne
    new_file = open(cs.PROJECT_FILE_PATH, "w+")
    for line in lines:
        new_file.write(line)
    new_file.close()
    return ''


def find(id):
    with open(cs.PROJECT_FILE_PATH, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        line_count = -1
        line_found = -1
        for row in reader:
                line_count +=1
                if id == row[0]: # if the username shall be on column 3 (-> index 2)
                    print ('existe dans la colon N '+str(line_count))
                    line_found = line_count
    return line_found


