import os
import sys
import json
sys.path.append(os.path.dirname(__file__)+"/..")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serverpl.settings")



from pleditor import check_dic_pl,  get_zip_value
from plparser import dicFromFile
from plrequest import SandboxCheck , PlMissingSoluceError
sys.path.append(os.path.dirname(__file__)+"/../")
from playexo.pythonbuildertest import PythonBuilderTest

import html

debug=True


def evaluate(dic, answer):
    try:
        exec(dic['evaluator'], globals())
        state, feedback = evaluator(answer, self.dic)
        if (not isinstance(state, bool)) or (not isinstance(feedback, str)):
            return True, ("/!\ ATTENTION: La fonction d'évaluation de cet exercice est incorrecte, merci de prévenir votre professeur:\n"
                          "Function evaluator() should return a tuple (bool, str).")
        return state, feedback
    except Exception as e:
        er=html.escape(str(type(e))+":\n"+str(e))
        return True, ("/!\ ATTENTION: La fonction d'évaluation de cet exercice est incorrecte, merci de prévenir votre professeur:\nError - "+er)
    



#filename = chemin depuis le repertoire (par exemple depuis plbank)
def checkplfile(filename, repo, sandboxurl="http://pl-sandbox-test.u-pem.fr/?action=execute"):
    """
    checkplfile : verifie le bon fonctionnement d'un exercice 
    
    1) charger avec plparser l'exercice et verifier la bonne syntaxe 
    si on echoue ici on retourne false,1

    2) verifier le "type" de l'exo si toute les balises nécessaires à l'exo sont présentes 
    si on echoue ici on retourne false2
    2.5) builder l'exercice (FIXME timeout)
    si echoue false,3
    3) si l'exo utilise la sandbox on test avec "print(3000)" comme studentcode 
    la réponse de la sandbox doit être plateforme==[] et sucess=false
    4) si l'exo utilise la sandbox on test avec soluce ou testcode comme studentcode 
    la réponse de la sandbox doit être plateforme==[] et sucess=True
    Dans les cas 4 et 5 si plateforme != [] 
    false,4
    
    si tout est ok retourne True,None
    """
    q,warning = dicFromFile(filename,repo)
    print(warning)
    
    if not q :
        return False, 1
    
    state, warning_msg = check_dic_pl(q)
    if not state:
        print(filename+" - "+warning_msg)
        return False, 2
    if warning_msg:
            warning += warning_msg+'\n'
    try:        
        q = PythonBuilderTest(q).get_dico()
    except Exception as e:
        print(str(type(e)) + str(e))
        return False, 3
        
    q['zipvalue'] = get_zip_value(q)
    if not q['zipvalue']:
        #Ceci devrait fonctionner pour tous les gifts si on ne duplique plus les réponses 
        list_rep = [q[x] for x in q.keys() if 'answer' in x]
        v,f = evaluate(q,list_rep)
        if not v:
            return False, 4
    #If dictionnary contains a zipvalue key, we have to use the sandbox
    else:
        s = SandboxCheck(q, url = sandboxurl)
        try:
            answer = s.call()
        except PlMissingSoluceError as e:
            print(e)
            return False, 2
        except Exception as e:
            print("Impossible de joindre la sandbox : " + sandboxurl + " - " + "exception is : " + str(type(e)) + " : "+ str(e))
            return False, 5
        result = json.loads(answer)
        if result["platform_error"] != []:
            print("Erreur de plateforme : " + str(result["platform_error"]))
            print("Vérifiez les fichiers produits par la Sandbox "+str(sandboxurl) +'\n')
            if  "127.0.0.1" in sandboxurl :
                os.chdir(s.createlocaldir())
            else:
                os.chdir(result['path_files'])
            os.environ['PS1']="Testez votre grader> "
            os.execl("/bin/bash",'bash','-norc')
            #return is not necessary 

        '''with open("/tmp/sandbox/result.html","w")as rf:
            feedback = result['grade']
            print(feedback,file=rf)'''

        if not result['grade']["success"]:
            print("\n[Invalid PL] : Bad soluce or testcode\n")
            return False, 4
        else :
            try:
                s.dic['zipvalue'] = s.zipvalue
                answer = s.call('print(3000)')
            except Exception as e:
                print("Impossible de re-joindre la sandbox : " + sandboxurl + " - " + "exception is : " + str(type(e)) + " : "+ str(e))
                return False, 5
            result = json.loads(answer)
            if result['grade']['success']:
                print("[Invalid Pl] :  mauvais code donne True")
                return False, 4
                
    return True, None
    '''if verbose: print("La correction pour "+studentfile+" est "+result["grade"]['feedback'])
    print("Saving tags")
    for key in q.dico.keys():
        print(key)
    tagl=q.dico["tag"].split("|")
    for tag in tagl:
        plcreatetag(tag,description="Initialisation par plcheck\n Dominique Revuz\n")
    print("Tags saved")'''

def checkpltpfile(filename, repo, sandboxurl="http://pl-sandbox-test.u-pem.fr/?action=execute") :
    q,warning = dicFromFile(filename,repo)
    print(warning)
    if not q :
        return False
    for pl in q['conceptl']:
        if not checkplfile(pl[0], pl[1], sandboxurl):
            print(pl[0])
            return False

    return True


''' ajouter des options pour préciser une url pour la sandbox si nécessaire
    tester si ca ping etc
'''




