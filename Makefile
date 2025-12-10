.ONESHELL:
SHELL := /bin/bash

## clean             : Remove output files
.PHONY : clean
clean :
	rm -f figures/*
	rm -rf _build
	rm -rf build
	rm -rf tools.egg-info
	pip uninstall tools -y


## env               : Create or update environment.yml
.PHONY : env
env :
	source /srv/conda/etc/profile.d/conda.sh
	conda env update -f environment.yml --prune


## html              : Build MYST instance
.PHONY : html
html :
	myst build --html


## all               : Execute notebooks
.PHONY : all
all :
	pip install .
	jupyter nbconvert --to notebook --execute --inplace *.ipynb


## help              : Show help
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
