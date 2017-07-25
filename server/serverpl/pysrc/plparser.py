#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  plparser.py
#  
#  Copyright 2017 Dominique Revuz <dr@univ-mlv.fr>
#  

import os, re, hashlib
from pathlib import Path

from pl import ErrorPL, PlSyntaxError, PlMultilineError, InvalidExtensionError, dicfusion

import cd 

import subprocess

"""
 plparser.py 
  Le parsing des fichiers pl et pltp et autres types de fichiers doit être réalisé par du code de ce fichier.
  Le parsing ne fait que transformer le fichier en un dictionnaire python.
  actuellement le fichier fournis trois méthode diFromFile qui appel la fonction parsePlFile ou parsePltpFile, 
  si l'on cherche à a jouter une nouveau type c'est ici qu'il faut ajouter une fonction parseExtFile ou Ext est l'extension capitalisée du nouveau type.
  Par exemple parsePlwFile pour les fichiers PlWims
"""

def getRepoByName(name):
    """
    find the repo name in directory premierlangage/repo/
    >>> getRepoByName(None).endswith("/premierlangage/repo/plbank")
    True
    >>> getRepoByName("plbank").endswith("/premierlangage/repo/plbank")
    True
    """
    if name==None:
        name="plbank"
    with cd.cd(os.path.dirname(__file__)):
        prems = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],stdout=subprocess.PIPE).communicate()[0].rstrip().decode("utf-8")
    p = Path(prems+"/repo/"+name)
    if not p.exists():
        raise Exception(str(p)+" doesn't exist")
    return str(p)


def _openandsplit(filename):
    """
    FIXME is the file closed 
    """
    try:
        try:
            filename = str(filename)
        except:
            raise ErrorPL("Filename type is incorrect: "+ filename+"\n"+type(filename))
        with open(filename,"r") as f:
            return f.read().split("\n")
    except Exception as e:
        raise ErrorPL("Can't open file '"+ filename+"': "+str(e))



concept='^concept==(?P<value>.*)$'
concept_regex=re.compile(concept)
key='^(?P<key>\w+)\s*'
operator='(?P<op>=|==|=@)\s*'
value='(?P<value>[^=@#]*)'
commentANDend='($|(?P<comment>#.*)$)'
correct_line=re.compile(key+operator+value+commentANDend)#,re.DEBUG)
starmulti=re.compile("^(?P<name>\w*)\s*(?P<op>==).*$")#,re.DEBUG)
debug=False



def _addcomment(d,comment):
    if not 'comment' in d :
        d['comment']=''
    d['comment'] += comment+"\n"


def _parseOneLine(line, dic, n_line, repo):
    """
    Return a tuple of 3 value (start_multiline, key_multiline, warning_msg):
        - start_multiline: True if the line start with 'key==', False if not
        - key_multiline: Value of key if start_multiline is True, None if False
        - warning_msg: Message alerting if a key has been overwritten, None if not
    """
    warning_msg = None
    
    if not line:
        return False, None, None
    
    if line.startswith('#'): #If the line is a comment
        _addcomment(dic, line)
        return False, None, None
    
    concept_list = concept_regex.search(line)
    if concept_list: #If the line is a list of concept
        if 'concept' in dic:
            dic['concept'].append(concept_list.group('value'))
        else:
            dic['concept'] = concept_list.group('value')
    
    correct = correct_line.search(line)
    if not correct: #Different than 'key==' or 'key=value'
        raise PlSyntaxError(line, str(n_line))
        
    if correct.group('comment'): #If a comment is at the end of the line
        _addcomment(dic, line)
    
    if correct.group('op') == '==': #If start of a multiline
        if correct.group('key') in dic:
            warning_msg = "Key "+correct.group('key')+" overwritten: "+line+"<br>"
        return True, correct.group('key'), warning_msg
        
    if correct.group('op') == '=@': #If link to a file
        if correct.group('key') == 'files' or correct.group('key') == 'sandbox':
            if 'files' in dic:
                dic['files'].append(correct.group('value'))
            else:
                dic['files'] = list()
                dic['files'].append(correct.group('value'))
        else:
                filename = _makefileName(correct.group('value'), repo)
                with open(filename,'r') as f:
                    dic[correct.group('key')] = f.read() 
    elif correct.group('op') == '=': #If 'key=value' line
        if not correct.group('value'):
            raise PlSyntaxError(line, str(n_line), "Syntax error, key without value")
        if correct.group('key') in dic:
            warning_msg = "Key "+correct.group('key')+" overwritten: "+line+"<br>"
        dic[correct.group('key')] = correct.group('value')
    
    return False, None, warning_msg


