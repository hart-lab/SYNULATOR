"""
This file holds the workflow for the simulation package
"""


from argparse import Namespace

from synulator.core.matrix_generator import generate_fitness_matrix
from synulator.core.table_generator import generate_fitness_table
from synulator.core.output_formatter import write_fitness_table


def run(args: Namespace) -> None:

    # 01: create fitness matrix
    fitness_matrix, gene_labels = generate_fitness_matrix(args.num_total_genes,
                                                          args.num_fitness_genes, args.mu_k_wt,
                                                          args.mu_k_fitness_min,
                                                          args.mu_k_fitness_max,
                                                          args.genetic_interaction_frequency,
                                                          args.genetic_interaction_fitness_min,
                                                          args.genetic_interaction_fitness_max,
                                                          args.wt_gi_multiplier)

    # 02: create fitness table
    fitness_table = generate_fitness_table(fitness_matrix, gene_labels, args.num_guides, 
                                           args.guide_stddev, args.sigma_k, args.time, 
                                           args.transduction_depth, args.median_read_depth,
                                           args.overdispersion_param, args.pseudocount, args.seed)

    # 03: write output to file
    write_fitness_table(fitness_table, args.output)
