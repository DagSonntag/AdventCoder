# AdventCoder
A repository for benchmarking different LLM models on advent of code problems


## Purpose
The purpose of this repository is to test and benchmark different LLM models in terms of their ability to code and solve 
problems of different complexity. Some common benchmarks already exists for this purpose, and the models are often tested
on these, but it is often unclear exactly what these benchmark tests are, and how they are performed (prompt input etc.).

Moreover, it is often hard to get an overview of how the different models struggle with different types of problems, and
compare them in a fair way side by side. 

Finally it is also unclear if the benchmark problems somehow have slipped into the training data of the models, giving 
them an unfair advantage over older models.

Hence, the purpose of this repository is to create a framework for testing and benchmarking different models on a set of
well known problems to coders. For this the Advent of code problems are used (https://adventofcode.com/), since many 
coders solve these problems each year and therefor have a good overview of their complexity. 

The advent of code is a (competitive) programming competition where a new two-part problem is released each day from the
1st to the 25th of December. The problems are often related to each other, and the difficulty increases as the days go by.
Each year a new set of problems are also released, so it is possible to test the models on new problems each year 
(and see if they remember old problems from their training data). Finally we can also relate how well the models can 
solve the problems to publicised data on how many humans that manage to solve them, and how long it takes them to do so.

## Scope
The scope of this framework is to:
- Provide code to download and parse the advent of code problems and solutions
- Provide code to run the different models on the problems and evaluate the found solutions
- Provide basic implementations for the most common LLMs 
- Provide an easy interface to add new models
- Provide code to compare and visualize the results of the models

What is not in scope:
- Evaluate the code in terms of how well it is written, security, or other metrics
- Evaluate how well the proposed solutions solve the problems in terms of time and memory (other than hard constraints)
- Evaluate how "close" an incorrect solution is to a correct solution. Either it is correct or it is not.

## Usage

## Framework design

## TODO:
- Build a basic LLM agent with the correct methods
- Build a framework for evaluating the agent on the downloaded problems
- Visualize the results