def _parseOneFile(filename, repo, currentdict=dict()):
    """
    Parse the file indicated by filename, creating the corresponding dic
    """
    n_line = 0
    opened = 0
    warning=""
    multiline = False
    multivalue=None
    another_multiline = re.compile('\w+==$')
    for line in _openandsplit(filename):
        n_line += 1
        if multiline:
            if (another_multiline.match(line)):
                warning += "Warning (l."+str(n_line)+"): multiline value declared inside another (declared at l."+str(opened)+")."
            if line == "==" :
                if not multivalue:
                    raise PlMultilineError(multikey, str(opened), "Multiline value can't be null")
                currentdict[multikey]=multivalue
                multiline = False
                multikey = None
            else:
                multivalue += line + "\n"
        else:
            multiline, multikey, warning_msg = _parseOneLine(line, currentdict, n_line, repo)
            multivalue=""
            if warning_msg:
                warning += warning_msg+'\n'
            if multiline:
                opened = n_line
    
    if multiline:
        raise PlMultilineError(multikey, str(opened))
        
    return currentdict, warning


def _makefileName(filename,repo):
    try:
        if filename.startswith(getRepoByName(repo)):
            return filename
        return getRepoByName(repo) + "/" + filename
    except Exception as e:
        print("impossible de trouver le repo : " + str(e))


def parsePltpFile(filename,repo,dico=dict()):
    dico['rel_path']=filename
    filename=_makefileName(filename,repo)
    hasher = hashlib.sha1()
    hasher.update((filename+repo).encode('utf-8'))
    dico['sha1']=hasher.hexdigest()
    try:
        dico, warning = _parseOneFile(filename, repo, dico)
    except PlSyntaxError as e:
        return None, str(e)
    except PlMultilineError as e:
        return None, str(e)
    except Exception as e:
        return None, "Erreur d'ouverture du fichier "+filename+": "+str(e)+" : "+str(type(e))
        
    while "template" in dico or "extends" in dico :
        if "template" in dico :
            templatename = dico['template']
        elif "extends" in dico :
            templatename = dico['extends']
        if not templatename.endswith('.pltp') :
            templatename += '.pltp'
        del dico['template'] # on boucle sur les templates
        filename=_makefileName(templatename,repo)
        dico_template = _parseOneFile(filename, repo, dict())
        dico = dicfusion(dico_template, dico)
    
    if not "concept" in dico:
        return None, "No excercice found in the PLTP."
    dico['conceptl']= list()
    for plname in dico['concept'].split("\n"):
        if plname != "":
            name = plname.split(" ")[1] # @ 
            if  ':' in name:
                lrepo,name = name.split(":")
            else:
                lrepo = repo
            if not(os.path.isfile(getRepoByName(lrepo)+name)):
                return None, "Can't find file '"+name+"' in repo "+lrepo
            dico['conceptl'].append((name,lrepo))
    del dico['concept']
    return dico, warning


