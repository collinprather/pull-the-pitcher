SRC = $(wildcard notebooks/*.ipynb)

all: pull_the_pitcher docs

pull_the_pitcher: $(SRC)
	nbdev_build_lib
	touch pull_the_pitcher

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist
    
# all my commands below

get_data:
	query_statcast --start_dt 2016-03-15 --end_dt 2016-11-15 --output_type db --output_path ./data/raw
	query_statcast --start_dt 2017-03-15 --end_dt 2017-11-15 --output_type db --output_path ./data/raw
	query_statcast --start_dt 2018-03-15 --end_dt 2018-11-15 --output_type db --output_path ./data/raw
	query_statcast --start_dt 2019-03-15 --end_dt 2019-11-15 --output_type db --output_path ./data/raw
    
dataset: get_data
	prep_data_for_modeling --db_path ./data/raw/statcast_pitches.db --years 2016 2017 2018 2019 --train_test_split_by year --output_path ./data/processed