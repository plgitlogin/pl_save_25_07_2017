#  Author: Coumes Quentin     Mail: qcoumes@etud.u-pem.fr
#  Created: 2017-06-29
#  Last Modified: 2017-06-29

type=direct

build==
def build(dic):
    d= dict(dic)
    n=1
    question=list()
    answer=list()
    while ('answer'+str(n) in dic):
        question.append(dic['answer'+str(n)])
        if 'right_answer'+str(n) in dic:
            answer.append(dic['right_answer'+str(n)])
        n += 1
    d['question'] = question
    d['answer'] = answer
    return d
==


form==
<center>
    {% for item in question %}
        <label class="checkbox-inline">
        <input type="checkbox" id="form_txt_answer" value="{{item}}"> {{item}}
        </label>
    {% endfor %}
</center>
==

evaluator==
def evaluator(reponse, dic):
    if not 'answer' in reponse:
        return False, "Merci de cocher au moins une case"
    if len(reponse['answer']) == len(dic['answer']):
        for answer in dic['answer']:
            if not answer in reponse['answer']:
                return False, "Réponse incorrect"
        return True, "Bonne réponse"
    return False, "Réponse incorrect"
==
