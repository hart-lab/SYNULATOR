# SYNULATOR
Synulator (Simulation for Synthetic Lethality) is a tool for simulating genetic interaction screen data, modeling fitness effects, and predicting synergistic genetic interactions.

### Dependencies
To run this software, `Python>=3.10.1` is required. 

Software dependencies:
- `numpy==2.0.2`
- `pandas==2.2.3`
- `scipy==1.13.1`

## Installation

1. Clone the repository into a directory on your computer and `cd` into the root directory of the `SYNULATOR` package.

```zsh
git clone https://github.com/hart-lab/SYNULATOR.git
cd SYNULATOR
```

2. Optional but recommended, create and start a virtual environment for the tool with:

```zsh
python3 -m venv syenv
source syenv/bin/activate
```

To exit the environment later, run `deactivate` in the command line. 

3. Install using the `setup.py` file with:

```zsh
pip3 install .
```

4. Verify installation:

```zsh
synulator -h
```
You should see the following:
```zsh
usage: synulator [-h] -o OUTPUT [--num_total_genes NUM_TOTAL_GENES] [--num_fitness_genes NUM_FITNESS_GENES] [--mu_k_wt MU_K_WT] [--mu_k_fitness_min MU_K_FITNESS_MIN] [--mu_k_fitness_max MU_K_FITNESS_MAX] [--genetic_interaction_frequency GENETIC_INTERACTION_FREQUENCY] [--genetic_interaction_fitness_min GENETIC_INTERACTION_FITNESS_MIN] --genetic_interaction_fitness_max GENETIC_INTERACTION_FITNESS_MAX] [--wt_gi_multiplier WT_GI_MULTIPLIER] [--num_guides NUM_GUIDES] [--sigma_k SIGMA_K] [--time TIME] [--transduction_depth TRANSDUCTION_DEPTH] [--median_read_depth MEDIAN_READ_DEPTH] [--overdispersion_param OVERDISPERSION_PARAM] [--pseudocount PSEUDOCOUNT] [--seed SEED]

Simulate genetic interaction screen data.
```

## Quick Usage Example
```zsh
synulator -o ./test.txt --num_total_genes 300 --num_fitness_genes 50 --time 6
```

### Required Arguments
| Argument       | Description                             |
| -------------- | --------------------------------------- |
| `-o, --output` | Output file path for simulation results |

### Optional Arguments
| Argument                            | Description                                                          | Default  |
| ----------------------------------- | -------------------------------------------------------------------- | -------- |
| `--num_total_genes`                 | Total number of genes in the simulated library                       | `200`    |
| `--num_fitness_genes`               | Number of fitness genes (non-wildtype)                               | `50`     |
| `--mu_k_wt`                         | Mean fitness of wildtype genes                                       | `1.0`    |
| `--mu_k_fitness_min`                | Minimum fitness for a fitness gene                                   | `0.2`    |
| `--mu_k_fitness_max`                | Maximum fitness for a fitness gene                                   | `1.0`    |
| `--genetic_interaction_frequency`   | Probability of a genetic interaction occurring                       | `0.01`   |
| `--genetic_interaction_fitness_min` | Minimum fitness for genetic interaction                              | `0.2`    |
| `--genetic_interaction_fitness_max` | Maximum fitness for genetic interaction                              | `1.0`    |
| `--wt_gi_multiplier`                | Multiplier to reduce genetic interaction frequency in wildtype genes | `0.1`    |
| `--num_guides`                      | Number of guides targeting each gene                                 | `4`      |
| `--sigma_k`                         | Standard deviation of fitness means                                  | `0.03`   |
| `--time`                            | Number of cell doublings (time steps)                                | `8`      |
| `--transduction_depth`              | Initial cell transduction depth                                      | `500`    |
| `--median_read_depth`               | Median sequencing read depth                                         | `500`    |
| `--overdispersion_param`            | Overdispersion parameter (must be 0-1)                               | `0.5`    |
| `--pseudocount`                     | Pseudocount added to avoid division by zero                          | `1`      |
| `--seed`                            | Seed value for reproducibility                                       | `None`   |
