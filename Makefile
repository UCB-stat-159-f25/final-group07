## clean             : Remove output files
.PHONY : clean
clean : 
	rm -f audio/*
	rm -f figures/*
	rm -rf _build


.ONESHELL:
SHELL = /bin/bash


## env             : Create or update environment.yml
env :
	source /srv/conda/etc/profile.d/conda.sh
	conda env update -f environment.yml --prune


## html             : Build MYST instance
html : 
	myst build --html


## all
all :
	jupyter nbconvert --to notebook --execute *.ipynb

.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
