import re,io,os.path,os
def remove_tag(str):
    alldigit = re.compile(r"^<.+")
    if alldigit.search(str) != None:
        return False
    return True




for line in open('./../text_list', "r"):
    filename = './../TXT/tragedies/'+line.rstrip()
    print filename
    f = open("./../TXT/test_"+line.rstrip(),"w")
    for line in io.open(filename,"r",encoding="utf-16"):
        if remove_tag(line):
            # remove signiture
            line = re.sub(re.compile("[!-/:-@[-`{-~;?]"),"", line).rstrip()
            # print line
            f.write(line.encode('utf-8'))

    f.close()
