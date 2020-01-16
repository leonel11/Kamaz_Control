# Kamaz_Control

## Description

Kamaz Control Challenge

## Required software

* [Git](https://git-scm.com/downloads)
* [Anaconda](https://www.anaconda.com/download/)
* Matlab R2017b
* [Microsoft Visual C++ 2015 compiler](https://www.visualstudio.com/ru/downloads/)

## Installation

1. Clone this repository using Git
2. Install pandas:
	```
	conda install pandas
	```
3. Download train and test data and unpack them to folder `data`
4. Clone ECO repository 
	```
	https://github.com/martin-danelljan/ECO
	``` 
	and follow the instructions about its installations. Also see Advices below for solving some problems in the process of installation ECO repository
5. Clone R-FCN repository
	```
	https://github.com/daijifeng001/R-FCN
	```

## Advices

1. For the installation of ECO repository:
	*	Before implemeting `install` in Matlab, perform 
		```
		mex -setup
		```
		It's necessary for compiling C++ code. In the process of performing this command, choose `Microsoft Visual C++ 2015` compiler, because `install` works only with this version of compiler.
	*	In case of cancel of downloading `image-vgg-m-2048.mat`, download [this model](http://www.vlfeat.org/matconvnet/models/) and copy it to the folder of ECO repository `./feature_extraction/networks`
