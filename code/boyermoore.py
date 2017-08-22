import sys

def badchar(pat, ab):
    l = len(ab)
    m = len(pat)
    bc = l*[-1]
    for i in range(m):
        bc[ab.index(pat[i])] = i 
    return bc


def goodsuffix(pat):
    m = len(pat)
    gs = (m+1)*[-1]
    for j in range(-1,m):
        for k in range(m):
            if (k<=(m-j-1) and pat[:k]==pat[m-k:]) or (k>(m-j-1) and pat[j+1:]==pat[k-(m-j-1):k]):
                gs[j+1] = k
    return gs


def boyermoore(txt, pat, ab):
    m, n, l = len(pat), len(txt), len(ab)
    occ = []
    bc = badchar(pat,ab)
    gs = goodsuffix(pat)
    #print "gs=",gs
    i = 0
    while i+m <= n:
        j = m-1
        while j>=0 and txt[i+j] == pat[j]:
            j -= 1
        #print txt
        #print "%s%s%s"%((i+j)*" " if j>=0 else i*" " , "!" if j>=0 else "",(m-j-1)*"=")
        #print "%s%s"%(i*" ",pat)
        #print
        if j<0:
            occ.append(i)
            i+= m-gs[0]
        else:
            i += max(m-gs[j+1], j-bc[ab.index(txt[i+j])]) 
    return occ

def oldmain():
    ab = [chr(i) for i in range(256)]
    pat = "beauty"
    txt = "That thereby beauty's rose might never die,"
    occ = boyermoore(txt, pat, ab)
    print occ

def main():
    ab = [chr(i) for i in range(256)]
    filename = sys.argv[1]
    txtfile = open(filename, "r")
    pat = sys.argv[2]
    lcount= 0
    count = 0
    for txt in txtfile:
        #print "txt=",txt
        occ = boyermoore(txt, pat, ab)
        count += len(occ)
        lcount += min(1,len(occ))
        if len(occ):
            print txt
    print "found",count,"occurrences in",lcount,"lines"
    

if __name__ == "__main__":
    main()
