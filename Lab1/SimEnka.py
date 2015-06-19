import sys

def epsilonSurround( qs, delta ):
    opened = list( qs )
    visited = set()

    while opened:
        q = opened.pop()
        visited.add( q )
        for x in delta[ q ][ '$' ]:
            if not x in visited:
                opened.append( x )

    return visited


def step( qs, delta, a ):
    nqs = set()
    for q in qs:
        if a in delta[ q ]:
            nqs |= set( delta[ q ][ a ] )
    return nqs

inputs      = sys.stdin.readline().strip()
allStates   = sys.stdin.readline().strip()
alphabet    = sys.stdin.readline().strip()
accepted    = sys.stdin.readline().strip()
start       = sys.stdin.readline().strip()

transitions = dict()

for s in allStates.split( ',' ):
    transitions[ s ] = dict( { '$' : [] } )

for l in sys.stdin:
    [ t, tq ]   = l.strip().split( '->' )
    [ q, a ]    = t.split( ',' )
    nq          = tq.split( ',' )

    if nq != [ '#' ]:
        transitions[ q ][ a ] = nq

for t in inputs.split( '|' ):
    ins     = t.split( ',' )
    states  = set( [ start ] )
    output  = []

    for a in ins:
        states  = epsilonSurround( states, transitions )
        out     = ','.join( sorted( states ) )
        output += [ '#' ] if not out else [ out ]
        states  = step( states, transitions, a )

    states  = epsilonSurround( states, transitions )
    out     = ','.join( sorted( states ) )
    output += [ '#' ] if not out else [ out ]

    print( '|'.join( output ) )

