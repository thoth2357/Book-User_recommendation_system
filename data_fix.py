with open('Books.csv','r', encoding='ISO-8859-1') as csv_file:
    ...:     for strline in csv_file.readlines():
    ...:         if len(strline[:-1].split(';')) != 8:
    ...:             print(strline[:-1].split(';'))
    ...:             print(f'{strline}')
    ...:             fixed = re.sub(r';\b',' ', strline).split(';')
    ...:             print(fixed)
    ...:             break
    
with open('Books.csv','r', encoding='ISO-8859-1') as csv_file:
    ...:     for strline in csv_file.readlines():
    ...:         if len(strline[:-1].split(';')) != 8:
    ...:             print(strline[:-1].split(';'))
    ...:             print(f'{strline}')
    ...:             fixed = re.sub(r';\B',' ', strline).split(';')
    ...:             print(fixed)
    ...:             break
    
with open('Books.csv','r', encoding='ISO-8859-1') as csv_file:
    ...:     for strline in csv_file.readlines():
    ...:         if len(strline[:-1].split(';')) != 8:
    ...:             print(strline[:-1].split(';'))
    ...:             print(f'{strline}')
    ...:             fixed = re.sub(r';\B:',' ', strline).split(';')
    ...:             print(fixed)
    ...:             break
    
for match in re.finditer(r'[a-zA-Z];' , sentence3):
    ...:     count += 1
    ...:     print("match", count, match.group(), "start index", match.start(), "End index", ma
    ...: tch.end())
    
##FiNAL
with open('Books.csv','r', encoding='ISO-8859-1') as csv_file:
    ...:     for strline in csv_file.readlines():
    ...:         if len(strline[:-1].split(';')) != 8:
    ...:             print(strline[:-1].split(';'))
    ...:             print(f'{strline}')
    ...:             fixed = re.sub(r';\B',' ', strline).split(';')
    ...:             print(fixed)
    ...:             for match in re.finditer(r'[a-zA-Z];', str(strline)):
    ...:                 print(match.end())
    ...:                 print(str(strline)[match.end()])
    ...:                 strline = str(strline[:match.end()-1]) + str(strline[match.end()+1:])
    ...:                 print(strline.split(';'), len(strline.split(';')))
    ...:             break