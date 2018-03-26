# Constraint-Based Grammar

## Rules Format

```
Operator Target Context Conditions
```

* Operator

'=!!' indicates that the target reading is the correct one if and only if all context conditions are satisfied; all other readings should be discarded. If the context conditions are not satisfied, the target reading itself is discarded.

‘=!’ indicates that the target reading is the correct one if and only if all context conditions are satisfied, all other readings are discarded.

‘=0’ indicates that the target reading will be discarded if and only of the context conditions are satisfied, it leaves all other readings. 

* Context Condition

```
Position [Careful Mode] POS Tag
```
Position (1, 0, ...)

Careful Mode = Appending character c to the position number requires the respective condition to be satisfied only if the cohort being tested is itself unambiguous
