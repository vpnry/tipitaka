
'''
Split the file into smaller parts

Enable AndrOpen OpenOffice (Android app)
inserts File
'''

f = 'min_tipitaka_freq.txt'

def countLine(f):
    n = 0
    for i in open(f, 'r', encoding='utf-8'):
        n += 1
    return n

def splitF(f):
    s = ''
    fin = open(f, 'r', encoding='utf-8')
    brek = int(countLine(f)/20)
    i = 0
    n = 0
    p = ''
    for line in fin:
        if i == brek:
            n += 1
            fn = 'p' + str(n)+'.txt'
            s += '**' + fn +': '+ p[0:50].strip() + '\n\n'
            f = open(fn, 'w', encoding='utf-8')
            f.write(p)
            f.close()
            p = ''
            print(line)
            print('Saved file:', n)
            i = 0
        p += line.strip() +'\n'
        i += 1
    n +=1
    k = open('p' +str(n)+'.txt', 'w', encoding='utf-8')
    k.write(p)
    k.close()
    fin.close()
    
    open('s.txt', 'w').write(s)

splitF(f)

print('Done')