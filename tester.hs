import Data.List
import System.Cmd
import System.Directory
import System.Environment

runDiff :: String -> IO ()
runDiff fout = do
    b <- readFile fout
    c <- readFile "test.c"
    putStrLn ( if b == c then "Test ok" else "Wrong answer" )

runTest :: String -> String -> String -> String -> String -> String -> IO ()
runTest prog base fin fout ver folder = do
    let interpreter = ( if ver == "2" then "python2.7" else "python3" )
    setCurrentDirectory folder
    system ( interpreter ++ " " ++ base ++ "/" ++ prog ++ " < " ++ fin ++ " > test.c"  )
    runDiff fout
    removeFile "test.c"
    setCurrentDirectory ".."

main :: IO ()
main = do
    [ prog, fin, fout, ver ]    <- getArgs
    base        <- getCurrentDirectory
    folders'    <- getDirectoryContents "tests"
    let folders = sort folders'
    setCurrentDirectory "tests"
    mapM_ ( runTest prog base fin fout ver ) $ filter ( not . isPrefixOf "." ) folders
