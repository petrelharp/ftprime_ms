nedges <- read.csv("data/simplify_num_edges.dat", header=TRUE)[,-1]
subsample <- read.csv("data/simplify_subsample.dat", header=TRUE)[,-1]

pdf(file="simplify_timings.pdf", width=4, height=2.4, pointsize=10)
layout(t(1:2), widths=c(1.2,1))
par(mar=c(3.5,3.5,0.5,0.5)+.1, mgp=c(2.2,1,0))
plot(nedges, type='b', xlab="number of edges", ylab="time (seconds)",
     ylim=range(0,nedges$time))
par(mar=c(3.5,0.5,0.5,1)+.1)
plot(subsample, type='b', xlab="subsample size", ylab="", yaxt='n',
     log='x',
     ylim=range(0,subsample$time))
dev.off()

