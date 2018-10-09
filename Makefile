SHELL := /bin/bash
PWD=$(shell pwd)
BASE.DIR=$(PWD)
APPLICATION.DIR=$(BASE.DIR)/app
CAPTURE.BIN=$(APPLICATION.DIR)/capture.py
VIRTUAL.ENV=$(BASE.DIR)/pyenv
PYTHON.BIN=$(VIRTUAL.ENV)/bin/python
SETUP.PY=$(BASE.DIR)/setup.py
ACTIVATE=$(VIRTUAL.ENV)/bin/activate
BUILD.DIR=$(BASE.DIR)/build
DEBUG.LOG=$(BASE.DIR)/debug.log

bootstrap: .FORCE
	virtualenv $(VIRTUAL.ENV)
	source $(ACTIVATE) && pip install pyserial

install: .FORCE
	source $(ACTIVATE) && python $(SETUP.PY) install 	

capture: install clean.log
	timeout 315 $(PYTHON.BIN) $(CAPTURE.BIN) | true # capture for 5 minutes plus an additional 15 seconds to allow for device setup

gdb: .FORCE
	gdb $(PYTHON.BIN) -ex "run $(CAPTURE.BIN)"

clean.log: .FORCE
	rm -f $(BASE.DIR)/debug.log

clean:. clean.log
	rm -rf $(VIRTUAL.ENV)
	rm -rf $(BUILD.DIR)
	rm -f $(BASE.DIR)/tags

.FORCE:

