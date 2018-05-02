# Cebuano POS Tagger

```
A Rule-Based Cebuano POS Tagger Using Constraint-Based Grammar
```
POS Tagset |
--- |
ADJ |
ADV | 
CONJ |
DET |
NOUN |
NUM |
OTH |
PART |
SYM |
VERB |

## Installation

* `pip install cebpostagger`
* Inside the project folder `python setup.py install`

## Requirements
* `cebstemmer`
* `cebdict`


## Functions
* tag_sentence(text='')
  - Accepts a Cebuano sentence and returns a list of tuples in (WORD, TAG) format
  Output:
    `[(WORD1, TAG), (WORD2, TAG)]`

## How To Use

```
from cebpostagger.tagger import tag_sentence

tagged = tag_sentence('Ang bata naligo sa sapa.')
print(tagged)

[('Ang', 'DET'), ('bata', 'NOUN'), ('naligo', 'VERB'), ('sa', 'PART'), ('sapa', 'NOUN'), ('.', 'SYM')]
```

## Evaluation

![image](https://user-images.githubusercontent.com/24803247/39524926-2a0bfb08-4e4d-11e8-8771-d228b1873ddc.png)

![image](https://user-images.githubusercontent.com/24803247/39524955-3e11dc94-4e4d-11e8-9a08-1192ebed8d72.png)

![image](https://user-images.githubusercontent.com/24803247/39524986-4fb03004-4e4d-11e8-8b3c-2998e30499b4.png)

## References

*  Alfred, R., Mujat, A., & Obit, J. H. (2013). A Ruled-Based Part of Speech (RPOS) Tagger for Malay Text Articles. In A. Selamat, N.          T. Nguyen, & H. Haron (Eds.), Intelligent Information and Database Systems (Vol. 7803, pp. 50–59). Berlin, Heidelberg: Springer 
       Berlin Heidelberg. https://doi.org/10.1007/978-3-642-36543-0_6
       
*  Eckhard, B. (2006). A Constraint Grammar-Based Parser for Spanish.
      In TIL 2006 - 4th Workshop on Information and Human Language Technology. 
      Ribeirão Preto. Retrieved from https://visl.sdu.dk/pdf/TIL2006.pdf

*  Karlsson, F. (1990). Constraint grammar as a framework for parsing running text (Vol.   
      3, pp. 168–173). Association for Computational Linguistics.    
      https://doi.org/10.3115/991146.991176

*  Lindberg, N., & Einoborg, M. (1998). Induction of Constraint Grammar-rules using   
      Progol. In International Conference on Inductive Logic Programming (Vol. 1446, 
      pp. 116–124). Springer, Berlin, Heidelberg. 
      Retrieved from https://link.springer.com/chapter/10.1007/BFb0027315
      
*  Petrov, S., Dipanjan, D., & McDonald, R. (2012). A Universal Part-of-Speech Tagset. 
       In LREC. Retrieved from http://www.petrovi.de/data/lrec.pdf

*  Tanangkinsing, M. (2009). A Functional Reference Grammar of 
       Cebuano (Dissertation). National Taiwan University, Taiwan.
