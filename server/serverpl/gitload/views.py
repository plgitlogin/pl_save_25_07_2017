#!/usr/bin/env python3
# coding: utf-8

import os, re, shutil, git
from os.path import basename, isdir, splitext

from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from gitload.browser import Browser
from gitload.models import PLTP, Repository, PL, Strategy
from gitload.utils import create_breadcrumb

from playexo.models import Activity
from playexo.views import try_pl

from serverpl.settings import DIRREPO


@login_required
def home(request):
    return render(request, 'gitload/home.html', {
    })

@login_required
def index(request):
    """ View for /gitload/ -- template: index.html """
    Repository.add_missing_repository_in_bd()
    error_url = False
    error_name = False
    
    if (request.method == 'POST'):
        repo_url = request.POST.get('repo_url', "")
        repo_name = request.POST.get('repo_name', "")
        repo_delete = request.POST.get('repo_delete', "")
        
        if (repo_delete != ""):
            try:
                Repository.objects.get(name=repo_delete).delete()
                messages.warning(request, "Le dépot <b>"+repo_delete+"</b> a bien été supprimé !")
            except:
                messages.error(request, "Erreur lors de la suppression du dépot <b>"+repo_delete+"</b>...")
            
        elif (repo_url != ""): #If new repository
            try:
                repo, created = Repository.objects.get_or_create(name=repo_name, url=repo_url)
                browser = Browser(repo)
                if (not browser.get_repo()):
                    shutil.rmtree(browser.root)
                    error_url = True
                    messages.error(request, "Dépot <b>" + browser.url + "</b> introuvable. Merci de vérifier l'adresse ou votre connexion internet.")
                    repo.delete()
                else:
                    messages.success(request, "Dépot <b>"+repo_name+"</b> ajouté avec succès !")
            except IntegrityError as e:
                error_name = True
                messages.error(request, "Le nom <b>"+repo_name+"</b> est déjà utilisé, merci d'en choisir un autre.")
                
        elif (repo_name != ""): #If default
            repo = Repository.objects.get(name=repo_name)
            browser = Browser(repo)
        
        if (repo_name != "" and repo_url == "" and repo_delete == ""):
            request.session["browser"] = browser.__dict__
            return redirect(browse)
    
    repo_list = Repository.objects.all()
    return render(request, "gitload/index.html", {
        "default": repo_list,
        "error_name": error_name,
        "error_url": error_url,
    })

@login_required
def browse(request):
    """ View for [...]/gitload/browse -- template: browse.html """
    if (not "browser" in request.session):
        return redirect(index)
    
    browser = Browser(None, dic=request.session["browser"])
    ask_force = False
    force = False
    plx_path = ""
    
    if (request.method == 'POST'):
        git_path = request.POST.get('git_path', "")
        plx_path = request.POST.get('exported', "")
        if git_path:
            browser.cd(git_path)
        
        if plx_path: #Loading a PLTP
            repo_object = Repository.objects.get(name=browser.name)
            if (request.POST.get('force', "False") == "True"):
                force = True
                
            if plx_path.endswith(".pltp"):
                plx, msg = browser.load_pltp(plx_path, repo_object, force)
                filetype = "PLTP"
            elif plx_path.endswith(".pls"):
                plx, msg = browser.load_pls(plx_path, repo_object, force)
                filetype = "PLS"
            elif plx_path.endswith(".pl"):
                plx, msg = browser.load_pl(plx_path, repo_object)
                filetype = "PL"
                
            if (not plx):
                if (msg):
                    msg = "<br>".join(msg.split("\n"))
                    messages.error(request, msg)
                else:
                    ask_force = True
            elif plx and filetype == "PL":
                msg = "<br>".join(msg.split("\n"))
                request.session['exercise'] = None
                return try_pl(request, plx, msg)
                
            else:
                if msg:
                    msg = "<br>".join(msg.split("\n"))
                    messages.warning(request, msg)
                messages.success(request, "Le "+filetype+" <b>"+plx_path+"</b> a bien été chargé.")
                if filetype == "PLTP":
                    strategy = Strategy.objects.get(name='python')
                    activity = Activity(id=0, pltp=plx, strategy=strategy, name=plx.name)
                    activity.save()
                    url_lti = request.get_host()+"/playexo/activity/lti/"+activity.name+"/"+activity.strategy.name+"/"+activity.pltp.sha1+"/"
                    url_test = "/playexo/activity/test/"+activity.name+"/"+activity.strategy.name+"/"+activity.pltp.sha1+"/"
                    messages.success(request, "L'activité <b>'"+activity.name+"'</b> a bien été créée et a pour URL LTI: <a>"+url_lti+"</a>.<br>&emsp; &emsp; Elle apparaitra dans la liste ci-dessous lorsqu'une personne cliquera sur le lien depuis un client LTI. Pour la tester en local, cliquez <a target=\"_blank\" href=\""+url_test+"\">ici</a>.")
            
        
        if (request.POST.get('refresh', False)):
            browser.get_repo()
    
    browser.parse_content()
    request.session["browser"] = browser.__dict__
    
    path = browser.current_path[browser.current_path.find(browser.name):]
    if (path[-1] != "/"):
        path += "/"
    rel_path = path[len(browser.name)+1:]
    breadcrumb, breadcrumb_value = create_breadcrumb(path)
    
    return render(request, 'gitload/browse.html', {
        'path': path,
        'rel_path': rel_path,
        'browser': browser,
        'breadcrumb': breadcrumb,
        'breadcrumb_value': breadcrumb_value,
        'ask_force': ask_force,
        'exported': plx_path,
    })

