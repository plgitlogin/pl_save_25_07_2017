#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python [3.6]
#
#  Author: Coumes Quentin     Mail: qcoumes@etud.u-pem.fr
#  Created: 2017-06-21
#  Last Modified: 2017-06-21

import json, random, time

from gitload.models import PL
from playexo.models import Activity
from playexo.exercise import Exercise, ExerciseTest




class Builder():
    """ Parent class for every builder. methods '__create_template()' and '__create_context()' should be implemented in every child class. """
    def __init__(self, request, activity, pl=None, seed=None):
        if type(activity) != Activity:
            raise TypeError("Variable 'activity' should be of type '"+type(Activity)+"', not '"+type(activity)+"...")
        if pl and type(pl) != PL:
            raise TypeError("Variable 'pl' should be of type '"+type(PL)+"', not '"+type(pl)+"...")
        self.request = request
        self.activity_id = activity.id
        self.activity_name = activity.name
        self.pltp = activity.pltp
        self.strategy = activity.strategy
        self.pl = pl
        self.pl_dic = None
        self.context = None
        self.template = None
        self.seed = seed
    
    def get_exercise(self):
        """ Create and return the context of the activity. """
        raise NotImplementedError("Method 'get_exercise' not implemented")



class PythonBuilder(Builder):
    """ Parent class for every builder for Python language. """
    def __init__(self, request, activity, pl=None, seed=None):
        super().__init__(request, activity, pl)
        self.pl_dic = dict()
        self.pl_dic['activity_name'] = self.activity_name
        self.pl_dic['activity_id'] = self.activity_id
        self.pl_dic['strategy_name'] = self.strategy.name
        self.pl_dic['pltp_name'] = self.pltp.name
        self.pl_dic['pltp_sha1'] = self.pltp.sha1
        if pl:
            self.pl_dic['pl_sha1'] = self.pl.sha1
            self.pl_dic['pl_name'] = self.pl.name
            self.pl_dic.update(json.loads(self.pl.json))
            if self.seed:
                self.pl_dic['seed'] = seed
            else:
                random.random()
                self.pl_dic['seed'] = time.time()
            
        else:
            self.pl_dic.update(json.loads(self.pltp.json))
        
    def get_exercise(self):
        return Exercise(self.pl_dic)


class PythonBuilderTest(PythonBuilder):
    """ Used to test directly a PL """
    def __init__(self, pl_dic):
        self.pl_dic = pl_dic
        self.pl_dic['seed'] = time.time()
    
    def get_exercise(self):
        return ExerciseTest(self.pl_dic)

