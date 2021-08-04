import csv

def deleteFromFileById(id,path):
    projects_file = open(path, "r")
    lines = projects_file.readlines()
    projects_file.close()
    #supprimer ligne
    index = findFromFileById(id,path)
    if index < 0:
        return 'Erreur de suppression '
    
    del lines[index]
    #reecrir fichier apres suppression ligne
    new_file = open(path, "w+")
    for line in lines:
        new_file.write(line)
    new_file.close()
    return ''
        



def findFromFileById(id, path):
    with open(path, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        line_count = -1
        for row in reader:
                line_count +=1
                if id == row[0]: # if the username shall be on column 3 (-> index 2)
                    print ('existe dans la colon N '+str(line_count))
                    return line_count
    print ('projet non trouvée ID= '+str(id))
    return -1
