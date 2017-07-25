#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  loader2.py
#  
#  Copyright 2017 Dominique Revuz <dr@univ-mlv.fr>
#  

from pleditor import check_dic_pl, check_dic_pltp, get_zip_value
from gitload.models import Repository, PL, PLTP, Strategy

from plparser import dicFromFile

from os.path import splitext,basename
import hashlib



def loadPLTP(rel_path, repo, force=False):
    """ Load the PLTP by checking its integrity and adding it and every self.pl to the database.
        Return:
            - (PLTP, None) if the PLTP was loaded successfully
            - (PLTP, warning_msg) if the PLTP was loading with warnings
            - (None, error_msg) if PLTP couldn't be loaded
            - (None, None) if PLTP is already loaded
    """
    warning = ""
    if not type(repo)==Repository:
        raise Exception(" repo is not a repository")
    name = splitext(basename(rel_path))[0]
    hasher = hashlib.sha1()
    hasher.update((rel_path+repo.name).encode('utf-8'))
    sha1 = hasher.hexdigest()
    
    try:
        existing= PLTP.objects.get(sha1=sha1)
        if not force:
            return None, None
        existing.delete()
    except: # If the PLTP does not exist, pass
        pass
    
    rootdir=repo.getRootDir()
    dic, warning_msg = dicFromFile(rel_path,repo.name)
    if warning_msg:
        warning += rel_path+": "+warning_msg+'\n'
    if not dic:
        return None, rel_path+" - "+warning_msg
    
    state, warning_msg = check_dic_pltp(dic)
    if warning_msg:
            warning += rel_path+": "+warning_msg+'\n'
    if not state:
        return None, rel_path+" - "+warning_msg
            
    pl_list=list()
    
    for lname,reponame in dic['conceptl']:
        repo2 = Repository.getRepoByName(reponame)
        pl, warning_msg = loadPL(lname, repo2)
        if warning_msg:
            warning += lname+": "+warning_msg+'\n'
        if not pl:
            return None, warning_msg #Returning only the error of the current PL if the loading failed
        pl_list.append(pl)
    del dic['conceptl']
    
    for pl in pl_list:
        pl.save()

    
    pltp = PLTP(name=name, sha1= sha1, json= dic, repository= repo, rel_path=rel_path)
    pltp.save()
    for pl in pl_list:
        pltp.pl.add(pl)
    
    return pltp, warning
    

def loadPL(rel_path, repo):
    warning = ""
    
    dic, warning_msg = dicFromFile(rel_path,repo)
    if (not dic):
        return None, rel_path+" - "+warning_msg
    if warning_msg:
            warning += warning_msg+'\n'
    
    state, warning_msg = check_dic_pl(dic)
    if (not state):
        return None, rel_path+" - "+warning_msg
    if warning_msg:
            warning += warning_msg+'\n'
    
    zipvalue = None
    if dic['type'] == 'sandbox':
        zipvalue = get_zip_value(dic)


    
    name = splitext(basename(rel_path))[0]
    hasher = hashlib.sha1()
    hasher.update((rel_path+repo.name).encode('utf-8'))
    sha1 = hasher.hexdigest()
    pl = PL(name= name, sha1=sha1, json=dic , zipvalue=zipvalue, repository=repo, rel_path=rel_path)
    return pl, warning



def loadPLS(rel_path, repo, force=False):
    name = splitext(basename(rel_path))[0]
    try:
        existing= Strategy.objects.get(name=name)
        if not force:
            return None, None
        existing.delete()
    except: # If the PLS does not exist, create it
        pass
    
    dic, warning = dicFromFile(rel_path, repo)
    if (not dic):
        return None, rel_path+" - "+warning_msg

    pls = Strategy(name=name, json=dic, rel_path=rel_path, repository=repo)
    pls.save()
    return pls, warning
