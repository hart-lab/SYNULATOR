"""
This file takes arguments from the command line and parses them to run synulator. For
direction on usage, a quick start guide, and other useful information, please see the `README.md`.
"""


import argparse
import sys

from synulator.core.run import run
from synulator.utils.defaults import *


def __main__():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Simulate genetic interaction screen data.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output', type=str, required = True,
                        help="Output file path for the simulated fitness table")
    
    parser.add_argument('--num_total_genes', type=int, default=DEFAULT_NUM_TOTAL_GENES,
                        help="Total number of genes")
    parser.add_argument('--num_fitness_genes', type=int, default=DEFAULT_NUM_FITNESS_GENES,
                        help="Number of fitness genes")
    parser.add_argument('--mu_k_wt', type=float, default=DEFAULT_MU_K_WT,
                        help="Wildtype fitness mean")
    parser.add_argument('--mu_k_fitness_min', type=float, default=DEFAULT_MU_K_FIT_MIN,
                        help="Minimum fitness value for fitness genes")
    parser.add_argument('--mu_k_fitness_max', type=float, default=DEFAULT_MU_K_FIT_MAX,
                        help="Maximum fitness value for fitness genes")
    parser.add_argument('--genetic_interaction_frequency', type=float, 
                        default=DEFAULT_GENETIC_INTERACTION_FREQUENCY,
                        help="Frequency of genetic interactions")
    parser.add_argument('--genetic_interaction_fitness_min', type=float, default=DEFAULT_GI_FIT_MIN,
                        help="Minimum fitness value for genetic interactions")
    parser.add_argument('--genetic_interaction_fitness_max', type=float, default=DEFAULT_GI_FIT_MAX,
                        help="Maximum fitness value for genetic interactions")
    parser.add_argument('--wt_gi_multiplier', type=float, default=DEFAULT_WT_GI_MULTIPLIER,
                        help="Multiplier to reduce genetic frequency among wildtype gene pairs")
    
    parser.add_argument('--num_guides', type=int, default=DEFAULT_NUM_GUIDES,
                        help="Number of guides per gene or pair")
    parser.add_argument('--sigma_k', type=float, default=DEFAULT_SIGMA_K,
                        help="Standard deviation for observed fitness noise")
    parser.add_argument('--time', type=int, default=DEFAULT_TIME,
                        help="Number of doublings")
    parser.add_argument('--transduction_depth', type=int, default=DEFAULT_TRANSDUCTION_DEPTH,
                        help="Initial transduction depth")
    parser.add_argument('--median_read_depth', type=int, default=DEFAULT_MEDIAN_READ_DEPTH,
                        help="Median read depth for normalization")
    parser.add_argument('--overdispersion_param', type=float, default=DEFAULT_OVERDISPERSION_PARM,
                        help="Overdispersion parameter for sequencing noise; must be 0 ~ 1")
    parser.add_argument('--pseudocount', type=int, default=DEFAULT_PSEUDOCOUNT,
                        help="Pseudocount added to avoid zeroes")
    parser.add_argument('--seed', type=int, default=DEFAULT_SEED,
                        help="Seed value for random number generation")
    
    arguments = parser.parse_args()
    run(arguments)


if __name__ == '__main__':
    sys.exit(__main__())
