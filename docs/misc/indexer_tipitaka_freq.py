"""Generate tipitaka pali word frequency & consonant case.

This code file is in public domain. No warranties!
https://github.com/vpnry/tipitaka/misc

Date:
    v1.0, 24 May 2021 last updated: 02 June 2021

Required input:
    filecode_map.py and its listed filenames
    
Output:
    frequency dict and consonant cases in descending order
"""

import re
import time
from os.path import isfile
from filecode_map import FCODE

FILEDIR = "mula/" # Dir of pali files
FILE_ENDWITH = "*" # Index all files
FILE_ENDWITH = "mul.html.txt" # Index only some files ending with this str

#  --------------- indexer  ---------------

def zfill_freq(wordDict, w, i=0):
    """Fill zero before sorting number."""
    
    w = w.rstrip("*").strip()
    n = wordDict[w][i]
    return str(n).zfill(6)

def count_word_freq(filedict, filterFile="*"):
    """Return unsorted word frequency dict: word: [freq, filecode]."""
    
    dic = {}
    n = 0
    wordRegex = re.compile('[a-zA-ZāīūṁṃṇḍḷṛṣśṭñṅĀĪŪṀṂṆḌḶṚṢŚṬÑṄ]+')
    for f, fileinfo in filedict.items():
        
        if filterFile != "*":
            if not f.endswith(filterFile): continue
        
        # Visuddhimagga: e0101n e0102n
        if filterFile == "mul.html.txt" and f.endswith(("e0101n.mul.html.txt","e0102n.mul.html.txt")):
            continue
        
        n += 1
        # if n == 2: break
        
        with open(FILEDIR + f, 'r') as fin:
            for line in fin:
                words = wordRegex.findall(line.lower())
                for word in words:
                    if word in dic:
                        dic[word][0] = dic[word][0] + 1
                        # Filecode is string, starting from index pos 1
                        if not fileinfo[0] in dic[word][1:]:
                            dic[word].append(fileinfo[0])
                    else:
                        dic[word] = [1, fileinfo[0]]
        print("Processed", n, f)
    
    print("Processed total:", n, "files")
    return dic

def save_word_freq(dic, freqFilename, sortFreqInDescOrder =True):
    """Sort & save word frequency dictionary."""
    
    writeText ="""
# Tipitaka pali word frequency in descending order.

# Counted unique words or tokens: {totalw}
# For free distribution only - https://github.com/vpnry/tipitaka/misc

# Data indexed using VRI version (2020) http://tipitaka.org
# Items: word: frequency, filecodes of files where the word occured
# For mapped filecodes and tiles, filenames see: filecode_map.py

""".format(totalw = len(dic))

    writeText = ""
    if sortFreqInDescOrder:
        wordListSorted = sorted(dic, key=lambda w: zfill_freq(dic,w), reverse=True)
    else:
        wordListSorted = sorted(dic, key=lambda w: zfill_freq(dic,w), reverse=False)

    for w in wordListSorted:
        winfo = dic[w]
        fcodeString = ""
        for i in winfo:
            fcodeString += str(i) + ","
        fcodeString = fcodeString.rstrip(",") # right strip last ","
        writeText += w + ": " + fcodeString +"\n"
    
    with open(freqFilename, "w") as f:
        f.write(writeText)
    print("Saved", freqFilename,"\n")

def get_word_freq_dict(freqFilename = "tipitaka_freq.txt", onefilecode=True):
    """Indexing word frequency afresh or parsing data from the saved file.
    
    When parsing, only the first file code is kept since it is enough for 
    listing consonant cases. For full filecode list, set onefilecode = False
    """
    
    dic = {}
    if FILE_ENDWITH != "*":
        freqFilename = FILE_ENDWITH[0:1] + "_" + freqFilename
    
    if not isfile(freqFilename):
        print("Counting word frequency afresh...")
        dic = count_word_freq(FCODE, filterFile = FILE_ENDWITH)
        print("\nCounting done:", "=> Dict size:", len(dic))
        save_word_freq(dic, freqFilename)
    else:
        try:
            # read text file, build a dictionary again 
            dic = {}
            fin = open(freqFilename, 'r')
            for line in fin:
                line = line.strip()
                if len(line) < 1:
                    continue
                if line.startswith("#"):
                    continue
                idx = line.find(": ")
                if idx < 0:
                    print("Mal-format: line has no ': '", line)
                    continue
                lines = line.split(": ")
                if len(lines) > 2:
                    print("Mal-format: line has multi ': '", line)
                    continue
                
                word = lines[0].strip()
                val = lines[1].split(",")
                
                # cut short 1 file code
                if onefilecode:
                    val = val[0:2]
                dic[word] =  val
            fin.close()
        except:
            print("Something went wrong when parsing", freqFilename)
            return {}
        print("Parsed", freqFilename, "=> Dict size:", len(dic))
        print("")
    
    return dic

