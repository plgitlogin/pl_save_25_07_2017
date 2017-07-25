import json
import sys
import io
import contextlib
import shlex

# Replacing standard outputs and error with stringsIO
# So we can retrieve the output of the execution
# We also need to replace the standard input by the input file if needed 


# STDOUT
@contextlib.contextmanager
def stdoutIO(stdout = None):
	old = sys.stdout
	if stdout is None:
		stdout = io.StringIO()
	sys.stdout = stdout
	yield stdout 
	sys.stdout = old 


# STDERR
@contextlib.contextmanager
def stderrIO(stderr = None):
	old = sys.stderr
	if stderr is None:
		stderr = io.StringIO()
	sys.stderr = stderr
	yield stderr
	sys.stderr = old


# STDIN
@contextlib.contextmanager
def stdinFile(input = None):
	old = sys.stdin

	if len(sys.argv) == 3 :
		stdin = open(sys.argv[2])
	else :
		stdin = StringIO()

	sys.stdin = stdin
	yield 
	sys.stdin = old
	stdin.close()


with open(sys.argv[1]) as f:
	try:
		code = compile(f.read(), sys.argv[1], 'exec')
		
		print('Code compilation complete')

		#loading input if any
		input = [sys.argv[1]]

		with stdoutIO() as out, stderrIO() as err :
			old = sys.stdin
			if len(sys.argv) == 3:
				sys.stdin = open(sys.argv[2])
			sys.argv = input
			exec(code, globals(), locals())
			sys.stdin = old
		
		print(json.dumps( { "stdout" : out.getvalue() , "stderr" : err.getvalue() } ))

		out.close()
		err.close()
	except SyntaxError as err :
		error_class = err.__class__.__name__
		details = err.args[0]
		line_number = err.lineno
		print(json.dumps( { "stdout" : "", "stderr" : "%s at line %d of your code : %s" % (error_class, line_number, details) } ))
		sys.exit(0)