import sys

def nextcolumn_orig(col, pat, a):
    m = len(pat)
    ncol = (m+1)*[0]
    for i in range(1,m+1):
        phi = 0 if a==pat[i-1] else 1
        ncol[i] = min(col[i]+1, ncol[i-1]+1, col[i-1]+phi)
    return tuple(ncol)


def nextcolumn(col, pat, a, err):
    m = len(pat)
    ncol = (m+1)*[0]
    for i in range(1,m+1):
        phi = 0 if a==pat[i-1] else 1
        ncol[i] = min(col[i]+1, ncol[i-1]+1, col[i-1]+phi, err+1)
    return tuple(ncol)


def build_fsm(pat, ab, err):
    m = len(pat)
    s = tuple(range(m+1))
    idx = 0
    queue = [(s,idx)]
    Q = {s:idx}
    F = set()
    delta = {}
    if m<=err:
        F.add(idx)
    while queue:
        (s,i) = queue.pop(0)
        for a in ab:
            snxt = nextcolumn(s, pat, a, err)
            if snxt not in Q:
                idx += 1
                Q[snxt] = idx
                queue.append((snxt,idx))
                if snxt[m]<=err:
                    F.add(idx)
            inxt = Q[snxt]
            delta[(i,a)] = inxt
    return(delta, F)


def scan(txt, fsm):
    (delta, F) = fsm
    n = len(txt)
    cur = 0
    occ = []
    for j in range(n):
        cur = delta[(cur, txt[j])]
        if cur in F:
            occ.append(j)
    return occ


def main2():
    txt = "abracadabra"
    pat = "abra"
    ab = "abcdrx"
    err = 1
    fsm = build_fsm(pat, ab, err)
    occ = scan(txt, fsm)
    print occ

def main():
    filename = sys.argv[1]
    txtfile = open(filename, "r")
    pat = sys.argv[2]
    err = int(sys.argv[3])
    count = 0
    lcount = 0
    ab = [chr(x) for x in range(256)]
    fsm = build_fsm(pat, ab, err)
    for txt in txtfile:
        #print "txt=",txt
        occ = scan(txt, fsm)
        count += len(occ)
        lcount += min(1,len(occ))
        if len(occ):
            print txt
    print "found",count,"occurrences in",lcount,"lines" 
    print "FSM has ", len(fsm[0])/len(ab), "states"

if __name__ == "__main__":
    main()
