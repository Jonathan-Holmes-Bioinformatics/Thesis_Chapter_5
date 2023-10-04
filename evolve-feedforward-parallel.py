# -----------------------------------------------------------------------------------------------
# 
#
#
# Jonathan Holmes
#
# Permission to use, copy, modify, and/or distribute this software or any part thereof for any
# purpose with or without fee is hereby granted provided that:
#     (1) the original author is credited appropriately in the source code
#         and any accompanying documentation
# and (2) that this requirement is included in any redistribution.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
#
# E-mail: jh795@leicester.ac.uk
# ------------------------------------------------------------------------------------------------
# 
#
#  		A NEAT - neural network 
#		 Input variables subject to change
# 
#
# ------------------------------------------------------------------------------------------------




"""
A parallel version of XOR using neat.parallel.

Since XOR is a simple experiment, a parallel version probably won't run any
faster than the single-process version, due to the overhead of
inter-process communication.

If your evaluation function is what's taking up most of your processing time
(and you should check by using a profiler while running single-process),
you should see a significant performance improvement by evaluating in parallel.

This example is only intended to show how to do a parallel experiment
in neat-python.  You can of course roll your own parallelism mechanism
or inherit from ParallelEvaluator if you need to do something more complicated.
"""

# Import libraries - neat and visualize must be downloaded and implemented from NEAT website
import multiprocessing
import os
import math
import neat
import visualize


def to_float(A):
	B = []
	for i in A:
		B.append(float(i))
	return B


# define input and output vdata sets
xor_inputs = []
xor_outputs = []
xor_inputs_test = []
xor_outputs_test = []
data = open("1m_training_data_4genes.csv").read().split("\n")[1:250000]

# Place data in input and output test and train (70% on train)
for line in range(0,len(data)):
	v = data[line].split("\t")

	#if 0.9 <= float(v[3]):
	if line < len(data)*0.70:
		xor_inputs.append(to_float(v[1:-4]))
		xor_outputs.append([v[0]] + v[-4:])	
	else:
		xor_inputs_test.append(to_float(v[1:-4]))
		xor_outputs_test.append([v[0]] + v[-4:])


# Evalute genome effecitiveness 
def eval_genome(genome, config):
	"""
	This function will be run in parallel by ParallelEvaluator.  It takes two
	arguments (a single genome and the genome class configuration data) and
	should return one float (that genome's fitness).

	Note that this function needs to be in module scope for multiprocessing.Pool
	which is what ParallelEvaluator uses) to find it.  Because of this, make
	sure you check for __main__ before executing any code (as we do here in the
	last few lines in the file), otherwise you'll have made a fork bomb
	instead of a neuroevolution demo. :)
	"""
	possible_picks = [1,2,4,8,16,32,64,128]
	numerical = [1,2,3,4,5,12,32,128]

	net = neat.nn.FeedForwardNetwork.create(genome, config)
	error = 1000
	for xi, xo in zip(xor_inputs, xor_outputs):

		output = net.activate(xi)
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))


		score_true = numerical[possible_picks.index(takeClosest(int(xo[0]),possible_picks))]
		score_pred = numerical[possible_picks.index(takeClosest(output[0],possible_picks))]
		error -= max([score_true,score_pred]) - min([score_true,score_pred])


		for i in range(1,len(output)):

	
			if float(xo[i]) < 1 and 1 <= output[i]:
				error -= (math.sqrt((float(output[i]) - float(xo[i])) ** 2))
				error -= 2
			elif 1 < float(xo[i]) and output[i] <= 1:
				error -= (math.sqrt((float(output[i]) - float(xo[i])) ** 2))
				error -= 2
			else:
				error -= (math.sqrt((float(output[i]) - float(xo[i])) ** 2))


		#error += math.sqrt((output[0] - xo[0]) ** 2)/(len(xor_inputs))

	return error

# Run main code - number of generations is 50 (winner = p.run(pe.evaluate, 50)) checkpoints every 9 generations ( p.add_reporter(neat.Checkpointer(9)))
def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    #p = neat.Checkpointer.restore_checkpoint('half_matrix_run')
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(9))
    # Run for up to 300 generations.
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate, 50)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(xor_inputs_test, xor_outputs_test):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    #visualize.draw_net(config, winner, True, node_names=node_names)
    #visualize.draw_net(config, winner, True, node_names=node_names, prune_unused=True)
    visualize.draw_net(config, winner, True)
    visualize.draw_net(config, winner, True, prune_unused=True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

## Run main code from 'config-feedforward-bottleneck' file
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward-bottleneck')
    run(config_path)

# Reload and rerun from a checkpoint
"""
p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-46')
local_dir = os.path.dirname(__file__)
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,os.path.join(local_dir, 'config-feedforward-bottleneck'))
winner_net = neat.nn.FeedForwardNetwork.create(p.run(eval_genomes, 1), config)
for xi in zip(X):
	output = winner_net.activate(xi)
	print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))
"""







