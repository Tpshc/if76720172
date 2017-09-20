import sys


def newcolumn(col, pat, a):
    m = len(pat)
    ncol = (m+1)*[0]
    for i in range(1,m+1):
        phi = 0 if a==pat[i-1] else 1
        ncol[i] = min(col[i]+1, ncol[i-1]+1, col[i-1]+phi)
    return ncol


def sellers(txt, pat, err):
    n = len(txt)
    m = len(pat)
    col = range(m+1)
    occ = []
    for j in range(n):
        col = newcolumn(col, pat, txt[j])
        if col[m]<=err:
            occ.append(j)
    return occ


def main2():
    txt = "abracadabra"
    pat = "abra"
    err = 2
    occ = sellers(txt, pat, err)
    print occ


def main():
    filename = sys.argv[1]
    txtfile = open(filename, "r")
    pat = sys.argv[2]
    err = int(sys.argv[3])
    count = 0
    lcount = 0
    for txt in txtfile:
        #print "txt=",txt
        occ = sellers(txt, pat, err)
        count += len(occ)
        lcount += min(1,len(occ))
        if len(occ):
            print txt
    print "found",count,"occurrences in",lcount,"lines" 

if __name__ == "__main__":
    main()
