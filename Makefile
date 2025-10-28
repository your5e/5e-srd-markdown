.PHONY: flake8 test ci vaults vault-dnd51 vault-dnd51-zip vault-dnd521 vault-dnd521-zip assets push pull

flake8:
	flake8 *.py lib/*py
	flake8 --ignore=E501 tests/

test: flake8
	@./test.sh

ci: test
	@bats tests/srd/srd.bats
	@bats tests/ci/ci.bats

vaults: vault-dnd51 vault-dnd521

assets: vault-dnd51-zip vault-dnd521-zip

vault-dnd51:
	./patches.sh dnd/51/markdown apply
	python update_vault.py --profile dnd51 dnd/51/markdown dnd/51/obsidian_vault
	./update_vault_indexes.sh dnd/51
	./patches.sh dnd/51/obsidian_vault apply

vault-dnd51-zip: vault-dnd51
	rsync -av dnd/51/obsidian_vault/ /tmp/dnd_51_srd/
	(cd /tmp && zip -r dnd_51_srd.zip dnd_51_srd/)

vault-dnd521:
	./patches.sh dnd/521/markdown apply
	python update_vault.py --profile dnd521 dnd/521/markdown dnd/521/obsidian_vault
	./update_vault_indexes.sh dnd/521
	./patches.sh dnd/521/obsidian_vault apply

vault-dnd521-zip: vault-dnd521
	rsync -av dnd/521/obsidian_vault/ /tmp/dnd_521_srd/
	(cd /tmp && zip -r dnd_521_srd.zip dnd_521_srd/)

push:
	rsync -ai --delete dnd/51/obsidian_vault/ ~/Downloads/dnd_51_srd/
	rsync -ai --delete dnd/521/obsidian_vault/ ~/Downloads/dnd_521_srd/

pull:
	rsync -ai --delete ~/Downloads/dnd_51_srd/ dnd/51/obsidian_vault/
	rsync -ai --delete ~/Downloads/dnd_521_srd/ dnd/521/obsidian_vault/
