.PHONY: test ci

test:
	@bats tests/alter/*.bats || true
	@bats tests/breakdown/*.bats || true
	@bats tests/clean/*.bats || true
	@bats tests/clean521/*.bats || true
	@bats tests/headers/*.bats || true
	@bats tests/rebuild/*.bats || true
	@bats tests/vault/*.bats || true

ci: test
	@bats tests/srd/srd.bats
	@bats tests/ci/ci.bats
