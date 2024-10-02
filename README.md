# EvalRTS: An artifact to evaluate Regression Test Selection tool  

Regression test selection (RTS) tool performs a crucial role on the e cient testing of software while
the codebase undergoes different versions within its life-cycle. Instead of running all the test cases
blindly on the changed versions of the code, an RTS tool selects a group of test cases which ensures
to validate the previously and newly introduced features. But the e ectiveness of an RTS tool largely
depends on  finding fewer test cases and not missing any test cases for a changed version. 

In this work, we have tried to evaluate an RTS tool, 'babelRTS' via mutation operation and then testing
its e ectiveness  nding how many it misses out of all the killable mutants. An RTS tool can work
on multiple language. Here in this project we are focused on java environment. In this work, we
have taken 9 java projects having varieties of  le sizes and performed mutation and evaluation. Our
developed tool has evaluated that babelRTS can kill 96% of killable mutants. As RTS tools are
becoming used for multi-lingual support, we have also developed our evaluation tool having multi-
lingual support.

## Pseudocode
```
-killable_mutants = 0 
-killed_mutants = 0
For revision In revisions: 
    -compile and test revision
    −runBabelRTS
    For i=0 To MAX_TIMES: 
        -choose random source file
        -choose random line in source file 
        -delete line
        -compile and test revision
        If mutant Is killed: 
            -killable_mutants = killable_mutants + 1 
            -run BabelRTS
            -run selected tests
            If mutant Is killed: 
                -killed_mutants = killed_mutants + 1 
Return killed_mutants/killable_mutants 

```

## Evaluation Metrics

**Mutation operation**: Program Mutation generates alternate programs (mutants), each of which di ers from
the original by a minor syntactic change, and then requests that the tester construct inputs to eliminate the
mutants by making each mutant provide a di erent result from the original version.

**Killable Mutants**: if anytest cases fail or provide erroneous output on a mutant, that mutant is killable.

**Killed Mutants:** we target to evaluate a RTS tool to see if it can generate a group of
test cases to have an e ect on the found killable mutants. Again, we are considering test cases faliure to determine
if the selected test suites by provided any RTS tool have an e ect on those killabled mutant. If they have an
e ect, those mutants are called killed mutants.


