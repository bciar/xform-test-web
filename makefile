SHELL=/bin/bash

# TODO: Some of these are no longer needed.
.PHONY: build lint linttest lintall pylint pylinttest pylintall code codetest \
codeall doc doctest docall test testdoc serve serve-local \
push-production-s3 serve-production push-staging-s3 serve-staging \
production staging serve-dev serve-dev-network-accessible \
production-connect-s3 staging-connect-s3 logs logs-staging production \
staging production-push staging-push push-production push-staging \
circleci-validate-config  gunicorn-local serve-local production-push-ci \
stagingpush-ci logs-s3 logs-staging-s3 validations validate \
connect-staging connect-prod connect connect-vim connect-vim-staging \
s3-setup

# DEVELOPMENT
## Linting
SRC=./
TEST=./test/
### All linting
lint:
	${LINT_SRC}; ${CODE_SRC}; ${DOC_SRC}
	# If you want to run this command directly, use the following:
	# python -m pylint --output-format=colorized --reports=n xform-test_web
	# test; \
	# python -m pycodestyle xform_test_web test; \
	# python -m pydocstyle xform_test_web test
linttest:
	${LINT_TEST}; ${CODE_TEST}; ${DOC_TEST}
lintall: lint linttest
### Pylint only
PYLINT=python -m pylint \
	--output-format=colorized \
	--reports=n
LINT_SRC=${PYLINT} ${SRC}
LINT_TEST=${PYLINT} ${TEST}
pylint:
	${LINT_SRC}
pylinttest:
	${LINT_TEST}
pylintall: pylint pylinttest
### Pycodestyle only
PYCODESTYLE=python -m pycodestyle
CODE_SRC=${PYCODESTYLE} ${SRC}
CODE_TEST=${PYCODESTYLE} ${TEST}
code:
	${CODE_SRC}
codetest:
	${CODE_TEST}
codeall: code codetest
### Pydocstyle only
PYDOCSTYLE=python -m pydocstyle
DOC_SRC=${PYDOCSTYLE} ${SRC}
DOC_TEST=${PYDOCSTYLE} ${TEST}
doc:
	${DOC_SRC}
doctest:
	${DOC_TEST}
docall: doc doctest

## Testing
# TODO
#test:
#	python -m unittest discover -v
#testdoc:
#	python -m test.test --doctests-only
test-unit:
	npm run test:unit
test-selenium:
	npm run test:selenium
test-staging:
	node ./test/index.js url=http://xform-test-staging.pma2020.org
test-production:
	node ./test/index.js url=http://xform-test.pma2020.org
test-prod: test-production
test: test-unit test-selenium

## Validations
circleci-validate-config:
	echo Make sure that Docker is running, or this command will fail.; \
	circleci config validate

# SERVERS & ENVIRONMENTS
## Local
serve:
	npm start

## Build
build:
	npm run build
# TODO
set-env:
	sed 's/const env = envSrc\..*;/const env = envSrc\.${CONFIG_KEY};/g' \
	  env.js > temp.js;
	mv temp.js env.js
set-default-development-env:
	make set-env CONFIG_KEY=developmentWithProductionApi
set-default-staging-env:
	make set-env CONFIG_KEY=stagingWithProductionApi
set-full-development-env:
	make set-env CONFIG_KEY=developmentAll
set-full-staging-env:
	make set-env CONFIG_KEY=stagingAll
set-full-production-env:
	make set-env CONFIG_KEY=productionAll

## Deploy
### AWS S3
push-staging-s3:
#	make set-default-staging-env
#	cp env.js build/env.js
#	open http://xform-test-staging.pma2020.org
	make build; \
	aws s3 sync build/ s3://xform-test-staging.pma2020.org \
	  --region us-west-2 --profile work; \
	open http://xform-test-staging.pma2020.org.s3-website-us-west-2.amazonaws.\
	com/

