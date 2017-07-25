#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

import os, shutil, git, subprocess, logging, re

from serverpl.settings import DIRREPO

from os.path import basename, isfile, isdir, splitext, dirname, realpath

from gitload.loader import loadPLTP, loadPLS, loadPL
from gitload.models import Repository

logger = logging.getLogger(__name__)


class Browser():
    
    def __init__(self, repository, dic = None):
        """ Members will be initialized with a dictionnary if provided """
        
        if (not dic):
            self.name = repository.name             #Name of the repository
            self.url = repository.url               #URL of the repository
            self.root = DIRREPO + '/' + self.name   #Absolute path to the local copy of the repository
            self.current_path = self.root           #Absolute path to the actual directory of the repository in the browser
            self.pltp_list = list()                 #List of every pltp in self.current_path
            self.pl_list = list()                   #List of every pl in self.current_path
            self.dir_list = list()                  #List of every directory in self.current_path
            self.other_list = list()                #List of every other files in self.current_path
            self.version = "Inconnue: Merci d'actualiser le dépot"

            try:
                if (self.name != "plbank"):
                    repo = git.Repo(self.root)
                    self.version = repo.heads.master.commit.name_rev[:40]
            except:
                if (self.name != "plbank"):
                    self.get_repo()
            
        else:
            for k, v in dic.items():
                setattr(self, k, v)
    
    def get_repo(self):
        """ Create or replace self.path with a new clone of self.url
            Update self.version """
        if self.name == 'plbank':
            return True
            
        if not os.path.isdir(self.root):
            repo = git.Repo.clone_from(self.url, self.root)
        else:
            repo = git.Repo.init(self.root)
        try:
            repo.git.pull(self.url)
        except:
            logger.info("Couldn't join "+self.url)
            return False

        self.version = repo.heads.master.commit.name_rev[:40]
        repo_object = Repository.objects.get(name=self.name)
        repo_object.version = self.version
        repo_object.save()
        return True

    def parse_content(self):
        """ Fill 'pltp', 'dir' and 'other' lists with the corresponding file. """
        self.pltp_list = list()
        self.dir_list = list()
        self.other_list = list()
        self.pl_list = list()
        
        pattern = re.compile("(.)+\.(pl(\w)+)$")
        
        for (path, subdirs, files) in os.walk(self.current_path):
            for filename in files:
                if (pattern.match(filename)):
                    self.pltp_list.append(filename)
                elif filename.endswith('.pl'):
                    self.pl_list.append(filename)
                else:
                    self.other_list.append(filename)
                    
            for filename in subdirs:
                if (filename[0] != '.'):
                    self.dir_list.append(filename)
            break;
        
        self.pl_list.sort()
        self.pltp_list.sort()
        self.other_list.sort()
        self.dir_list.sort()
    
    def load_pl(self, rel_path, repository):
        return loadPL(rel_path, repository)
        
    def load_pls(self, rel_path, repository, force=False):
        return loadPLS(rel_path, repository, force=force)
    
    def load_pltp(self, rel_path, repository, force=False):
        """ Create a PLTP_Loader with the rel_path to the local repo of a pltp """
        return loadPLTP(rel_path, repository, force=force)
        
    def cd(self, rel_path = "/"):
        """ Change self.current_path, rel_path is relative to self.root """
        if (rel_path == "/" or rel_path == "~"):
            self.current_path = self.root
            
        elif (isdir(self.root + "/" + rel_path)):
            self.current_path = self.root + "/" + rel_path
            if (self.current_path[-1] != "/"):
                self.current_path += "/"
