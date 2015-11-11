
REPO := $(shell cd ../..; pwd)

all: build

build:
	JUJU_REPOSITORY=$(REPO) charm build -l debug

files-clean:

charm-clean:

cache-clean:

clean:
	$(RM) -r $(REPO)/trusty/nginx

.PHONY: all build clean files-clean charm-clean cache-clean

