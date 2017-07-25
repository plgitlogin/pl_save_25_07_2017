#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  request.py
#  
#  Copyright 2017 Dominique Revuz <dr@univ-mlv.fr>
#  

__doc__ = """

    Ce fichier a pour objectif de gérer les communications
    avec la sandbox.
    """


import requests
import question
import zipfile
import pathlib
import pleditor
import cd
import subprocess
import hashlib
import json
import shutil
import os


class PlMissingSoluceError(Exception):
    """ Raised if an error occured during parsing a PL """

    def __init__(self, message="Missing Soluce"):
        self.message = message
        
    def __str__(self):
        return self.message

defaultpldataurl="http://127.0.0.1:9090"

def pllogdata(user,zipsha1,pljsonsha1,studentfile=None,mode="try",url = defaultpldataurl):
    if studentfile == None:
        mode= "start"
    geturl=url+"/add/tt"
    posturl=url+"/add/xx"
    try:
        csrftoken = requests.get(geturl).cookies['csrftoken']
        header = {'X-CSRFToken': csrftoken}
        cookies = {'csrftoken': csrftoken}
        r=requests.post(posturl,headers=header, cookies=cookies,data={"user":user,"code":studentfile,"mode":mode,"zipsha1":zipsha1,"pljsonsha1":pljsonsha1})
    except Exception as e:
        print(" Berk can't access pldata",e) # don't dye for this
        r=None
    return r

def plcreatetag(tag,description="construit automatiquement"):
    if studentfile == None:
        mode= "start"
    createurl="http://pl.univ-mlv.fr/concept/create/"
    existurl="http://pl.univ-mlv.fr/concept/exist/"+tag+"/"
    try:
        r=requests.get(existurl)
        if r.ok : # le tag exist sortie 
            return
        csrftoken = requests.get(createurl).cookies['csrftoken']
        header = {'X-CSRFToken': csrftoken}
        cookies = {'csrftoken': csrftoken}
        r=requests.post(createurl,headers=header, cookies=cookies,data={"name":tag,"lname":tag,"description":description})
    except Exception as e:
        print(" Berk can't access pl.univ-mlv.fr",e) # don't dye for this
        r=None
    return r


class SandboxCheck:
    def __init__(self, pldic, url = "/sandbox/pl"):
        self.url = url
        self.dic = pldic
    
    def call(self, studentcode=None):
        if studentcode:
            studentfile=studentcode
            if "testcode" in self.dic:
                self.dic["testcode"]=studentfile
            else:
                self.dic['basefiles']["soluce.py"]=studentfile
        else:    
            if "testcode" in self.dic:
                studentfile=self.dic["testcode"]
            elif "soluce.py" in self.dic['basefiles']:
                studentfile=self.dic['basefiles']["soluce.py"]
        mn = hashlib.sha1()
        self.zipvalue = self.dic['zipvalue']
        del self.dic["zipvalue"]
        mn.update(self.zipvalue[:])
        self.ziphashvalue = mn.hexdigest()
        files = {
            'environment.zip': self.zipvalue,
            'student.py': studentfile,
            "grader.py": self.dic['basefiles']['grader.py'],
            'hashvalue': self.ziphashvalue,
            'pl.json': json.dumps(self.dic),
        }
        x = requests.post(self.url, data=self.dic, files=files, timeout=1)
        return x.text

    def createlocaldir(self,dirname="/tmp/sandbox/"):
        # (re-)create directory 
        shutil.rmtree(dirname, ignore_errors=True)
        os.mkdir(dirname)
        with open("/tmp/sandbox/student.py", 'w') as student:
            print(self.dic['testcode'], file=student)
        with open("/tmp/sandbox/grader.py", 'w') as grader:
            print(self.dic['basefiles']['grader.py'], file=grader)
        with open("/tmp/sandbox/pl.json", 'w') as js:
            print(json.dumps(self.dic), file=js)
        with open("/tmp/sandbox/environment.zip", 'w') as env:
            print(self.zipvalue, file=env)
        with open("/tmp/sandbox/hashvalue", 'w') as hsh:
            print(self.ziphashvalue, file=hsh)

        return dirname


class SandboxSession:
    def __init__(self, dic, studentfile, url = "/sandbox/pl"):
        """
        avec un pl on appel :
        SandboxSession(pl
        """
        self.url = url
        print(dic['basefiles'])
        self.zipvalue = pleditor.createzipfile(dic['basefiles'])
        self.dic = dic
        self.studentfile = studentfile
    
    def call(self):        
        mn = hashlib.sha1()
        mn.update(self.zipvalue[:])
        ziphashvalue = mn.hexdigest()
        
        files = {
            'environment.zip': self.zipvalue,
            'student.py': self.studentfile,
            "grader.py": self.dic['basefiles']['grader.py'],
            'hashvalue': ziphashvalue,
            'pl.json': json.dumps(self.dic),
        }
        
        x = requests.post(self.url, data=self.dic, files=files, timeout=1)
            
        return x.text
