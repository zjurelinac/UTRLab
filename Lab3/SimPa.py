import sys

def writeStack( s ):
    return '#' + ( '$' if not s else ''.join( reversed( s ) ) ) + '|'

def jump( q, i, s, d ):
    Z = s.pop()
    p, Y = d[ q ][ ( i, Z ) ]
    if Y == '$': Y = ''
    s += reversed( Y )
    return p

inputs      = [ s.split( ',' ) for s in sys.stdin.readline().strip().split( '|' ) ]
states      = sys.stdin.readline().strip().split( ',' )
alphaIn     = sys.stdin.readline().strip().split( ',' )
alphaSt     = sys.stdin.readline().strip().split( ',' )
accepted    = sys.stdin.readline().strip().split( ',' )
start       = sys.stdin.readline().strip()
startStack  = list( sys.stdin.readline().strip() )

delta       = dict()

for q in states:
    delta[ q ] = dict()

for l in sys.stdin:
    [ lhs, rhs ]    = l.strip().split( '->' )
    [ q, a, Z ]     = lhs.split( ',' )
    [ p, Y ]        = rhs.split( ',' )
    delta[ q ][ ( a, Z ) ]   = ( p, Y )

stack = []


for ins in inputs:
    state       = start
    stack[:]    = startStack
    broken      = False
    ins         = list( reversed( ins ) )

    try:
        while ins:
            print( state + writeStack( stack ), end = '' )
            s = stack[ -1 ]
            i = ins[ -1 ]

            if ( i, s ) in delta[ state ]:
                state = jump( state, i, stack, delta )
                ins.pop()
            elif ( '$', s ) in delta[ state ]:
                state = jump( state, '$', stack, delta )
            else:
                print( 'fail|0' )
                broken = True
                break

        if broken: continue

        while stack:
            s = stack[ -1 ]
            print( state + writeStack( stack ), end = '' )

            if state in accepted: break

            if ( '$', s ) in delta[ state ]:
                state = jump( state, '$', stack, delta )
            else: break

        if not stack:
            print( state + writeStack( stack ), end = '' )

        print( int( state in accepted ) )

    except IndexError:
        print( 'fail|0' )
