def min_range(li):
    len_input = len(li)
    if len_input < 1:
        print('Empty list of filecodes', li)
        return ''
    st = []
    li = sorted(li, key=lambda k:str(k).zfill(3), reverse=False)
    
    st.append(int(li.pop(0)))
    temp = st[-1]
    n =''
    while len(li) > 0:
        n = int(li.pop(0))
        if temp + 1 == n:
            temp = n
            continue
        if temp == st[-1]:
            st.append(',')
            st.append(n)
            temp = n
        else:
            st.append('-')
            st.append(temp)
            st.append(',')
            st.append(n)
            temp = n

    if len_input != 1:
        if st[-1] != n:
            st.append('-')
            st.append(n)

    res = ''
    for i in st: res += str(i)
    return res


def parse_line(line):
    st = ''
    lines = line.split(': ')
    nums = lines[1].strip(',').split(',')
    st += lines[0] + ': ' + nums[0] + ','
    
    fcodes = nums[1:]
    if len(fcodes) < 1: print('Bad line', line)
    return st + min_range(fcodes)


def fmin(f):
    fin = open(f)
    tex = ''
    for line in fin:
        line = line.strip()
        if len(line) < 1: continue
        tex += parse_line(line) +'\n\n'
    open('min_' + f, 'w').write(tex)
    print("Done")


fmin('tipitaka_freq.txt')
fmin('m_tipitaka_freq.txt')

