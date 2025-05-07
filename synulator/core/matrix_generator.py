"""
This file generates a NxN matrix of fitness values to be used by the simultation package
"""


import sys
from typing import Dict, List, Tuple

import pandas as pd
import numpy as np


def generate_fitness_matrix(num_total_genes: int, num_fitness_genes: int, mu_k_wt: float,
                            mu_k_fitness_min: float, mu_k_fitness_max: float,
                            genetic_interaction_frequency: float,
                            genetic_interaction_fitness_min: float,
                            genetic_interaction_fitness_max: float,
                            wt_gi_multiplier: float) -> Tuple[pd.DataFrame, Dict[str, List[int]]]:
    """
    Generate an NxN matrix of target knockout fitness values.
    A[i,i] = single gene fitness, where 1.0 = wildtype and 0.0 = total loss of proliferation
    A[i,j] = genetic interaction fitness, where 1.0 = no interaction and 0.0 = synthetic lethal.
    In the master fitness equation Xc = Xo*2^(kt), where k~N(mu,sigma), the mu term is generated
    from these fitness values
        
    Parameters:
        num_total_genes : int
            Total number of genes in the system
        num_fitness_genes : int
            Number of genes that have a fitness phenotype when knocked out
        mu_k_wt : float
            Fitness value assigned to wildtype gene knockouts (typically 1.0)
        mu_k_fitness_min : float
            Minimum fitness value for fitness gene knockouts
        mu_k_fitness_max : float
            Maximum fitness value for fitness gene knockouts
        genetic_interaction_frequency : float
            Probability that a gene pair has a genetic interaction
        genetic_interaction_fitness_min : float
            Minimum fitness value for genetic interactions
        genetic_interaction_fitness_max : float
            Maximum fitness value for genetic interactions
        wt_gi_multiplier : float
            Scaling factor to adjust genetic interaction frequency for wildtype genes

    Returns:
        Tuple[pd.DataFrame, Dict[str, List[int]]]
            - A DataFrame (N x N) containing the fitness matrix to be used in the further analysis
            - A dictionary with two lists: 'wildtype' and 'fitness' gene indices
    """

    # initialize matrix: all ones
    fitness_matrix = pd.DataFrame(index=np.arange(num_total_genes),
                                  columns=np.arange(num_total_genes),
                                  data=np.ones([num_total_genes,num_total_genes]))
    num_wt_genes = num_total_genes - num_fitness_genes
    if (num_fitness_genes > num_total_genes):
        sys.exit('Number of fitness genes exceeds number of total genes\n')

    # Initialize gene label
    wt_genes = list(range(num_wt_genes))
    fitness_genes = list(range(num_wt_genes, num_total_genes))

    # single gene phenotypes: mu_k. – wildtype genes (no fitness phenotype)
    for i in np.arange(num_wt_genes):
        fitness_matrix.loc[i,i] = mu_k_wt


    # fitness genes (some ko fitness phenotype) – mu_k is uniformly distributed on 
    # (mu_k_fitness_min, mu_k_fitness_max)
    for i in np.arange(num_wt_genes,num_total_genes):
        fitness_matrix.loc[i,i] = np.random.uniform(low=mu_k_fitness_min, high=mu_k_fitness_max)   

    # off diagonal: genetic interaction. 
    for i in range(num_total_genes-1):
        fit_i = fitness_matrix.loc[i,i]
        for j in range(i+1,num_total_genes):
            fit_j = fitness_matrix.loc[j,j]
            if ( (fit_i ==1) & (fit_j ==1 ) ):
                # among "wildtype" genes, reduce 
                genetic_interaction_frequency_threshold = (genetic_interaction_frequency
                                                           * wt_gi_multiplier)
            else:
                genetic_interaction_frequency_threshold = genetic_interaction_frequency
            if (np.random.rand() <= genetic_interaction_frequency_threshold):
                fitness_matrix.loc[i,j] = np.random.uniform(low=genetic_interaction_fitness_min,
                                                            high=genetic_interaction_fitness_max)

    # Return fitness matrix and gene labels
    gene_labels = {
        'wildtype': wt_genes,
        'fitness': fitness_genes
    }

    return fitness_matrix, gene_labels
