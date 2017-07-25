from pysrc.newcheck import checkplfile, checkpltpfile
from gitload.loader import loadPL, loadPLTP
from gitload.models import Repository
from pleditor import check_dic_pl, check_dic_pltp, get_zip_value

import pytest, hashlib, json


@pytest.mark.django_db
def test_checkplfile_succeed():
    r = Repository(name="plbank",url="elsewhere",version=1)
    assert(checkplfile("/test/allwayscorrect.pl", r, sandboxurl = "http://127.0.0.1:8000/sandbox/?action=execute"))

@pytest.mark.django_db
def test_checkplfile_failed():
    r = Repository(name="plbank",url="elsewhere",version=1)
    assert not (checkplfile("/test/bad_grader.pl", r, sandboxurl = "http://127.0.0.1:8000/sandbox/?action=execute"))

@pytest.mark.django_db
def test_checkpltpfile_succeed():
    r = Repository(name="plbank",url="elsewhere",version=1)
    assert(checkpltpfile("/test/alwayscorrect.pltp", r, sandboxurl = "http://127.0.0.1:8000/sandbox/?action=execute"))
    
@pytest.mark.django_db
def test_checkpltpfile_failed():
    r = Repository(name="plbank",url="elsewhere",version=1)
    assert not (checkpltpfile("/test/bad_pl_grader.pltp", r, sandboxurl = "http://127.0.0.1:8000/sandbox/?action=execute"))
