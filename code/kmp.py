import sys


def str_brd(X):
    n = len(X)
    mk = 0
    for k in range(1,n-1):
        if X[:k]==X[n-k:]:
            mk = k
    return mk
        
def brd_bf(pat):
    m = len(pat)
    brd = (m+1)*[0]
    for j in range(2,m+1):
        brd[j] = str_brd(pat[:j])
    return brd

def bruteforce(txt, pat):
    n = len(txt)
    m = len(pat)
    occ = []
    i = 0
    while i <= n-m:
        j = 0
        while j<m and txt[i+j]==pat[j]:
            j += 1
        if j==m:
            occ.append(i)
        i += 1
    return occ


def brd(pat):
    m = len(pat)
    nxt = (m+1)*[0] 
    i = 1
    j = 0
    while i+j < m:
        while i+j<m and pat[i+j]==pat[j]:
            j += 1
            nxt[i+j] = j
        i += max(1, (j-nxt[j])) 
        j = nxt[j]
    return nxt


def sbrd(pat):
    m = len(pat)
    nxt = (m+1)*[-1] 
    if m==1 or (m>0 and pat[0]!=pat[1]):
        nxt[1] = 0
    i = 1
    j = 0
    while i < m:
        #print "i=",i
        while i+j<m and pat[i+j]==pat[j]:
            j += 1
            if i+j==m or pat[j]!=pat[i+j]:
                nxt[i+j] = j
            else:
                nxt[i+j] = nxt[j]
        if j==0 and (i==m-1 or pat[0]!=pat[i+1]):
            nxt[i+1] = 0
        i = i + j - nxt[j]
        j = max (0, nxt[j])
    return nxt


def kmp(txt, pat):
    n = len(txt)
    m = len(pat)
    nxt = sbrd(pat)
    #print "nxt=", nxt
    occ = []
    i = 0
    j = 0
    while i <= n-m:
        while j<m and txt[i+j]==pat[j]:
            j += 1
        #print txt
        #print "%s%s%s"%(i*" ",j*"=","!" if j<m else "")
        #print "%s%s"%(i*" ",pat)
        #print "%s%s"%(i*" ",nxt[j]*"-")
        #print
        if j==m:
            occ.append(i)
        #print "skipping ", max(1, (j-nxt[j]))
        i += max(1, (j-nxt[j])) 
        j = max(0, nxt[j])
    return occ

def main():
    filename = sys.argv[1]
    txtfile = open(filename, "r")
    pat = sys.argv[2]
    count = 0
    lcount = 0
    for txt in txtfile:
        #print "txt=",txt
        occ = kmp(txt, pat)
        count += len(occ)
        lcount += min(1,len(occ))
        if len(occ):
            print txt
    print "found",count,"occurrences in",lcount,"lines" 

if __name__ == "__main__":
    main()
