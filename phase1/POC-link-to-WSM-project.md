# PHASE 1 - LINK TO WSM PROJECT

The WSM program contains a bunch of R code, and when run, it takes more than 5 minutes to complete each run.

This process is repeated N number of times (currently 10 times, but possibly more in the future).

The individual results are then aggregated.

## Phase 1 Overview

Phase 1 of this project involves running the following 3 Python scripts:

1. **Python Script 1 (generate_batch_number.py):** This script generates unique batch numbers and name-value pairs.

2. **Python Script 2 (mean_rand_numbers.py):** This script generates random numbers and introduces a 600-second delay using the `time.sleep` attribute. It saves the generated numbers as CSV files and uploads them to an S3 bucket.

3. **Python Script 3 (collect_file_from_s3_bucket.py):** This script collects the generated CSV files from the S3 bucket, extracts the numbers, and calculates their average.

This phase mimics the individual runs and runtime of the WSM code.

These Python scripts are executed using workflows orchestrated by AWS Step Functions. Each iteration of Python Script 2 is run in parallel.