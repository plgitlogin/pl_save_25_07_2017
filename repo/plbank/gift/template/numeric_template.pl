#  Author: Coumes Quentin     Mail: qcoumes@etud.u-pem.fr
#  Created: 2017-06-29
#  Last Modified: 2017-06-29

type=direct

form==
<div class="input-group">
    <span class="input-group-addon">Réponse</span>
    <input id="form_txt_answer" type="number" class="form-control" placeholder="" required>
</div>
==

evaluator==
def evaluator(response, dic):
    try:
        float(response['answer'])
    except:
        return False, "Merci de rentrer un entier ou un flottant"
       
    if float(response['answer']) >= float(dic['mini']) and float(response['answer']) <= float(dic['maxi']):
        return True, 'Bonne réponse'
    return False, 'Réponse incorrecte'
==
