.PHONY: test ci

test:
	@bats tests/alter/*.bats
	@bats tests/breakdown/*.bats
	@bats tests/clean/*.bats
	@bats tests/headers/*.bats
	@bats tests/rebuild/*.bats
	@bats tests/vault/*.bats

ci: test
	@bats tests/srd/srd.bats
	@bats tests/ci/ci.bats
