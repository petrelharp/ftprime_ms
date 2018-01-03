library(stringr)

files = list.files(path='.',pattern=glob2rx("time_arg.*.out"))

data = NA
for (i in files)
{
    x = str_split(i,"\\.")
    N = x[[1]][2] %>% str_replace_all("[A-Z]","")
    size = x[[1]][3]%>% str_replace_all("[a-z]","")
    GC = x[[1]][4]%>% str_replace_all("[A-Z]","")

    d=read.table(i)
    if(is.na(data))
    {
    data = data.frame(list(N=as.numeric(N),
                                      size=as.numeric(size),
                                      GC=as.numeric(GC),
                                      time=d$V1,mem=d$V2))
    }
    else{
    data = rbind(data,data.frame(list(N=as.numeric(N),
                                      size=as.numeric(size),
                                      GC=as.numeric(GC),
                                      time=d$V1,mem=d$V2)))
    }
}

write.table(data,"gc_interval_timings.txt",sep="\t",quote=F)
