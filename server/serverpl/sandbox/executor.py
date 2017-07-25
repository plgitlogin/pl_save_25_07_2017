
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,Http404

from uuid import uuid4
import json
import os
import zipfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import subprocess




class Executor:
    def __init__(self,request):
        self.containername = None
        
        # New DIR contenant tout les fichiers passé en parametre dans FILES
        unique=str(uuid4())
        self.dirname = os.path.join(settings.MEDIA_ROOT, unique)
        os.mkdir(self.dirname)
        for filename in request.FILES.keys():
            path = default_storage.save(unique+"/"+filename, ContentFile(request.FILES[filename].read()))
        
        #self.tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        self.dirname = os.path.join(settings.MEDIA_ROOT, unique)
        

        

    def execute(self):
        os.chdir(self.dirname)
        # FIXME la ligne suivante doit disparaitre 
        try:
            zip_ref = zipfile.ZipFile(self.dirname+"/environment.zip", 'r')
            zip_ref.extractall(self.dirname)
            zip_ref.close()
            xx = subprocess.check_output(['python3','grader.py'])
        except Exception as e:
            errormessage={"feedback":" Erreur de la plateforme \npassez à l'exercice suivant\nMerci de votre compréhension\n\n("+str(type(e))+": "+str(e)+")", 'success':True}
            dico_response = {"platform_error":[str(e)] ,"grade":errormessage}
            os.chdir("..")

            return json.dumps(dico_response)
        os.chdir("..")
        dico_response = {"platform_error":[] ,"grade":json.loads(xx.decode("UTF-8"))}
        dico_response['path_files'] = self.dirname
        return json.dumps(dico_response)

def letsrock(request):
    executor=Executor(request)
    return HttpResponse(executor.execute())

"""
def buildDockerInvocation():
    ["docker","run","-v",HostPath+":"+InnerPath+":rw","-a", "stdin","-a","stdout","-a","stderr"].append(Env_Var).append(["--rm=true", "--net=none","-m",memlimit,"--cpu-shares", CPU_SHARES,"--cpu-period",CPU_PERIOD,"--cpu-quota",CPU_QUOT,"-v",SFTP_PATH+":"+SFTP_INNER_PATH+":ro","--name",CONTAINER_NAME","execute_in_environment",
"""
