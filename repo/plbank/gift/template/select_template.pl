
#  Author: Coumes Quentin     Mail: qcoumes@etud.u-pem.fr
#  Created: 2017-06-29
#  Last Modified: 2017-06-29

type=direct

build==
def build(dic):
    n=1
    answer=list()
    while ('answer'+str(n) in dic):
        answer.append(dic['answer'+str(n)])
        n += 1
    dic['answer'] = answer
    return dic
==


form==
<center>
    {% for item in answer %}
        <label class="radio-inline">
        <input id="form_txt_answer" type="radio" value="{{item}}" name="answer" required>{{item}}
        </label>
    {% endfor %}
</center>
==

evaluator==
def evaluator(reponse, dic): 
    if reponse['answer'] == dic['right_answer']:
        if 'right_feedback' in dic:
            return True, dic ['right_feedback']
        else:
            return True, "Bonne réponse"
    
    for i in range(len(dic['answer'])): # Getting the corresponding wrong feedback
        if reponse['answer'] == dic['answer'][i]:
            if 'feedback'+str(i+1) in dic:
                return False, dic['feedback'+str(i+1)]
            else:
                break
    return False, "Mauvaise Réponse"
==
