
def build_fsm(pat,ab):
    fsm = {}
    m = len(pat)
    for a in ab:
        fsm[(0,a)] = 0
    fsm[(0,pat[0])] = 1
    brd = 0
    for j in range(1,m+1):
        print "brd", brd
        print fsm
        for a in ab:
            fsm[(j,a)] = fsm[(brd,a)]
        if j!=m:
            fsm[(j,pat[j])] = j+1
        brd = fsm[(brd,pat[j-1])]
    return fsm

def scan(txt, fsm, m):
    state = 0
    n = len(txt)
    occ = []
    for i in range(n):
        state = fsm[(state, txt[i])]
        if state == m: #bip
            occ.append (i-m+1)
    return occ

def main():
    ab = [chr(i) for i in range(256)]
    pat = "church"
    fsm = build_fsm(pat, ab)
    txt = "diogo went to the churchurch to study the church-turing thesis"
    #txt = "church"
    occ = scan(txt, fsm, len(pat))
    print occ


if __name__ == "__main__":
    main()
