# Thesis_Chapter_5
Thesis Chapter 5


This repository contains the code used in chapter 5 of the thesis: Understanding how mutability facilitates survival of alternating selection and botlenecks by the major food-borne pathogen Campylobacter jejuni (2023)

Chapter 5 concerns modelling the dynamics of phase variation and estimating key environmental features - as such the repository is broken into two parts: Direct modelling of phase variarble systmes and predictive modelling

Direct modelling of phase variation systems:

Input_Form.csv                   <- Input variables to run a model - covering selection, mutation and bottleneck size
Run_Model.py                     <- Code which runs the model desribed in the input file
Mutation_Selection_Model.py      <- Mutation-selection model used to apply selection and mutation coefficients over a number of generations
File_Formatter.py                <- A script to parse and format input scripts, read outputs and read input files
Figure_Generation                <- A collection of scripts to generate figures for the model (can be activated in Run_Model.py)

Predictive modelling:

Generate_Training_Data.py        <- Generates training data for model input
tensorflow_model.py              <- Creates a TensorFlow model 
TensorFlow_shap_model.py         <- Validates and checks weights of TensorFlow model
RFR_Model.py                     <- Random Forest Regression Model creation, validation and weight discovery
evolve-feedforward-parallel.py   <- NEAT machine learning algorithm implementation
config-feedforward-bottleneck    <- NEAT input config file used to generate model



