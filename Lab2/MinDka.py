import sys


def isEquiv( p, q, d ):
    return ( ( p in d ) and ( q in d ) ) or ( ( not p in d ) and ( not q in d ) )

def transition( p, q, a, tr ):
    np, nq = tr[ p ][ a ], tr[ q ][ a ]
    return min( np, nq ), max( np, nq )

def markIneq( p, d, e ):
    for w in d[ p ]:
        if e[ w ]:
            e[ w ] = False
            markIneq( w, d, e )



statesStr   = sys.stdin.readline().strip()
alphabetStr = sys.stdin.readline().strip()
acceptedStr = sys.stdin.readline().strip()
start       = sys.stdin.readline().strip()

alphabet    = alphabetStr.split( ',' )
states      = statesStr.split( ',' )
accepted    = set( acceptedStr.split( ',' ) )

equiv       = dict()
dependency  = dict()
transitions = dict()

for p in states:
    transitions[ p ] = dict()

for l in sys.stdin:
    [ t, nq ]   = l.strip().split( '->' )
    [ q, a ]    = t.split( ',' )
    transitions[ q ][ a ] = nq

opened      = [ start ]
reachable   = set()

while opened:
    p = opened.pop()
    reachable.add( p )

    for a, q in transitions[ p ].items():
        if not q in reachable:
            opened.append( q )

states = [ s for s in states if s in reachable ]
accepted = { s for s in accepted if s in reachable }

for p in states:
    for q in states:
        if p == q:
            equiv[ ( p, p ) ] = True
            continue
        if p > q: continue
        equiv[ ( p, q ) ] = isEquiv( p, q, accepted )
        dependency[ ( p, q ) ] = []


for p in states:
    for q in states:
        if p >= q: continue

        for a in alphabet:
            np, nq = transition( p, q, a, transitions )
            if not equiv[ ( np, nq ) ]:
                equiv[ ( p, q ) ] = False
                markIneq( ( p, q ), dependency, equiv )
                break

        if equiv[ ( p, q ) ]:
            for a in alphabet:
                np, nq = transition( p, q, a, transitions )
                if np != nq:
                    dependency[ ( np, nq ) ].append( ( p, q ) )


ntrans = dict()
replacement = dict()

for p in states:
    replacement[ p ] = p

uEquiv = sorted( [ k for k, v in equiv.items() if v and k[ 0 ] != k[ 1 ] ] )

for ( p, q ) in uEquiv:
    replacement[ q ] = replacement[ p ]
    if q in states:
        states.remove( q )
    accepted.discard( q )
    if start == q:
        start = p

for p in states:
    for a, q in transitions[ p ].items():
        ntrans[ ( p, a ) ] = replacement[ q ]


print( ','.join( states ) )
print( alphabetStr )
print( ','.join( sorted( accepted ) ) )
print( start )

for ( p, a ), q in sorted( ntrans.items() ):
    print( p + ',' + a + '->' + q )
