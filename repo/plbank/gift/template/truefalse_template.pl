#  Author: Coumes Quentin     Mail: qcoumes@etud.u-pem.fr
#  Created: 2017-06-29
#  Last Modified: 2017-06-29

type=direct

feedback_correct==
Bonne réponse
==

feedback_wrong==
Mauvaise réponse
==

form==
<center>
    <label class="radio-inline">
        <input id="form_txt_answer" type="radio" value="True" name="answer" required> Vrai
    </label>
    <label class="radio-inline">
        <input id="form_txt_answer" type="radio" value="False" name="answer"> Faux
    </label>
</center>
==


evaluator==
def evaluator(reponse, dic):
    if (str(dic['answer']) == reponse['answer']):
        return True, str(dic['feedback_correct'])
    return False, str(dic['feedback_wrong'])
==