#  --------------- extract consonant task ---------------
def find_consonant_case(wordDict):
    """Find possible consonant cases, its frequency and return unsorted dict."""
    
    if len(wordDict) < 1:
        print("Word frequency dict is empty.")
        return {}
    
    conRegex = re.compile('(?:[kghcjtdpbmnyrvlshṁṃṇḍḷṛṣśṭñṅṀṂṆḌḶṚṢŚṬÑṄ]){2,}')
    
    # kh, (gh, and so on) is just a single consonant (with 2 consonant chars)
    # this is a confusing render of pali Roman script so we ignore these cases
    
    exceptConsLis = "kh,gh,ch,jh,ṭh,ḍh,th,dh,ph,bh".split(",")
    
    conCaseDict = {}
    for w, v in wordDict.items():
        # a pali word should always end with a vowel. So no ending con case.
        conList = conRegex.findall(w)
        for c in conList:
            if not c in exceptConsLis:
                conCaseDict[c] = conCaseDict.get(c, 0) + int(v[0])
    
    print("Total consonant cases:", len(conCaseDict))
    
    return conCaseDict

def code_to_title(filecode_list):
    """Transform code to title in ascending order."""
    
    temp = [str(n).zfill(6) for n in filecode_list]
    temp.sort()
    code2name = {v[0]:v[2] for _, v in FCODE.items()}
    res = ""
    for i in temp:
        ilstrip = str(i.lstrip('0'))
        res += '['+ ilstrip +']: ' + code2name.get(ilstrip, "?") + '\n\n'
    
    return res.replace('.html.txt', '.html')

def save_con_case_sample(wordDict, conCaseDict, conCaseSortedList, sampleDict, caseFilename="tipitaka_cons.txt"):
    """Sort & save consonant case to disk."""

    st = "\nTotal cases:" + str(len(conCaseSortedList)) +"\n\n"
    st += "Case: word [filecode of the file where this word appeared]\n"
    st += "A word followed by a * shows that it has been used as a sample in a former case.\n\n"
    
    fcodeLis = []
    lineNumber = 0
    for k in conCaseSortedList:
        lineNumber += 1
        tempt = ""
        kinfo = sampleDict.get(k, [])
        if len(kinfo) < 1:
            print("Case has no word sample:", k)
            continue
        
        # Sort again, since there are reused words appended
        kinfo = sorted(kinfo, key=lambda w: zfill_freq(wordDict, w), reverse=True)
        
        for word in kinfo:
            _word = word
            # remove * in starred word
            word = word.rstrip("*").strip()
            wfilecodes = wordDict.get(word, ["_", "?"])
            if len(wfilecodes) < 2:
                print("Error: Word has no filecode", word)
            
            # a single file code (1st) is enough
            fcode = wfilecodes[1]
            
            # _fcode = wfilecodes[0]
            # tempt += str(_word) + str(_fcode) + " [" + str(fcode) + "] "
            tempt += str(_word) + " [" + str(fcode) + "] "
            
            if not fcode in fcodeLis:
                fcodeLis.append(fcode)
            
        st += str(lineNumber) + ". " + str(k) + ": " + tempt.strip() + "\n\n"
    
    ref = code_to_title(fcodeLis)
    st += "\n\n-------- file code -------- \n" + ref
    st += "\n\n-------- consonant case and repeated time -------- \n\n"
    
    breakline = 0
    for k in conCaseSortedList:
        breakline += 1
        st += "{case}: {repik}, ".format(case=k, repik=conCaseDict[k])
        if breakline == 8:
            st += "\n\n"
            breakline = 0
    st += "\n\n"
    
    caseFilenamePrefix = caseFilename
    if FILE_ENDWITH != "*":
        caseFilenamePrefix = FILE_ENDWITH[0:1] + "_" + caseFilename
    
    with open(caseFilenamePrefix, "w") as f:
        f.write(st)
    print("Saved", caseFilenamePrefix)

