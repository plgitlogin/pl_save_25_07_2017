#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python [Version]
#
#  Author: Coumes Quentin     Mail: qcoumes@etud.u-pem.fr
#  Created: 2017-07-03
#  Last Modified: 2017-07-03

from sympy import latex

from django.template import Template, Context, RequestContext
from gitload.models import PLTP, PL
from playexo.models import Answer

default_load = '{% load bootstrap3 %}{% load static %}{% load markdown_deux_tags %}{% load input_fields_ajax %}{% load json_filter %}'
pls_known = [
    ('form', 'form'), ('css', 'css'), ('pl', 'exo'),
    ('pltp', 'exo'), ('navigation', 'navigation'),
    ('load', 'load'), ('state', 'state'), ('end_script', 'end_script'),
    ('header_script', 'header_script')
]

def for_template(arg):
# renvoie arg dans un bon format pour l'affichage dans un template html avec mathjax. Si arg est une liste, s'applique récursivement aux éléments de arg.
    if ('sympy' in str(type(type(arg)))) or  ('sympy' in str(type(arg))): # selon les cas 'sympy' n'est pas dans type(arg), mais dans type(type(arg)). C'est de la cuisine.
        return  r'\displaystyle '+latex(arg, mat_delim="(")        # par défaut l'output latex n'a pas les $, mais est en 'displaystyle'.
    elif type(arg) in [int, float, str] :
        return arg
    elif isinstance(arg, dict):
        return {k: for_template(arg[k]) for k in arg}
    elif isinstance(arg, list):
        return list(map(for_template,arg))
    elif isinstance(arg, tuple):
        return tuple(map(for_template,arg))
    else : return arg

class Exercise:
    def __init__(self, pl_dic):
        self.dic = pl_dic
    
    def evaluate(self, answer):
        try:
            exec(self.dic['evaluator'], globals())
            dic = self.__build()
            state, feedback = evaluator(answer, dic)
            if (not isinstance(state, bool)) or (not isinstance(feedback, str)):
                return True, ("/!\ ATTENTION: La fonction d'évaluation de cet exercice est incorrecte, merci de prévenir votre professeur:\n"
                              "Function evaluator() should return a tuple (bool, str).")
            return state, feedback
        except Exception as e:
            import html
            er=html.escape(str(type(e))+":\n"+str(e))
            return True, ("/!\ ATTENTION: La fonction d'évaluation de cet exercice est incorrecte, merci de prévenir votre professeur:\nError - "+str(e))
    
    def __build(self):
        if 'build' in self.dic:
            exec(self.dic['build'], globals())
            return build(self.dic)
        return self.dic
            
    def __get_context(self, request, feedback=None, success=None):
        pl_list = list()
        color= {
            'ST': 'warning',
            'FA': 'danger',
            'SU': 'success',
            'NA': 'info',
        }
        pltp = PLTP.objects.get(sha1=self.dic['pltp_sha1'])
        for item in pltp.pl.all():
            answer = Answer.objects.filter(user=request.user, pl=item).order_by('-date')
            if answer:
                state = answer[0].state
            else:
                state = 'NA'
            if 'pl_sha1' in self.dic and item.sha1 == self.dic['pl_sha1']:
                self.dic['student_answer'] = answer[0].value
            pl_list.append((item, color[state]))
                
        context = RequestContext(request)
        dic = self.__build()
        context.update(dic)
        context['pl_list'] = pl_list
        
        
        if success:
            context['success'] = success
        if feedback:
            context['feedback']= feedback
        
        return context
    
    def __get_template(self):
        if 'pl_sha1' in self.dic:
            raw = '{% extends "playexo/default_pl_exo.html" %}'+default_load
            for key, block_name in pls_known:
                if key in self.dic:
                    raw += "{% block "+block_name+" %}"+self.dic[key]+"{% endblock %}"
        else:
            raw = '{% extends "playexo/default_pltp_exo.html" %}'+default_load
        return raw
        
    def render(self, request, feedback=None, success=None):  
        """ Return the rendered template for this PL """
        context = self.__get_context(request, feedback, success)
        template = self.__get_template()
        return Template(template).render(context)
    
    
    
class ExerciseTest(Exercise):
    def __init__(self, pl_dic):
        super().__init__(pl_dic)
    
    def __build(self):
        if 'build' in self.dic:
            exec(self.dic['build'], globals())
            return build(self.dic)
        return self.dic
    
    def __get_template(self): 
        raw = '{% extends "playexo/default_pl_test.html" %}'+default_load
        for key, block_name in pls_known:
            if key in self.dic:
                raw += "{% block "+block_name+" %}"+self.dic[key]+"{% endblock %}"
        return raw
    
    def __get_context(self, request, feedback=None, success=None):
        context = RequestContext(request)
        dic = self.__build()
        dic = for_template(dic)
        context.update(dic)
        if success:
            context['success'] = success
        if feedback:
            context['feedback']= feedback
        return context
        
    def render(self, request, feedback=None, success=None):  
        """ Return the rendered template for this PL """
        context = self.__get_context(request, feedback, success)
        template = self.__get_template()
        return Template(template).render(context)
