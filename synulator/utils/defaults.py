"""
This file contains definitions to run the tool
"""

from typing import Optional


DEFAULT_NUM_TOTAL_GENES: int = 200
"""total number of single genes in the simulated library"""

DEFAULT_NUM_FITNESS_GENES: int = 50
"""number of fitness genes; num_total_genes - num_fitness_genes = wildtype genes"""

DEFAULT_MU_K_WT: float = 1.0
"""wildtype gene fitness mean"""

DEFAULT_MU_K_FIT_MIN: float = 0.2
"""fitness mean is a uniform distribution between min and max, this parameter specify the min"""

DEFAULT_MU_K_FIT_MAX: float = 1.0
"""fitness mean is a uniform distribution between min and max, this parameter specify the max"""

DEFAULT_GENETIC_INTERACTION_FREQUENCY: float = 0.01
"""genetic interaction frequency"""

DEFAULT_GI_FIT_MIN: float = 0.2
"""genetic interaction fitness is a uniform distribution, this parameter specify the min"""

DEFAULT_GI_FIT_MAX: float = 1.0
"""genetic interaction fitness is a uniform distribution, this parameter specify the max"""

DEFAULT_WT_GI_MULTIPLIER: float = 0.1
"""multiplier to reduce genetic interaction frequency threshold among WT gene pairs"""

DEFAULT_NUM_GUIDES: int = 4
"""number of guides targeting a gene or gene pair"""

DEFAULT_GUIDE_STDDEV: float = 0.0755
"""guide-level stddev of guides targeting a nonessential gene, estimated from DepMap"""

DEFAULT_SIGMA_K: float = 0.03
"""stddev for mu_k"""

DEFAULT_TIME: int = 8
"""Number of cell doublings"""

DEFAULT_TRANSDUCTION_DEPTH: int = 500
"""initial cell transduction depth"""

DEFAULT_MEDIAN_READ_DEPTH: int = 500
"""median library coverage/sequecing read depth for Xt (observed cell count) normalization"""

DEFAULT_OVERDISPERSION_PARM: float = 0.5
"""overdispersion parameter for sequencing and experimental noise, must be 0 ~ 1"""

DEFAULT_PSEUDOCOUNT: int = 1
"""pseudocount added to avoid zeroes when calculating fold change"""

DEFAULT_SEED: Optional[int] = None
"""seed value for random number generation"""
