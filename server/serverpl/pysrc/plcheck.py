import subprocess
import sys
import pathlib
import os
import getopt
from newcheck import checkplfile, checkpltpfile

#DIRREPO=BASE_DIR + "../../repo"

debug=True
verbose=False


defaultsandbox="http://pl-sandbox-test.u-pem.fr/?action=execute"
localsandbox="http://127.0.0.1:8000/sandbox/?action=execute"

commandline=False

def main(repo_dir,exopath,sandboxurl=localsandbox):
    pe = pathlib.Path(exopath)
    filename = str(pe.resolve())
    if verbose :
        pass
    if filename.endswith(".pl"):
        if ":" in pl:
            return checkplfile(filename, s.split(":")[0], sandboxurl=sandboxurl)
        else:
            return checkplfile(filename, 'plbank', sandboxurl=sandboxurl)
    elif filename.endswith(".pltp"):
        return checkpltpfile(filename,repo_dir,sandboxurl=sandboxurl)


#def checkpltpfile(pltp, sandboxurl=defaultsandbox):
	#print("Test de "+DIRREPO+'/'+pltp.repository.name+pltp.rel_path+"\nsur : "+sandboxurl)
	#tp = pltp.pl.all()
	#ok=True
	#for pl in tp:
		#print("checking pl file :", DIRREPO+'/'+pltp.repository.name +plfilename)
		#ok=ok and checkplfile(pl, sandboxurl=sandboxurl)
		#if not ok:
			#raise Exception( "Un exercice pose problème pltp non validé")
	#return ok
	##pe = pathlib.Path(exopath)
	##s = str(pe.resolve())
	##if verbose:
		##print("Test de "+s+"\nsur : "+sandboxurl)
	##q=question.Question(s[len(str(repo_dir)):],root=repo_dir)
	##dico = q.dico
	##for key in ["introduction","concept","name"]:
		##if not key in dico:
			##raise question.ErrorPL("PLTP sans balise "+key)
	##if verbose: print(dico['concept'])

	#### FIX ME tester si les fichier sont connus de git et a jour


#def checkplfile(filename,repo,sandboxurl="http://pl-sandbox-test.u-pem.fr/?action=execute",studentfile="print(3000)"):

	#q = dicFromFile(filename,repo)

	
	#if verbose : print("Question chargée") 
	#if "testcode" in q.dico:
		#studentfile=q.dico["testcode"]
	#elif "soluce" in q.dico :
		#studentfile=q.dico["soluce"]
	#s = SandboxSession(pl,q,sandboxurl,studentfile)# question,url,studentfile
	#print(s.answer)
	#result = json.loads(s.answer)
	#if result["platform_error"] != []:
		#print("Erreur de platforme ")
		#print(result["platform_error"])
		#return False

	#if verbose: print("La correction pour "+studentfile+" est "+result["grade"]['feedback'])
	#with open("/tmp/result.html","w")as rf:
		#print(result["grade"]['feedback'],file=rf)
	#print("le feedback est dans file:///tmp/result.html ")
	#print("Saving tags")
	#for key in q.dico.keys():
		#print(key)
	#tagl=q.dico["tag"].split("|")
	#for tag in tagl:
		#plcreatetag(tag,description="Initialisation par plcheck\n Dominique Revuz\n")
	#print("Tags saved")
	#return True

def getrepodir():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
    stdout=subprocess.PIPE).communicate()[0].rstrip().decode("utf-8")

def docommit(name):
    print(name.split("/")[-1]+" is valid, commiting...")
    subprocess.run(['git', 'commit','-m','plcheck commit '+name, name])
    # FIXME quentin ajouter le nom dans le message


if __name__ == '__main__':
    repo_dir = getrepodir()
    
    if repo_dir == "" :
        sys.exit(-1)

    if debug :
        print("Traitement du repo"+repo_dir)

    sandboxarg = localsandbox
    
    try :
        opts, args = getopt.getopt(sys.argv, "vs:")
    except getopt.GetoptError as goe:
        print(goe)
        #usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == "-v":
            verbose = True
        if opt == "-s":
            sandboxarg = arg
            
    for pl in sys.argv[1:]:
        try:
            ok, num = main(repo_dir,pl,sandboxurl=sandboxarg) #  tout les test en local and sandbox
            if ok:
                docommit(pl)
            else :
                print(num)
        except Exception as e:
            print("Problem avec ",pl)
            raise e

    sys.exit(0)
