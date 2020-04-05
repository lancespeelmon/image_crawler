DOCKER_IMAGE=web-crawler-whip
DOCKER_TAG=latest
HOST=127.0.0.1
LOG_LEVEL=DEBUG
TEST_PATH=./

clean-pyc:
	find . -name '*.pyc' -exec rm -rf {} \;
	find . -name '*.pyo' -exec rm -rf {} \;
	find . -name '*~'    -exec rm -rf {} \;

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean:
	rm -rf output/*

real-clean: clean clean-build clean-pyc

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

run:
	LOG_LEVEL=$(LOG_LEVEL) python3 ./fbi_crawler.py

docker-build:
	docker build --tag="$(DOCKER_IMAGE):$(DOCKER_TAG)" .

docker-run: docker-build
	docker run -it -v "${PWD}/output:/app/output" "$(DOCKER_IMAGE):$(DOCKER_TAG)"
