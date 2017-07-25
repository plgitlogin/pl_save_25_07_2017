# Bienvenue sur la documentation du projet Premier Langage!


La documentation du projet Premier Langage se découpe en qutres
grandes sections suivant la position dans laquelle vous utilisez le
projet.



## Manuel utilisateur élève

* Description du tableau de bord
* Comment ça marche
* Description des stratégies accessibles
* Comment réviser en autonomie
* Pourquoi les enseignants sont-ils des bourreaux d'enfants ?


## Manuel utilisateur enseignant

* Comment écrire des exos `exo_exemple.pl`
* Comment faire un énoncé de travaux pratique `exemple.pltp`
* Description des graders accessibles
* ... La vie de Dominique Revuz ...
* Écrire un grader


## Manuel du developpeur

* Organisation du projet
* Articulation plserveur <--> plressources
* Comment contribuer, design et manière de travailler
* Rapporter un bug, établir une demande
* Git niveau 1
* Sphinx et documentation

* [Exemple de fichier Python produisant un documentation Sphinx correcte](misc/doc_exemple.html)

* [Titre1](bon fichier.md)
* [Titre2](bon fichier2.md)



# Tests de fichiers sources à documenter


Les trucs suivants ont été automatiquement générée à partir des
sources dégueulasses que des gens aimables ont accepté de tapper
jusque aujourd'hui.


* [Grader](pysrc/plgrader.html)
* [Editor](pysrc/pleditor.html)
* [ErrorPL](pysrc/pl.html)



```
Virer tous les tests Sphinx suivants ou les mettre dans une section
qui explique comment contribuer à Premier Langage et pondre de la
documentation.
```

$$ \sum_{n=0}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{2} $$


```Python
def ceci_est_un_test(arg):
    return arg*arg
```

Voci un autre test de code Python un peu plus long

```Python
def partition(myList, start, end):
    pivot = myList[start]
    left = start+1
    right = end
    done = False
    while not done:
        while left <= right and myList[left] <= pivot:
            left = left + 1
        while myList[right] >= pivot and right >=left:
            right = right -1
        if right < left:
            done= True
        else:
            # swap places
            temp=myList[left]
            myList[left]=myList[right]
            myList[right]=temp
    # swap start with myList[right]
    temp=myList[start]
    myList[start]=myList[right]
    myList[right]=temp
    return right

def quicksort(myList, start, end):
    if start < end:
        # partition the list
        pivot = partition(myList, start, end)
        # sort both halves
        quicksort(myList, start, pivot-1)
        quicksort(myList, pivot+1, end)
    return myList
```

Dingue, Sphinx s'est aussi fair le C gratuitement... Décidement, Si
Revuz ne veut pas de Sphinx, là, je ne saurais plus quoi faire.

```C
int ca_marche_pour_le_c(int ou_bien, char* maison){
  printf("J'habite ici : %s\n", maison);
  return ou_bien*12;
}
```

Test de modification affectant le .gitignore
