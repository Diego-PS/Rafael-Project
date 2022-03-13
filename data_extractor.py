# -*- coding: utf-8 -*-
import os
import csv

# open the file in the write mode
csv_f = open('coord_data.csv', 'w')

# create the csv writer
writer = csv.writer(csv_f)

# write a row to the csv file   
writer.writerow(['estação', 'data', 'duração', 'X', 'Y', 'Z', 'sigmaX', 'sigmaY', 'sigmaZ', 'IAR'])

def csrs (directory):
    files = os.listdir(directory)

    i = 0
    for file in files:
        
        treated_file = file
        while (ord('a') <= ord(treated_file[0]) and ord(treated_file[0]) <= ord('z')) or (ord('A') <= ord(treated_file[0]) and ord(treated_file[0]) <= ord('Z')):
            treated_file = treated_file[1:]
        
        date = treated_file[:3]
        date = int(date)

        p1, p2 = file.split('_')
        duration, file_format = p2.split('.')
        duration = int(duration)
        #print(duration)

        files[i] = (date, duration, file)
        i+=1

    files.sort()

    for file_tuple in files:
    
        date, duration, file = file_tuple
        #print(date, duration, file)
        
        f = open(directory+'/'+file, 'r')
        message = f.read()

        #print(message)

        f.close()
        lines = message.split('\n')

        #print(lines)

        lines = [line.split() for line in lines]

        IAR_line = []
        for line in lines:
            if len(line) > 0:
                if line[0] == 'IAR':
                    IAR_line = line
        
        MKR_line = []
        for line in lines:
            if len(line) > 0:
                if line[0] == 'MKR':
                    MKR_line = line

        POS_lines = []
        for line in lines:
            if len(line) > 0:
                if line[0] == 'POS':
                    POS_lines.append(line)

        X_line = []
        for line in POS_lines:
            if (line[1] == 'X'):
                X_line = line

        Y_line = []
        for line in POS_lines:
            if (line[1] == 'Y'):
                Y_line = line

        Z_line = []
        for line in POS_lines:
            if (line[1] == 'Z'):
                Z_line = line

        csv_row = [MKR_line[1], str(date), str(duration), X_line[5], Y_line[5], Z_line[5], X_line[7], Y_line[7], Z_line[7], IAR_line[1]]
        writer.writerow(csv_row)

def ibge (directory):
    files = os.listdir(directory)

    i = 0
    for file in files:
        
        treated_file = file
        while (ord('a') <= ord(treated_file[0]) and ord(treated_file[0]) <= ord('z')) or (ord('A') <= ord(treated_file[0]) and ord(treated_file[0]) <= ord('Z')):
            treated_file = treated_file[1:]
        
        date = treated_file[:3]
        date = int(date)
        #print(date)

        p1, p2 = file.split('_')
        duration, more, file_format = p2.split('.')
        duration = int(duration)
        #print(duration)

        files[i] = (date, duration, file)
        i+=1

    files.sort()

    for file_tuple in files:
        date, duration, file = file_tuple
        f = open(directory+'/'+file, 'r', encoding='latin-1')
        message = f.read()

        f.close()
        lines = message.split('\n')

        section3_2index = lines.index(' 3.2 Sessao Observada')
        station_line_idx = section3_2index+2
        station_line = lines[station_line_idx]
        station_line = station_line.split()

        section3_3index = lines.index(' 3.3 Coordenadas Estimadas na Data do Levantamento')
        X_line_idx = section3_3index+5
        Y_line_idx = section3_3index+6
        Z_line_idx = section3_3index+7
        
        X_line = lines[X_line_idx]
        X_line = X_line.split()
        
        Y_line = lines[Y_line_idx]
        Y_line = Y_line.split()

        Z_line = lines[Z_line_idx]
        Z_line = Z_line.split()

        csv_row = [station_line[4], str(date), str(duration), X_line[3], Y_line[3], Z_line[3], X_line[4], Y_line[4], Z_line[4], '']
        writer.writerow(csv_row)

while True:
    directory = input('Please insert the directory path: ')
    print(directory)

    try:
        csrs(directory)
    except:
        try:
            ibge(directory)
        except:
            print('ERROR: The files in the given directory have their name and/or content in an invalid format. Please, check if the correct path to the directory was inserted')
            input('Press ENTER to try again')
            continue

    ans = input('Would you like to extract data from another directory? (Y/N)')
    if ans == 'Y':
        continue
    else:
        input('Press ENTER to quit')
        csv_f.close()
        exit(0)