.PHONY: flake8 test ci

flake8:
	flake8 *.py lib/*py
	flake8 --ignore=E501 tests/

test: flake8
	@./test.sh

ci: test
	@bats tests/srd/srd.bats
	@bats tests/ci/ci.bats
