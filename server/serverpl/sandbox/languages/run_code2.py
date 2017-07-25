import sys
import subprocess
import io
import json

proc = subprocess.Popen(["python3", sys.argv[1]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

inputData = None 

if len(sys.argv) == 3:
	with open(sys.argv[2], "r") as f :
		inputData = f.read()

out, err = proc.communicate(input=inputData)

print(json.dumps( { "stdout" : out , "stderr" : err } ))