@login_required
def view_file(request):
    """ View for [...]/gitload/view_file -- template: view_file.html"""
    if (request.method == 'POST'):
        file_path = request.POST.get('file_path', "")
        if (file_path != ""):
            readed_file = open(DIRREPO+file_path, "r")
            lines = list()
            for line in readed_file:
                lines.append(line)
            readed_file.close()
            
            request.current_app = 'gitload'
            return render(request,  'gitload/view_file.html', {
                'lines': lines,
                'filename': basename(file_path),
            })
    
    return redirect(browse)

@login_required
def edit_file(request):
    """ View for [...]/gitload/edit_file -- template: edit_file.html"""
    if (request.method == 'POST'):
        file_path = request.POST.get('file_path', "")
        
        if (file_path != ""):
            with open(DIRREPO+file_path, "r") as f:
                content  = f.read()
            
            request.current_app = 'gitload' # Interet ?
            return render(request,  'gitload/edit_file.html', {
                'filecontent': content,
                'filename': basename(file_path),
            })
    
    return redirect(browse)

@login_required
def save_file(request):
    """ View for [...]/gitload/edit_file -- template: edit_file.html"""
    if (request.method == 'POST'):
        file_path = request.POST.get('file_path', "")
    
    return redirect(browse)

@login_required
def loaded_pltp(request):
    """ View for [...]/gitload/loaded_pltp -- template: loaded_pltp.html"""
    allpltp = PLTP.objects.all();
    
    if (request.method == 'POST'):
        pltp_delete = request.POST.get('pltp_delete', "")
        rel_path = request.POST.get('rel_path', "")
        repo_name = request.POST.get('repo', "")
        if (pltp_delete != ""):
            try:
                to_del = PLTP.objects.get(sha1=pltp_delete)
                name_del = to_del.name
                to_del.delete()
                messages.warning(request, "Le PLTP <b>"+name_del+"</b> a bien été supprimé !")
            except Exception as e:
                messages.error(request, "Erreur lors de la suppression du PLTP <b>"+name_del+"</b>:<br>"+str(type(e))+": "+str(e))
        
        elif repo_name == "N/A":
            messages.error(request, "<b>Erreur:</b> Impossible de recharger l'activité <b>"+rel_path+"</b> car le dépot asssocié à été supprimé")
        elif (rel_path != "" and repo_name != ""):
            repo = Repository.objects.get(name=repo_name)
            browser = Browser(None, dic=request.session["browser"])
            pltp, msg = browser.load_pltp(rel_path, repo, True)
            strategy = Strategy.objects.get(name='python')
            activity = Activity(id=0, pltp=pltp, strategy=strategy, name=pltp.name)
            activity.save()
            url_lti = request.get_host()+"/playexo/activity/lti/"+activity.name+"/"+activity.strategy.name+"/"+activity.pltp.sha1+"/"
            url_test = "/playexo/activity/test/"+activity.name+"/"+activity.strategy.name+"/"+activity.pltp.sha1+"/"
            if (not pltp):
                messages.error(request, "<b>Erreur:</b> "+msg)
            else:
                messages.success(request, "Le PLTP <b>"+pltp.name+"</b> a été rechargé avec succès !")
                messages.success(request, "L'activité <b>'"+activity.name+"'</b> a bien été créée et a pour URL LTI: <a>"+url_lti+"</a>.<br>&emsp; &emsp; Elle apparaitra dans la liste ci-dessous lorsqu'une personne cliquera sur le lien depuis un client LTI. Pour la tester en local, cliquez <a target=\"_blank\" href=\""+url_test+"\">ici</a>.")
            
    
    return render(request, 'gitload/loaded_pltp.html', {
        'pltp': allpltp,
        'domain': "http://"+request.get_host(),
    })
    
