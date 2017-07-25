[//]: # (-*- coding: utf-8 -*-)

[//]: # (Copyright 2017 Dominique Revuz <dominique . revuz at u-pem dot fr>)
[//]: # (2017 Nicolas Borie <nicolas . borie at u-pem dot fr>)
 
[//]: # (Distributed under the terms of the GNU General Public License)
[//]: # (as published by the Free Software Foundation; either version 2 of)
[//]: # (the License, or any later version.)
[//]: # (http://www.gnu.org/licenses/)

# Documentation de Premier Langage avec Sphinx.

Cette page rassemble quelques possibilités de formatage de différent
styles de texte avec Sphinx et le langage Markdown. Cette page doit
être visionnée conjointement avec son code source. Ainsi, vous pourrez
écrire votre documentation en copiant partiellement des parties bien
choisies.

## Mise en page des sections d'un document

Le simple dièse suivi d'un espace introduira un titre de page de
documentation `# Titre page.` produit ainsi

# Titre page.

Un titre de grande section se fait avec deux dièse contigus avant
l'espace. `## Section` donne le rendu qui suit

## Section.

Trois dièses pour les sous sections `### Sous section`

### Sous section.

Et ainsi de suite...

#### Sous sous section.

Ne pas trop utiliser de hiérarchie, trois niveau de titre, c'est bien!
Si les sous sections ne suffisent plus, il est peut-être temps de
scinder votre documentation en plusieurs pages relié par des liens.

##### Sous sous sous section.

Les cinq dièses donnent ici un titre dont la taille de police est fort
petite.

## Mettre en place des liens

Pour faire un lien, il faut mettre la chaîne de caractères cliquable
entre crochets puis accolé directement l'adresse du lien entre
parenthèse. Ainsi l'écriture suivante
`[Google](http://www.google.fr/)` donnera le lien cliquable
suivant [Google](http://www.google.fr/).


Pour un lien interne, on place toujours la chaîne cliquable entre
crochet mais l'url devient un chemin relatif dans l'arborescence des
sources du projet Premier Langage. Pour aller vers la page d'entrée de
la documentation, cela donne l'écriture
`[Documentation Premier Langage](../index.html)` qui produit alors le
lien [Documentation Premier Langage](../index.html).


La chaîne `![Logo de Markdown](../doc/logo_markdown.png)` donnera
l'inclusion de l'image pointé dans le document. On peut placer une URL
externe entre les parenthèses, l'image sera alors potentiellement
charger depuis le web.

![Logo de Markdown](../doc/logo_markdown.png)


## Emphase de texte

On peut *mettre en emphase* un bout de texte en le placant entre des
étoiles `*`.

On peut aussi _mettre en emphase_ un bout de texte en le placant entre des
underscores `_`.

Placer entre **double étoiles** produit un autre effet `**`.

De même que pour les __double underscores__ `__`.

***Tripler les étoiles*** produit cet effet `***`.

De ___la même façon___ pour le triple underscore `___`.

Part soucis de lisibilité et par cohérence, Premier Langage préféra
l'utilisation des étoiles pour mettre du texte en emphase.

On peut citer du texte, comme dans un mail en introduisant les lignes
avec un chevron pointant à droite suivi d'un espace. Ainsi, Charles
Antony Richard Hoare déclare en 2009 en conférence :


> Je l’appelle mon erreur à un milliard de dollars. Il s'agit de
> l'invention de la valeur null pour un pointeur, en 1965. À l'époque,
> je concevais le premier système de typage complet pour un langage
> orienté objet (Algol W). Je voulais m'assurer que tout usage de
> références était absolument sûr, avec un test effectué
> automatiquement par le compilateur. Mais je n'ai pas pu résister à
> ajouter la référence nulle, simplement parce que c'était si facile à
> implémenter. Ceci a conduit à un nombre incalculable d'erreurs, de
> déficiences, de plantages de système, qui ont probablement causés
> des problèmes et des dommages d'un milliard de dollars dans les
> quarante dernières années.


## Listes et énumération

On obtient une liste non ordonnée en plaçant une étoile et un espace
`* ` avant chaque item.

* une chose
* une autre
* un truc
* un bidule

On peut ordonnée en spécifiant un nombre à droite duquel on a accolé
un point.

1. une première chose
2. une autre chose
3. suivi d'un truc
4. finissant par un bidule
 
Enfin, une liste en mode case à cocher avec les symboles `- [ ]` et `-
[X]`.

- [ ] Choisir le format reStructuredText pour la doc Sphinx de Premier Langage.
- [X] Préférer Markdown pour la documentation de premier langage.


## Afficher des symboles mathématiques avec du code latex

Le bout de code latex `\sum_{n=1}^{\infty} \frac{1}{n^2} =
\frac{\pi^2}{6}` placé entre deux balise double dollars donnera
l'effet suivant :

$$
\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}
$$

Pour les curieux, ce rendu est assuré par l'utilitaire *mathjax*.

Sphinx et markdown ne supporte pas encore l'insertion en milieu de
phrase. Pour le moment, l'équation $E = m c^2$ n'est probablement pas
affiché correctement avec l'exposant en hauteur et l'accent
circonflexe élidé.

Toutefois l'affichage en mode environnement ainsi que inliné est
correct dans une activité Premier Langage. 

## Documenter du code écrit dans le langage Python.

Voici un premier exemple avec une implantation récursive d'une
factorielle. Le code Python est placé entre deux balises
d'environnement tagué par la spécification Python (triplé de backquote
avec le mot Python directement accolé à droite). La balise de
fermeture d'environnement (triple backquotes) n'est pas taguée.

```Python
def factorial(n):
    r"""
    Returns the factorial of the integer `n` given in argument.
    
    EXAMPLES::

        print(factorial(5))
        120
	
    """
    if n < 0:
		# We raise an error for negative numbers.
        raise ValueError('{} should be a non negative integer'.format(n))
    if n <= 1:
        return 1
    return n*factorial(n-1)
```

On peut facilement présenter un comportement dans l'interpréteur
Python en utilisant toujours l'environnement Python mais en rajoutant
un prompt devant chaque ligne donné à l'interpréteur. Le prompt idoine
en Python est le triple chevron pointant à droite. Ici l'affichage du
résultat rendu lors d'un appel à la fonction factorial définie plus
haut donne :

```Python
>>> print(factorial(6))
720
```

## Documenter du code écrit dans le langage C.

L'environnement C permet d'inclure du code C dans la documentation. Le
code cité sera alors placé dans un bloc idoine avec une police à
chasse fixe. Aussi Sphinx assure une coloration syntaxique
raisonnable. La balise ouvrant l'environnement est le triple backquote
avec la spécification C accolé sans espace au triplé de backquotes.


Pour un fichier `fact.c` dont le contenu est le suivant :

```C
#include <stdio.h>
#include <stdlib.h>

int factorial(int n){
	/* We stop the programm if the function is called with a negative integer. */
	assert(n >= 0, "n should be a non negative integer.");
	if n <= 1:
		return 1;
	else:
		return n*factorial(n-1);
}

int main(int argc, char* argv[]){
	int n;
	
	n = atoi(argv[1]);
	printf("La factorielle de %d est : %d\n", n, factorial(n));
	return 0;
}
```

On peut alors présenté un résultat en terminal en utilisant
l'environnement `pre`.

<pre>
user@machine~$ gcc -o test fact.c -Wall
user@machine~$ ./test 5
La factorielle de 5 est : 120
user@machine~$
</pre>

Ici, la chaîne de caractères pour le prompt est `user@machine~$` qui
rappelle un classique *bash* disponible sous système de type *Unix*.
