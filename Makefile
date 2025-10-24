.PHONY: flake8 test ci vaults vault51 vault51-zip vault521 vault521-zip assets

flake8:
	flake8 *.py lib/*py
	flake8 --ignore=E501 tests/

test: flake8
	@./test.sh

ci: test
	@bats tests/srd/srd.bats
	@bats tests/ci/ci.bats

vaults: vault51 vault521

assets: vault51-zip vault521-zip

vault51:
	python update_vault.py --profile dnd51 dnd/51/markdown dnd/51/obsidian_vault
	./update_vault_indexes.sh dnd/51

vault51-zip: vault51
	rsync -av dnd/51/obsidian_vault/ /tmp/dnd_51_srd/
	(cd /tmp && zip -r dnd_51_srd.zip dnd_51_srd/)

vault521:
	python update_vault.py --profile dnd521 dnd/521/markdown dnd/521/obsidian_vault
	./update_vault_indexes.sh dnd/521

vault521-zip: vault521
	rsync -av dnd/521/obsidian_vault/ /tmp/dnd_521_srd/
	(cd /tmp && zip -r dnd_521_srd.zip dnd_521_srd/)