@login_required
def loaded_pls(request):
    """ View for [...]/gitload/loaded_pls -- template: loaded_pls.html"""
    allpls = Strategy.objects.all();
    
    if (request.method == 'POST'):
        pls_delete = request.POST.get('pls_delete', "")
        rel_path = request.POST.get('rel_path', "")
        repo_name = request.POST.get('repo', "")
        
        if (pls_delete != ""):
            try:
                to_del = Strategy.objects.get(name=pls_delete)
                name_del = to_del.name
                to_del.delete()
                messages.warning(request, "Le PLS <b>"+name_del+"</b> a bien été supprimé !")
            except:
                messages.error(request, "Erreur lors de la suppression du PLS <b>"+name_del+"</b>...")
                
        elif (rel_path != "" and repo_name != ""):
            repo = Repository.objects.get(name=repo_name)
            browser = Browser(None, dic=request.session["browser"])
            pls, msg = browser.load_pls(rel_path, repo, True)
            if (not pls):
                messages.error(request, "<b>Erreur:</b> "+msg)
            else:
                messages.success(request, "Le PLS <b>"+pls.name+"</b> a été rechargé avec succès !")
    
    return render(request, 'gitload/loaded_pls.html', {
        'pls': allpls,
    })
    
@login_required
def loaded_pl(request):
    """ View for [...]/gitload/loaded_pl -- template: loaded_pl.html"""
    allpl = PL.objects.all();
    
    return render(request, 'gitload/loaded_pl.html', {
        'pl': allpl,
    })
    
@login_required
def activity(request):
    activities = Activity.objects.all()
    pltps = PLTP.objects.all()
    strategies = Strategy.objects.all()
    activity = None
    
    if (request.method == 'POST'):
        activity_delete = request.POST.get('activity_delete', "")
        activity_name = request.POST.get('activity_name', "")
        activity_pltp = request.POST.get('activity_pltp', "")
        activity_strategy = request.POST.get('activity_strategy', "")
        
        if (activity_delete != ""):
            try:
                to_del = Activity.objects.get(name=activity_delete)
                name_del = to_del.name
                to_del.delete()
                messages.warning(request, "L'Activité <b>"+name_del+"</b> a bien été supprimée !")
            except Exception as e:
                messages.error(request, "Erreur lors de la suppression de l'Activité <b>ID: "+activity_delete+"</b>: "+str(e))
                
        elif (activity_name != "" and activity_pltp != "" and activity_strategy != ""):
            if Activity.objects.get(name=activity_name):
                messages.error(request, "Une activité avec ce nom existe déjà")
            else:
                pltp = PLTP.objects.get(sha1=activity_pltp)
                strategy = Strategy.objects.get(name=activity_strategy)
                activity = Activity(id=0, pltp=pltp, strategy=strategy, name=activity_name)
                activity.save()
                url_lti = request.get_host()+"/playexo/activity/lti/"+activity.name+"/"+activity.strategy.name+"/"+activity.pltp.sha1+"/"
                url_test = "/playexo/activity/test/"+activity.pltp.sha1+"/"+activity.strategy.name+"/"
                messages.success(request, "L'activité <b>'"+activity.name+"'</b> a bien été créée et a pour URL LTI: <a>"+url_lti+"</a>.<br>&emsp; &emsp; Elle apparaitra dans la liste ci-dessous lorsqu'une personne cliquera sur le lien depuis un client LTI. Pour la tester en local, cliquez <a target=\"_blank\" href=\""+url_test+"\">ici</a>.")
            
        
    return render(request, 'gitload/activity.html', {
        'activities': activities,
        'pltps': pltps,
        'strategies': strategies,
        'activity': activity,
        'domain': "http://"+request.get_host(),
    })
