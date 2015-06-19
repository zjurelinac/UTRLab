import sys


def fail():
    print( "\nNE" )
    sys.exit()


def pS( l ):
    print( 'S', end = '' )
    x = l.pop( 0 )
    if x == 'a':
        pA( l )
        pB( l )
    elif x == 'b':
        pB( l )
        pA( l )
    else: fail()


def pA( l ):
    print( 'A', end = '' )
    x = l.pop( 0 )
    if x == 'a':
        return
    elif x == 'b':
        pC( l )
    else: fail()


def pB( l ):
    print( 'B', end = '' )
    if not l or l[ 0 ] != 'c': return
    if l.pop( 0 ) != 'c': fail()
    if l.pop( 0 ) != 'c': fail()
    pS( l )
    if l.pop( 0 ) != 'b': fail()
    if l.pop( 0 ) != 'c': fail()


def pC( l ):
    print( 'C', end = '' )
    pA( l )
    pA( l )


input = list( sys.stdin.readline().strip() )

try:
    pS( input )
except Exception as e:
    fail()

if input: fail()

print( "\nDA" )