def parsePlFile(filename,repo,dico=dict()):
    dico['rel_path']=filename
    filename=_makefileName(filename,repo) 

    warning = ""
        
    try:
        dico, warning_msg = _parseOneFile(filename, repo, dico)
        if warning_msg:
            warning += warning_msg+'\n'
    except PlSyntaxError as e:
        return None, str(e)
    except PlMultilineError as e:
        return None, str(e)
    except IOError as e:
        return None, "Erreur lors de l'ouverture du fichier : "+str(e)
    except Exception as e:
        return None, "Erreur d'ouverture du fichier "+str(_makefileName(filename, repo))+" - "+str(type(e))+": "+str(e)
        
    while "template" in dico:
        if  ':' in dico['template']:
            templaterepo, templatename = dico['template'].split(":")
        else:
            templatename = dico['template']
            templaterepo = repo
        if not templatename.endswith('.pl') :
            templatename += '.pl'
        del dico['template']
        filename=_makefileName(templatename,templaterepo)
        try:
            try:
                dico_template, warning_msg = _parseOneFile(filename, templaterepo, dict())
                if warning_msg:
                    warning += warning_msg+'\n'
            except PlSyntaxError as e:
                return None, str(e)
            except PlMultilineError as e:
                return None, str(e)
            except Exception as e:
                return None, "Erreur d'ouverture du fichier "+str(filename)+": "+str(e)
            if warning_msg:
                warning += warning_msg+'\n'
        except Exception as e:
            return None, str(e)
        dico = dicfusion(dico_template, dico)
    else :
        templaterepo = repo
    if 'files' in dico:
        dico["basefiles"]={}
        l = dico['files']
        del dico['files']
        n = 0
        for x in l:
            filexname=_makefileName(x,templaterepo)
            name = os.path.basename(x)
            if name in dico:
                return None, 'Key "'+name+'" is already defined in the PL'
            try:
                with Path(filexname).open() as f:
                    dico["basefiles"][name]=f.read()
            except Exception as e:
                return None, "Can't open the file: "+str(x)+": "+str(e)
            n+=1
    return dico, warning


def parsePlsFile(filename, repo, dic=dict()):
    dic['rel_path'] = filename
    filename = _makefileName(filename,repo)
    
    warning = ""
    
    try:
        dic, warning_msg = _parseOneFile(filename, repo, dic)
        if warning_msg:
            warning += warning_msg+'\n'
    except PlSyntaxError as e:
        return None, str(e)
    except PlMultilineError as e:
        return None, str(e)
    except IOError as e:
        return None, "Erreur lors de l'ouverture du fichier: "+str(e)
    except Exception as e:
        return None, "Erreur lors de la lecture du fichier "+str(e)+": "+str(filename)
    
    while "template" in dic:
        if  ':' in dic['template']:
            templaterepo, templatename = dic['template'].split(":")
        else:
            templatename = dic['template']
            templaterepo = repo
        if not templatename.endswith('.pls') :
            templatename += ends
        del dic['template']
        filename=_makefileName(templatename,templaterepo)
        try:
            try:
                dico_template, warning_msg = _parseOneFile(filename, templaterepo, dict())
                if warning_msg:
                    warning += warning_msg+'\n'
            except PlSyntaxError as e:
                return None, str(e)
            except PlMultilineError as e:
                return None, str(e)
            except Exception as e:
                return None, "Erreur d'ouverture du fichier "+str(filename)+": "+str(e)
            if warning_msg:
                warning += warning_msg+'\n'
        except Exception as e:
            return None, str(e)
        dico = dicfusion(dico_template, dico)
    
    return dic, warning

#def _repoexist(repo):
    #if type(repo)==str:
        #repo = Path(repo).name
        #p=Path(DIRREPO)
        #for x in p.iterdir():
            #if repo == x.name:
                #return x
        #raise Exception("Repo",repo,"Doesn't Exist")
    #elif type(repo)==Repository:
        #if not Path(repo.path).is_dir():
            #raise Exception("Repo",repo,"Doesn't Exist")
        #else:
            #return Path(repo.path)
    



def dicFromFile(filename, repo):
    """
    >>> len(dicFromFile("python/0PLG/TPE/error.pl","plbank"))
    13
    """
    if type(repo) != str :
        reponame = repo.name
    else:
        reponame = repo
    if filename.endswith(".pl"):
        return parsePlFile(filename, reponame, dict())
    if filename.endswith(".pltp"):
        return parsePltpFile(filename, reponame, dict())
    if filename.endswith(".pls"):
        return parsePlsFile(filename, reponame, dict())
    raise InvalidExtensionError(filename)
        

if __name__ == "__main__":

    import doctest
    doctest.testmod()

