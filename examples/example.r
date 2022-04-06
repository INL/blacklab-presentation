
### Add repo
# Maak file /etc/apt/sources.list.d/r-base.list met deze regel:
# deb http://cran.rstudio.com/bin/linux/ubuntu trusty/

### Add key
# gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
# gpg -a --export E084DAB9 | sudo apt-key add -

### Install R
# sudo apt-get update
# sudo apt-get -y install r-base

### Install libs
# sudo apt-get install libcurl4-openssl-dev g++
# R
# > install.packages("RCurl", repos='http://cran.us.r-project.org')
# > install.packages("rjson", repos='http://cran.us.r-project.org')
# > q()
# Rscript example.r


suppressMessages(library("RCurl"))
suppressMessages(library("rjson"))

# Convert word array to string.
words <- function(context) {
    return(paste(context[['word']], collapse=" "))
}

# Search and show hits.
search <- function(cqlQuery) {
    url <- paste("http://opensonar.ato.inl.nl/blacklab-server", 
         "/zeebrieven/hits?patt=", curlEscape(cqlQuery),
         "&outputformat=json", sep="")
    lines <- suppressWarnings(readLines(url))  # suppress "Incomplete final line"
    response <- fromJSON(paste(lines, collapse=""))
    docs <- response[['docInfos']]
    hits <- response[['hits']]
    for(hit in hits) {
       # Add the document title and the hit information
       doc <- docs[[ hit[['docPid']] ]];
       cat(paste(words(hit[['left']]),
          " [", words(hit[['match']]), "] ", words(hit[['right']]),
          " (", doc[['title']], ")\n", sep="", collapse="\n"))
    }
    return()
}

invisible(search('[pos="PRN"] "schip"'))