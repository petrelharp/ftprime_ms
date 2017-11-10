Units

| parameter          | msprime | ftprime | fwdpy11_arg_example |
| -------------      | ------------- | ------------- | ------------- |
|  time | generations  | generation | generations  | generations |
| genome | base pairs  | base pairs  | ?  |
| recombination rate | 1/base * 1/generation  | 1/base * 1/generation  [1] | ?  |
| mutation rate      | 1/base * 1/generation| 1/base * 1/generation [2]  | ?  |

[1] I think the above is true regardless of if we use distance-based `intensity=` or uniform `rates=` [parameterizations in simuPOP](http://simupop.sourceforge.net/manual_svn/build/refManual_ch3_sec5.html?highlight=recombinator#Recombinator.Recombinator).
The test runs were done with `rates=`.

[2] We use an [SNPMutator](http://simupop.sourceforge.net/manual_svn/build/refManual_ch3_sec6.html?highlight=mutation%20rate#class-snpmutator) and apply it once per generation. There, the rate "specifies the probability at which each allele mutates to another" so it's per allele, but we apply it to all available loci so it's per base-pair.


Scalings

| parameter          | msprime | ftprime | fwdpy11_arg_example |
| -------------      | ------------- | ------------- | ------------- |
|  time | generations  | ?  | ?  | ? |
| recombination rate | ?  | ?  | ?  |
| mutation rate      | ?  | ?  | ?  |
