.PHONY: test ci

test:
	@bats tests/breakdown/*.bats
	@bats tests/clean/*.bats
	@bats tests/headers/*.bats
	@bats tests/rebuild/*.bats

ci: test
	@bats tests/ci/ci.bats
