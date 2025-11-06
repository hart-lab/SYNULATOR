"""
This file generates a guide-level fitness table using the fitness matrix from matrix_generator.py
"""


from typing import Dict, List, Optional

import pandas as pd
import numpy as np

import scipy.stats as stats


def generate_fitness_table(fitness_matrix: pd.DataFrame, gene_labels: Dict[str, List[int]],
                           num_guides: int, sigma_k: float, time: int,
                           transduction_depth: int, median_read_depth: int, 
                           overdispersion_param: float, pseudocount: int,
                           seed: Optional[int]) -> pd.DataFrame:
    """
    Generate a guide-level fitness table based on a given fitness matrix.

    Parameters:
        fitness_matrix : pd.DataFrame
            NxN matrix of fitness values from `generate_fitness_matrix()`
        gene_labels : Dict[str, List[int]]
            Dictionary categorizing genes as 'wildtype' or 'fitness' 
            (output from `generate_fitness_matrix()`)
        num_guides : int
            Number of gRNAs per target gene or gene pair.
        sigma_k : float
            Standard deviation for noise in fitness measurements
        time : int
            Cell doubling time duration affecting `Xt` calculation
        transduction_depth : int
            Initial number of cells (`X0`)
        median_read_depth : int
            Median sequencing read depth used for scaling `Xt`
        overdispersion_param : float
            Overdispersion parameter (between 0 and 1) for negative binomial modeling of sequencing 
            noise
        pseudocount : int
            Pseudocount added to sequencing read counts (`Reads_t`) to prevent zero values
        seed : Optional[int]
            Random seed for reproducibility

    Returns:
        pd.DataFrame
        A guide-level fitness table with the following columns:
        - `guide_id`: Unique identifier for each guide
        - `target_id`: Target gene(s) for the guide
        - `mu_k`: Mean fitness value of the guide
        - `GI`: Genetic interaction term (1.0 = no interaction, 0.0 = synthetic lethal)
        - `label`: Gene type ('wildtype' or 'fitness')
        - `X0`: Initial cell count
        - `k_obs`: Observed fitness coefficient (sampled from `mu_k` with noise)
        - `Xt`: Final observed cell count
        - `Reads_t`: Simulated sequencing read counts with noise
        - `Log2fc`: Log2 fold-change of reads relative to initial transduction
    """

    if seed is not None:
       np.random.seed(seed)

    genelist = fitness_matrix.index.values
    num_genes_in_genelist = len(genelist)
    guide_level_data = []

    # Set the largest possible guide stddev consistent with sigma_k total variance
    guide_stddev = np.sqrt(num_guides) * sigma_k
    print(f"[INFO] Guide-level stddev automatically set to {guide_stddev:.4f}")

    # populate the guide-level fitness table
    for i in range(num_genes_in_genelist):
        gene1 = str(genelist[i])
        gene1_label = 'wildtype' if i in gene_labels['wildtype'] else 'fitness'
        for j in range(i, num_genes_in_genelist):
            gene2 = str(genelist[j])
            gene2_label = 'wildtype' if j in gene_labels['wildtype'] else 'fitness'
            if (i==j):
                # on the diagonal of the fitness matrix, we are dealing with single knockout fitness
                mu_k = fitness_matrix.loc[i,i]
                target = gene1
                gi = 1.
                guide_label = gene1_label
            else:
                # off the diagonal, we are dealing with double knockout fitness. 
                # Under the multiplicatiave model, this is ki * kj. 
                # With interactions, this is ki * kj * GI(i,j)
                mu_k = fitness_matrix.loc[i,i] * fitness_matrix.loc[j,j] * fitness_matrix.loc[i,j]
                target = f'{gene1}_{gene2}'
                gi = fitness_matrix.loc[i,j]
                guide_label = f'{gene1_label}_{gene2_label}'
            
            # gene-level latent mean to correct for increased variance from guides
            sigma_latent_sq = sigma_k**2 - (guide_stddev**2 / num_guides)
            mu_gene_latent = np.random.normal(loc=mu_k, scale=np.sqrt(sigma_latent_sq))

            # generate guide-level data for each target
            for guide_num in range(1, num_guides + 1):
                guide_id = f'{target}_guide{guide_num}'
                mu_k_guide = np.random.normal(loc=mu_gene_latent, scale=guide_stddev)
                guide_level_data.append({
                    'guide_id': guide_id,
                    'target_id': target,
                    'mu_k': mu_k_guide,
                    'GI': gi,
                    'label': guide_label
                })

    # Convert the list of dictionaries to a DataFrame
    fitness_table = pd.DataFrame(guide_level_data)
    fitness_table = fitness_table.astype({'mu_k': float, 'GI': float})

    # set X0 counts for each target. Placeholder for future roadmap where this value might vary
    fitness_table['X0'] = transduction_depth + pseudocount

    # we have mu_k for each target, and sigma_k as a noise term. 
    # Calculate Xt = X0 * 2^(kt), where k~N(mu_k, sigma_k)
    fitness_table['k_obs'] = np.random.normal(loc=fitness_table['mu_k'].values, scale=sigma_k)
    fitness_table['Xt'] = fitness_table.X0 * 2 ** (fitness_table.k_obs * time)
    
    # scale observed cell counts, Xt, to median library coverage/sequecing read depth
    reads_t = np.floor(fitness_table.Xt.values * median_read_depth / fitness_table.Xt.median())

    # add sequencing noise from negative binomial model with overdispersion paramenter p
    p = overdispersion_param
    n = reads_t * p / (1-p)
    if np.any(n <= 0):
        raise ValueError("Invalid 'n' values calculated for the negative binomial distribution.")

    # calculate "observed" reads and add pseudocount, if present. 
    fitness_table['Reads_t'] = stats.nbinom.rvs(n=n, p=p) + pseudocount

    # calculate fold change from observed reads_t and initial reads X0.
    # note that absence of a pseudocount can lead to zeros at reads_t and nans for log(fc)
    fitness_table['Log2fc'] = np.log2((fitness_table.Reads_t.values
                                        / sum(fitness_table.Reads_t.values)) 
                                       / (fitness_table.X0.values / sum(fitness_table.X0.values)))
    
    fitness_table = fitness_table.astype({'Reads_t': int}, copy=False, errors='raise')
    fitness_table.set_index('guide_id', inplace=True)

    gene_means = fitness_table.groupby('target_id')['mu_k'].mean()
    print("Empirical variance of averaged guides:", np.var(gene_means))

    return fitness_table
