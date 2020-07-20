#!/bin/bash

# to be run from root directory with `$ sh scripts/get_data.sh`

# can be finnicky if you give it multiple years, here I just do one at a time
query_statcast --start_dt 2016-03-15 --end_dt 2016-11-15 --output_type db --output_path ./data/raw
query_statcast --start_dt 2017-03-15 --end_dt 2017-11-15 --output_type db --output_path ./data/raw
query_statcast --start_dt 2018-03-15 --end_dt 2018-11-15 --output_type db --output_path ./data/raw
query_statcast --start_dt 2019-03-15 --end_dt 2019-11-15 --output_type db --output_path ./data/raw

