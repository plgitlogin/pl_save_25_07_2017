# Écrire un PL
## Introduction
### Bases
PL est un format de fichier permettant l'écriture d'exercices très différents. L'évaluation ainsi que le formulaire de réponse de l'exercice étant intégré à celui-ci, les possibilités sont quasiment infinis (les limites étant le langage Python ainsi que les différents langages web: HTML, JS, etc...). 

### Format
Le format PL est un ensemble de déclaration de couple clé, valeur. Ces déclarations ce font avec une syntaxe simple que voici:
* "=" (_clé = valeur_) : Permet l'attribution d'une valeur sur une ligne, exemple: _title=Exercice 1_
* "\==" : Permet l'attribution d'une valeur sur plusieurs lignes, de la lignes suivant _clé==_ à la ligne précédant le prochain _==_, exemple:
```
 clé==
 valeur
 sur
 plusieurs
 lignes
 ==
```
* "=@" (_clé =@ valeur_) : Permet d'attribuer le contenu d'un fichier à la clé, exemple: _enonce=@ /python/enonce/exercice3.txt_

### Clés Particulières
Il existe deux clés particulières associées au symbole "=": les clés "_extends_" et "_include_" (_include= /python/patron-exercice.pl_ ou _extends= /python/patron-exercice.pl_):
* _extends_ permet d'étendre un autre fichier, c'est à dire de récupérer l'ensemble des clés de ce fichier puis, si n'importe laquelle de ces clés est aussi déclaré dans votre fichier, cette dernière écrasera celle du fichier étendue.
* _include_ permet d'inclure un autre fichier, c'est à dire ajouter l'ensemble de ce clés à votre fichier, contrairement à _extends_, les clés ajouté peuvent écraser vos clés si le fichier est inclus après la déclaration de celles-ci.
Ces balises permettent d'éviter de devoir réécrire les clés les plus compliquées pouvant servir pour plusieurs exercices (formulaire, fonction d'évaluation, etc...).

### Clés réservées
Bien qu'il soit possible d'attribuer n'importe quel clés, il est important de noté que certaine sont utilisé pour l'interface et pour le traitement de l'exercice, ces clés sont:

###### Pour l'interface:
* _title_ - Titre de l'exercice/feuille d'exercice
* _author_ - Auteur de l'exercice
* _text_ - Énoncé de l'exercice, le contenu de cette clé est affiché comme du markdown.
* _introduction_ - (Présentation de la feuille d'exercice, le contenu de cette clé est affiché comme du markdown. 
* _form_ - Formulaire HTML permettant à l'élève de répondre. Voir la page [Écrire un Formulaire](./formulaire.html).
* _css_ - Permet l'ajout de feuille de style css si le formulaire en nécessite.
* _script\_header_ et _script\_end_ - Permet l'ajout de javascript.

###### Pour le traitement de l'exercice:
* _type_ - Permet de déterminer les clés obligatoires/recommandées, c'est la seul clés obligatoire, peut importe le type.
* _build_ - Code python permettant de créer des variables plus compliqué que celle possible par le PL (liste, dictionnaire, utilisation d'aléatoire, etc...), ce code sera exécuté avant l'affichage et avant l'évaluation de l'exercice.  Voir la page [Écrire une Fonction *build()*](./build.html).
* _evaluator_ - Code python permettant d'évaluer la réponse l'élève. Voir la page [Écrire un Évaluateur](./evaluator.html).
D'autres clés, suivant les types, peuvent être réservées.
Toutes clés déclarées dans _build_ écrasera celle déclaré dans le PL si le même nom est donné.
Voir la page build, evaluator et form pour plus d'information sur ces clés particulière.


### Exemple
Voici un exemple pour un simple QCM avec 4 choix de réponse et 2 bonnes réponses:
```
title=La Tombe de Grant
 
text==
Qui sont les personnes enterrés dans la tombe de Grant?

(Indice: 2 personnes)
==
 
type=direct

extends=/gift/template/multiplechoices_template.pl

answer1=La mère de Grant

answer2=Grant

answer3=La femme de Grant

answer4=Le père de Grant

right_answer1=Grant

right_answer2=La femme de Grant
```

Après application du extends:
```
title=La Tombe de Grant
 
text==
Qui sont les personnes enterrés dans la tombe de Grant?

(Indice: 2 personnes)
==
 
type=direct

build==
def build(dic):
    n=1
    question=list()
    answer=list()
    while ('answer'+str(n) in dic):
        question.append(dic['answer'+str(n)])
        if 'right_answer'+str(n) in dic:
            answer.append(dic['right_answer'+str(n)])
        n += 1
    dic['question'] = question
    dic['answer'] = answer
    return dic
==

form==
<center>
    {% for item in question %}
        <label class="radio-inline">
        <input type="checkbox" value="{{item}}" name="answer">{{item}}
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

answer1=La mère de Grant

answer2=Grant

answer3=La femme de Grant

answer4=Le père de Grant

right_answer1=Grant

right_answer2=La femme de Grant
```
Voici le rendu:
____
![Exemple PL](images/exemple_PL.png "Exemple PL")

## Types Définis
Bien que le format PL permet la création de type d'exercice par les professeurs, certain types ont déjà été définis pour faciliter l'écriture d'exercices.

### Exercice de Programmation Python
Voir la page wiki associé.

### Vrai / Faux
Ce type permet l'écriture rapide d'un vrai/faux. Les seuls clés requises sont les clés _title_, _answer_ (vaut soit "True", soit "False") et _text_.
Il est possible d'écraser _feedback\_correct_ et _feeback\_wrong_ pour des retours personnalisés.
Pour utiliser ce type, il faut étendre: /gift/template/truefalse_template.pl.

Exemple:
```
title=Vrai / Faux
text=Grant a été enterré à New York.
answer=True
extends=/gift/template/truefalse_template.pl
```

Voici le contenu du patron:
```
type=direct
feedback_correct=Bonne réponse
feedback_wrong=Mauvaise réponse

form==
<center>
    <label class="radio-inline">
        <input id="form_txt_answer" type="radio" value="True" required> Vrai
    </label>
    <label class="radio-inline">
        <input id="form_txt_answer" type="radio" value="False" > Faux
    </label>
</center>
==

evaluator==
def evaluator(reponse, dic):
    if (str(dic['answer']) == reponse['answer']):
        return True, str(dic['feedback_correct'])
    return False, str(dic['feedback_wrong'])
==
```

### QCM a Réponse Unique
Ce type permet l'écriture rapide d'une QCM avec une seule bonne réponse. Les seuls clés requises sont les clés _title_, plusieurs _answerX_, _right_answer_ et _text_.
Pour utiliser ce type, il faut étendre: /gift/template/select_template.pl.

Exemple:
```
title=QCM
text=Qui est enterré dans la tombe de Grant?
extends=/gift/template/select_template.pl
answer1=Grant
answer2=Personne
answer3=Napoleon
answer4=Churchill
answer5=Mother Teresa
right_answer=Grant
```

Il est aussi possible d'ajouter un feedback pour chaque réponse avec _feedbackX_ où X correspond à la réponse et _right\_feedback_ pour le retour de la bonne réponse:
```
title= QCM Feedback
text=Qu'est-ce qui est entre le orange et le vert sur le spectre des couleurs?
extends=/gift/template/select_template.pl
answer1=Jaune
answer2=Rouge
answer3=Bleu
feedback2=Non, c'est le jaune !
feedback3=Non, c'est le jaune !
right_answer=Jaune
right_feedback=Excellent !
```

Voici le contenu du patron:
```
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
        <input id="form_txt_answer" type="radio" value="{{item}}" required>{{item}}
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
```

### Réponse Courte
Ce type permet l'écriture rapide d'une question nécessitant une courte réponse à taper (un nom, un nombre, etc...). Les seuls clés requises sont les clés _title_, plusieurs _answerX_, _right_answer_ et _text_.
Il est possible d'écraser _feedback\_correct_ et _feeback\_wrong_ pour des retours personnalisés.
Pour utiliser ce type, il faut étendre: /gift/template/short_template.pl.

Exemple:
```
title=Short
text=Deep Thought said:
extends=/gift/template/short_template.pl
answer=forty two
correct_feedback=Correct according to The Hitchhiker's Guide to the Galaxy!
wrong_feedback=Incorrect !
```

Il est aussi possible de préciser plusieurs réponses possibles, ainsi que des retours correspondants:
```
title=Short
text=Deep Thought said:
extends=/gift/template/short_template.pl
answer1=forty two
answer2=42
answer3=forty-two
feedback1=Correct according to The Hitchhiker's Guide to the Galaxy!
feedback2=Correct, as told to Loonquawl and Phouchg
feedback3=Correct!
```

Voici le contenu du patron:
```
type=direct

form==
<div class="input-group">
    <span class="input-group-addon">Réponse</span>
    <input id="form_txt_answer" type="text" class="form-control" placeholder="" required>
</div>
==

evaluator==
def evaluator(response, dic):
    if 'answer' in dic:
        if response['answer'] == dic['answer']:
            if 'correct_feedback' in dic:
                return True, dic['correct_feedback']
            return True, "Bonne réponse"
        else:
            if 'wrong_feedback' in dic:
                return False, dic['wrong_feedback']
            return False, "Mauvaise réponse"
    else:
        n = 1
        answer = list()
        while ('answer'+str(n) in dic):
            ans = dic['answer'+str(n)]
            if ('feedback'+str(n) in dic):
                fee = dic['feedback'+str(n)]
            else:
                fee = ('Bonne réponse')
            answer.append((ans, fee))
            n += 1
        
        for answer, feedback in answer:
            if response['answer'] == answer:
                return True, feedback
        if 'wrong_feedback' in dic:
                return False, dic['wrong_feedback']
            return False, "Mauvaise réponse"
==
```

### Réponse Numérique
Ce type permet l'écriture rapide d'une question demandant une réponse se situant dans un intervalle. La réponse ne peut qu'être un nombre entier ou un nombre décimale. Les seuls clés requises sont les clés _title_, _mini_ et _maxi_, et _text_.
Pour utiliser ce type, il faut étendre: /gift/template/numeric_template.pl.

Exemple:
```
title=Intervalle
text=Donnez un nombre entre 1 et 5.
extends=/gift/template/numeric_template.pl
mini=1
maxi=5
```

Voici le contenu du patron:
```
type=direct

form==
<div class="input-group">
    <span class="input-group-addon">Réponse</span>
    <input id="form_txt_answer" type="text" class="form-control" placeholder="" required>
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
```


### QCM
Ce type permet l'écriture rapide d'un QCM. Les seuls clés requises sont les clés _title_, plusieurs _answerX_, 1 ou plusieurs _right_answerX_ et _text_.
Pour utiliser ce type, il faut étendre: /gift/template/multiplechoices_template.pl.

Exemple:
```
title=La Tombe de Grant

text==
Qui sont les personnes enterrés dans la tombe de Grant?

(Indice: 2 personnes)
==

type=direct
template=/gift/template/multiplechoices_template.pl
answer1=La mère de Grant
answer2=Grant
answer3=La femme de Grant
answer4=Le père de Grant
right_answer1=Grant
right_answer2=La femme de Grant
```

Voici le contenu du patron:
```
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
```

### Correspondance
Ce type permet l'écriture rapide d'un exercice ou il faut faire correspondre plusieurs réponses. Les seuls clés requises sont les clés _title_, plusieurs_questionX_, plusieurs _answerX_ où _answerX_ est la réponse à _questionX_, et _text_.
Pour utiliser ce type, il faut étendre: /gift/template/match_template.pl.

Exemple:
```
title=Match
text=Which animal eats which food?
template=/gift/template/match_template.pl
question1=cat 
question2=dog 
answer1= cat food
answer2= dog food
```

Voici le contenu du patron:
```
type=direct

build==
def build(dic):
    n=1
    answer = dict()
    question_list = list()
    answer_list = list()
    while ('answer'+str(n) in dic):
        answer_list.append(dic['answer'+str(n)])
        question_list.append(dic['question'+str(n)])
        answer[dic['question'+str(n)]] = dic['answer'+str(n)]
        n += 1
    dic['answer'] = answer
    dic['answer_list'] = answer_list
    dic['question_list'] = question_list
    return dic
==


css==
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.12.2/js/bootstrap-select.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.12.2/css/bootstrap-select.min.css">
==

form==
<center>
    <div style="display: inline-block; vertical-align: middle;">
        {% for item in question_list %}
            <span class="input">{{item}}:</span>
            <select id="form_txt_{{item}}" class="selectpicker" style="display: inline-block; vertical-align: middle;" title="Réponse" required>
                {% for item2 in answer_list %}
                    <option value="{{ item2 }}">{{item2}}</option>
                {% endfor %}
            </select>
            <br>
            <br>
        {% endfor %}
    </div>
</center>
==

evaluator==
def evaluator(reponse, dic):
    if (reponse == dic['answer']):
        return True, "Bien joué"
    return False, "Mauvais matching"
==
```

### Description
Ce type permet d'entrée un simple texte (explication, rappel de cours, etc...), il ne contient donc pas de formulaire.


Exemple:
```
title=Description
text=You can use your pencil and paper for these next math questions.
type=description
evaluator=def evaluator(reponse, dico): return True, 'Merci pour votre lecture'
```


## Créer un nouveau type
La syntaxe PL permettant d'inclure ou d'étendre d'autre fichier, il est possible (et recommandé) de créer nouveau type.

Ces types doivent pouvoir être utilisés en déclarant le moins de clés possibles, afin de faciliter l'écriture de futures exercices. Les principales clés permettant de définir un nouveau type sont les clés:
* [build](./build.html) (optionnel)
* [form](./formulaire.html)
* [evaluator](./evaluator.html)

Ce sont les clés *form* et *evaluator* qui permettent de "normer" l'exercice et de définir l'interface de réponse, ainsi que la façon d'évaluer l'exercice. Cela peut être aussi une bonne pratique de crée des *feedback* par défaut.

Pour des exemples, vous pouvez référer aux patrons des types d'exercices déclarés plus haut.
