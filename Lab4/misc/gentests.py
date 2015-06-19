import random
import subprocess
import heapq
import random

start_number = 9
base_fname = 't'
in_ext = 'in'
out_ext = 'out'
npairs = 6
lens = [15, 35, 58, 93, 123, 195] 

alphabet = ['a', 'b', 'c']
def rand_str(nchars):
    return ''.join(random.choice(alphabet) for _ in range(nchars))

def gen(nchars, in_name, out_name, expect):
    print('generating nchars={} in_name={} out_name={} expect={}'.format(nchars, in_name, out_name, expect))
    while True:
        if expect == 'DA':
            s = rand_langstr(nchars-5, nchars+5)
        else:
            s = rand_str(nchars)
        with open(in_name, 'w', encoding='utf-8', newline='\n') as fin:
            fin.write(s + '\n')
        with open(in_name, 'r', encoding='utf-8', newline='\n') as fin:
            with open(out_name, 'w', encoding='utf-8', newline='\n') as fout:
                subprocess.call('Parser.py', stdin=fin, stdout=fout, shell=True)
            with open(out_name, 'r', encoding='utf-8', newline='\n') as fout:
                if fout.readlines()[-1].strip() == expect:
                    return

P = { 'S': ['aAB', 'bBA'],
      'A': ['bC', 'a'],
      'B': ['ccSbc', ''],
      'C': ['AA'], }

def check_add(s, maxlen, PQ):
    if len(s) - sum(1 for c in s if c=='B') <= maxlen:
        heapq.heappush(PQ, (len(s), s))
def is_terminal(s):
    return s.lower() == s

def genlang(maxlen):
    lang = []
    PQ = [(1, 'S')]
    while len(PQ) > 0:
        l, s = heapq.heappop(PQ)
        if is_terminal(s):
            lang.append(s)
        else:
            for i in range(l):
                if s[i].upper() == s[i]:
                    for rhs in P[s[i]]:
                        check_add(s[:i] + rhs + s[i+1:], maxlen, PQ)
                    break
    return lang

def rand_langstr(minlen, maxlen, s='S'):
    potlen = len(s) - sum(1 for c in s if c=='B')
    if potlen <= maxlen:
        if is_terminal(s):
            if potlen < minlen:
                return None
            else:
                return s
        for i in range(len(s)):
            if s[i].upper() == s[i]:
                for _ in range(3):
                    rhs = random.choice(P[s[i]])
                    cand = s[:i] + rhs + s[i+1:]
                    res = rand_langstr(minlen, maxlen, cand)
                    if res is not None:
                        return res
                break

for i in range(npairs):
    for j in range(2):
        testnum = start_number + i*2 + j
        in_name = '{}{}.{}'.format(base_fname, testnum, in_ext)
        out_name = '{}{}.{}'.format(base_fname, testnum, out_ext)

        gen(lens[i], in_name, out_name, 'DA' if (j&1) else 'NE')
