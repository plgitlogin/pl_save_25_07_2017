
import json
from django.shortcuts import get_object_or_404
from pysrc.plrequest import SandboxSession
from sandbox.models import Sandbox

def evaluator(reponse, dic):
    sandbox = get_object_or_404(Sandbox, name="php-sandbox")
    sandbox_session = SandboxSession(dic, reponse['answer'], sandbox.url)
    feedback = json.loads(sandbox_session.call())
    if feedback['grade']['success']:
        return True, feedback['grade']['feedback']
    return False, feedback['grade']['feedback']