push-production-s3:
#	make set-full-production-env
#	cp env.js build/env.js
#	open http://xform-test.pma2020.org
	make build; \
	aws s3 sync build/ s3://xform-test.pma2020.org \
	  --region us-west-2 --profile work; \
  	open http://xform-test.pma2020.org.s3-website-us-west-2.amazonaws.com/


## Aliases and defaults
production-push-s3: push-production-s3
staging-push-s3: push-staging-s3
production: push-production-s3
staging: push-staging-s3
production-push: production-push-ci
staging-push: staging-push-ci
push-production: production-push
push-staging: staging-push
production-push-ci: production-push-s3
staging-push-ci: staging-push-s3
serve-local: serve
validations: circleci-validate-config
validate: validations


## Heroku
### Setup
#heroku-setup-staging:
#	heroku buildpacks:add --index 1 heroku/jvm --app xform-test-staging; \
#	heroku buildpacks:add --index 2 heroku/python --app xform-test-staging
#heroku-setup-production:
#	heroku buildpacks:add --index 1 heroku/jvm --app xform-test; \
#	heroku buildpacks:add --index 2 heroku/python --app xform-test
#heroku-setup:
#	make heroku-setup-staging; \
#	make heroku-setup-production

### Pushing & Serving
#push-production-heroku:
#	git status; \
#	printf "\nGit status should have reported 'nothing to commit, working tree\
#	 clean'. Otherwise you should cancel this command, make sure changes are\
#	  committed, and run it again.\n\n"; \
#	git checkout master; \
#	git branch -D production; \
#	git checkout -b production; \
#	git push -u trunk production --force; \
#	git checkout master; \
#	open https://dashboard.heroku.com/apps/xform-test/activity; \
#	open https://circleci.com/gh/PMA-2020/workflows/xform-test-web
#push-staging-heroku:
#	git status; \
#	printf "\nGit status should have reported 'nothing to commit, working tree\
#	 clean'. Otherwise you should cancel this command, make sure changes are\
#	  committed, and run it again.\n\n"; \
#	git checkout develop; \
#	git branch -D staging; \
#	git checkout -b staging; \
#	git push -u trunk staging --force; \
#	git checkout develop; \
#	open https://dashboard.heroku.com/apps/xform-test-staging/activity; \
#	open https://circleci.com/gh/PMA-2020/workflows/xform-test-web

### SSH
#production-connect-heroku:
#	heroku run bash --app xform-test
#staging-connect-heroku:
#	heroku run bash --app xform-test-staging
#	production-connect: production-connect-heroku
#install-vim-on-server:
#	mkdir ~/vim; \
#	cd ~/vim; \
#	curl 'https://s3.amazonaws.com/bengoa/vim-static.tar.gz' | tar -xz; \
#	export VIMRUNTIME="$HOME/vim/runtime"; \
#	export PATH="$HOME/vim:$PATH"; \
#	cd -

### Logs
#logs-heroku:
#	heroku logs --app xform-test --tail
#logs-staging-heroku:
#	heroku logs --app xform-test-staging --tail

### Serve
#serve-production:
#	${GUNICORN}
#serve-staging: serve-production

#serve-heroku-local:
#	heroku local
#serve-dev-network-accessible:
#	${GUNICORN} \
#	--access-logfile logs/access-logfile.log \
#	--error-logfile logs/error-logfile.log \
#	--capture-output \
#	--pythonpath python
#gunicorn-local: serve-dev-network-accessible

## Aliases and defaults - Heroku
#gunicorn: serve-production
#production-push-heroku: push-production-heroku
#staging-push-heroku: push-staging-heroku
#production-push-ci: production-push-heroku
#staging-push-ci: staging-push-heroku
#staging-connect: staging-connect-heroku
#connect-staging: staging-connect-heroku
#connect-prod: production-connect-heroku
#connect: production-connect-heroku
#logs: logs-heroku
#logs-staging: logs-staging-heroku
