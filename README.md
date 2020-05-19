# Bee-colony-optimization

The Artificial Bee Colony (ABC) algorithm is a nature-inspired meta-heuristic method for dealing with hard, real-life combinatorial and continuous optimisation problems. It is based on the foraging habits of honeybees and was proposed by Dervis Karaboga in 2005. ABC is a simple, but effective meta-heuristic method that has already been successfully applied to various combinatorial optimization problems in transport, location analysis, scheduling and some other elds.

# Algorithm

In this mathematical model, our bee colony is composed of three types of bees: The Employee Bees, which will work on the collection of food to the hive at a specific food source. The Onlooker Bees, which will patrol the employees to verify when a specific food source is not worth it anymore, and the Scout Bees, which will be the ones looking for new food sources locations.
On the ABC algorithm a food source is defined as a position in the search space (a candidate solution for the optimization problem), and initially the number of food sources is equal to the number of bees on the hive. The quality of a food source is defined by the value of the objective function on that position (fitness value).
The emergent intelligent behavior from the bees can be summarized on some few steps:
The bees start to randomly explore the environment looking for good food sources (fitness value).
After finding a food source, the bee becomes an employee bee and begins to extract the food at the discovered source.
The employee bee returns to the hive with the nectar and unloads the nectar. After unloading the nectar, she can go back to her discovered source site directly or she can share information about her source site by performing a dance on the dance area.
If a food source is exhausted, the employee bee becomes a scout and starts to randomly search for a new food source.
Onlooker bees waiting in the hive watch the employee bees on their food source collection and choose a source among the more profitable sources.
The selection of a food source is proportional to the quality of the source (fitness value).
Even though we described three types of bees, at an implementation level we realize that there are only two types, the employees and the onlookers. The scout bee is in fact an exploratory behavior that can be performed by both employees and onlooker bees.

Artificial Bee

To begin the development of our algorithm we must find a way to represent our Bee agent on the python code. There are three main generic functionalities that any bee needs to have. The first one is when due to the exploratory behavior a bee moves out of our decision boundary it needs to have the ability to return to the hive. The second one is the ability to update the status of the actual food source in which the bee is working on and evaluate if a new neighborhood region its a better food source. And the last one realizes when a food source is exhausted and now the bee has to scout for some new food sources.

Employee Bee

The main behavior of an employee bee is to extract the food from the food source in which the employee is working on becomes exhausted. At an implementation level, this behavior can be seen as generating a new position close to where the employee bee is, and evaluating if this new position has a better amount of food. The employee bee always will memorize the best food source position achieved so far until it is exhausted.

Onlooker Bee

The onlooker bees will patrol the work of employee bees. The will fly over the hive and check the progress of their work and evaluate which employees are being more successful in gathering food.
The onlooker bees will always target the best employees, using a probabilistic approach, as a “meeting point”, where the other bees should come to this successful position with the hope to extract more food.
At an implementation level, the onlooker bees will look through the best employees and try to improve that food source. After a specific number of trials, the onlooker bee will tell to the hive that this food source is exhausted and must be discarded.
The Complete Artificial Bee Colony Algorithm
First we reset the internal parameters of ours ABC algorithm and initialize our employee bees and onlooker bees at random positions. A default strategy that is very well succeeded in real-world problems, is to initialize half of the entire hive as employee bees and the other half as onlooker bees.
After that, we begin by sending our employee bees to collect food at their respective initial food sources, always looking for better spots of food around it. Once the employee bees phase is done, we send the onlooker bees to patrol their work and evaluate how good the food extraction is going on each food source. Finally, its time to check if some food source is exhausted, at this point either employee or onlooker can become a scout bee and began an exploration process in the search for a new food source.

