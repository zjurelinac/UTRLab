import sys

states      = sys.stdin.readline().strip().split( ',' )
inputAlpha  = sys.stdin.readline().strip().split( ',' )
trackAlpha  = sys.stdin.readline().strip().split( ',' )
empty       = sys.stdin.readline().strip()
track       = list( sys.stdin.readline().strip() )
accepted    = sys.stdin.readline().strip().split( ',' )
start       = sys.stdin.readline().strip()
i           = int( sys.stdin.readline().strip() )

delta       = dict()

for q in states:
    delta[ q ] = dict()

for t in sys.stdin:
    [ lhs, rhs ]    = t.strip().split( '->' )
    [ q, z ]        = lhs.split( ',' )
    [ p, y, d ]     = rhs.split( ',' )
    delta[ q ][ z ] = ( p, y, d )

state = start

try:
    while True:
        p, y, d     = delta[ state ][ track[ i ] ]
        track[ i ]  = y
        i          += 1 if d == 'R' else -1
        if i < 0:
            i       = 0
            break
        elif i > 69:
            i       = 69
            break
        state       = p

except KeyError:
    pass

print( state, i, ''.join( track ), int( state in accepted ), sep = '|' )