def count_dict_val(dic):
    n = 0
    for _,v in dic.items():
        if len(v) > 0: n +=1
    return n

def append_sample(case, sample, wordListSorted, usedWordsList, sampleDict):
    """Add words to sampleDict and usedWordsList."""
    
    for word in wordListSorted:
        if len(sampleDict.get(case,[])) == sample: break
        if (case in word) and (not word in usedWordsList):
            sampleDict.setdefault(case, []).append(word)
            usedWordsList.append(word)

def get_con_sample(sample=5, savefile = True):
    """Get word samples for consonant cases. May take a few minutes."""
    
    wordDict = get_word_freq_dict() # 961622
    wordListSorted = sorted(wordDict, key=lambda w: zfill_freq(wordDict, w),reverse=True)

    conCaseDict = find_consonant_case(wordDict)
    # single number, not [], cannot use zfill_freq
    conCaseSortedList = sorted(conCaseDict, key=lambda c: str(conCaseDict[c]).zfill(6),reverse=True)

    usedWordsList = []
    sampleDict = {}
    
    # Step 1: Avoid reusing words in samples
    for case in conCaseSortedList:
        
        # Important: should set all cases value to empty [] first
        # to make sure that all cases are present in the sampleDict.
        # Otherwise some cases will be missed also in the second round when reusing
        # used words.
        # Because a word can have multi consonant cases within it.
        # So in the first round, a preceding case uses that word as a word sample
        # and prevent the succeeding cases using it.
        sampleDict.setdefault(case, [])
        
        if len(sampleDict.get(case,[])) == sample: continue
        # Seem to run faster a bit when moving code to this append_sample func
        append_sample(case, sample, wordListSorted, usedWordsList, sampleDict)
    
    # Step 2: When it could not get enough required samples, try reusing used words
    # A reused word will be marked with a *
    
    for case in conCaseSortedList:
        caseinfo = sampleDict.get(case, [])
        if len(caseinfo) == sample: continue
        # print("\nBefore re-use", case, caseinfo)
        for word in usedWordsList:
            if len(sampleDict.get(case, [])) == sample: break
            if case in word:
                if not word in sampleDict.get(case, []):
                    starredWord = word + " *"
                    sampleDict.setdefault(case, []).append(starredWord)
        # print("After re-use", case, sampleDict[case], "\n")
    
    print("Cases filled with samples:", count_dict_val(sampleDict), "/", len(conCaseDict))

    if savefile:
        save_con_case_sample(wordDict, conCaseDict, conCaseSortedList, sampleDict)
    print("Extracting consonant cases is done.")
    
    # return sampleDict



t1 = time.time()
"""
for i in ["*", "mul.html.txt"]:
    FILE_ENDWITH = i
    get_con_sample()
"""
get_con_sample()
print("\nDone. Took:", time.time() - t1, "seconds\n")
















# def index_con_freq_debug(filedict=FCODE, filterFile=FILE_ENDWITH):
#     """Return unsorted con frequency dict: con: [freq, filecode(s)]"""
    
#     dic = {}
#     n = 0
#     conRegex = re.compile('(?:[kghcjtdpbmnyrvlshṁṃṇḍḷṛṣśṭñṅṀṂṆḌḶṚṢŚṬÑṄ]){2,}')
#     exceptConsLis = "kh,gh,ch,jh,ṭh,ḍh,th,dh,ph,bh".split(",")
#     for f, fileinfo in filedict.items():
#         if filterFile != "*":
#             if not f.endswith(filterFile): continue
#         # Visuddhimagga: e0101n e0102n
#         if filterFile == "mul.html.txt" and f.endswith(("e0101n.mul.html.txt","e0102n.mul.html.txt")):
#             continue
#         n += 1
#         # if n == 2: break
#         fin = open(FILEDIR + f)
#         for line in fin:
#             cons = conRegex.findall(line.lower())
#             for con in cons:
#                 if con in exceptConsLis: continue
#                 if con in dic:
#                     dic[con][0] = dic[con][0] + 1
#                     if not fileinfo[0] in dic[con][1:]:
#                         dic[con].append(fileinfo[0])
#                 else:
#                     dic[con] = [1, fileinfo[0]]
#         fin.close()
#         # print("Indexed", n, f)
#     print("Indexed total:", n, "files")
#     save_word_freq(dic, str(time.time()) +"_con_debug.txt")
#     return dic


