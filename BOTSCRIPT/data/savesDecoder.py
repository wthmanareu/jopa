def encode(lvl):
    sp = []
    for i in lvl.split(';'):
        sp2 = []
        for j in i.split(','):
            sp2.append(int(j))
        sp.append(sp2)
    return sp


def decode(lvl):
    sp = []
    for i in lvl:
        txt = ','.join(list(map(str, i)))
        sp.append(txt)
    return ';'.join(sp)