library(matrixcalc)

N <- 60

# get the WF transition matrix
# stirling number of the second kind:
# S[n,k] = number of ways to partition n elements into k nonempty sets
S <- stirling.matrix(N)[-1,-1]
lS <- log(S)
# P[n,k] = prob put n balls in N boxes and have exactly k nonempty boxes somewhere
#        = S[n,k] * choose(N,k) * factorial(k) / N^n
P <- exp( sweep(lS, 2, lchoose(N,1:N) + lfactorial(1:N), "+") - (1:N) * log(N) )
stopifnot(all(abs(P[upper.tri(P,diag=FALSE)]) < 1e-8))
P[upper.tri(P,diag=FALSE)] <- 0
P[!is.finite(P)] <- 0
stopifnot(all(abs(rowSums(P) - 1) < 1e-8))


# Solve for the mean occupation times:
#  v[n,k] = mean time spent at k starting at n
#         = delta(n,k) + sum_j( P[n,j] * v[j,k] )
# for k > 1
#  v = I + P %*% v
V <- forwardsolve(diag(N-1) - P[-1,-1], diag(N-1))
# T[n] = expected total length of tree starting at n
T0 <- rowSums(sweep(V, 2, 2:N, "*"))

# Or, do this directly:
#  T[n] = n + sum_j( P[n,j] * T[j] )
#  T = (2:N) + P %*% T
T1 <- forwardsolve(diag(N-1) - P[-1,-1], 2:N)

# coal expectation
Tcoal <- 2 * N * cumsum(1/(2:N-1))

layout(1:2)

plot(2:N, T1, type='l', ylim=range(0,T1,finite=TRUE),
     xlab='number of initial leaves',
     ylab='expected total tree length',
     main=paste("N =", N))
lines(2:N, T0, col='green')
lines(2:N, Tcoal, col='red')
legend("bottomright", lty=c(1, 1, 1), col=c('black', 'green', 'red'),
       legend=c('WF', 'WF', 'coalescent'))

plot(2:N, T1/Tcoal, type='l',
     xlab='number of initial leaves',
     ylab='ratio of total tree length, WF to coal',
     main=paste("N =", N))

