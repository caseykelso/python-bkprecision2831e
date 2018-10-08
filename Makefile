SHELL := /bin/bash
PWD=$(shell pwd)
BASE.DIR=$(PWD)
TEST.DIR=$(BASE.DIR)/tests
TEST.BIN=$(TEST.DIR)/tests.py
TEST.ENV=$(BASE.DIR)/pyenv
PYTHON.BIN=$(TEST.ENV)/bin/python
SETUP.PY=$(BASE.DIR)/setup.py
ACTIVATE=$(TEST.ENV)/bin/activate
BUILD.DIR=$(BASE.DIR)/build
DEBUG.LOG=$(BASE.DIR)/debug.log

bootstrap: .FORCE
	virtualenv $(TEST.ENV)
	source $(ACTIVATE) && pip install pyserial

install: .FORCE
	source $(ACTIVATE) && python $(SETUP.PY) install 	

test: install clean.log
	$(PYTHON.BIN) $(TEST.BIN)

gdb: .FORCE
	gdb $(PYTHON.BIN) -ex "run $(TEST.BIN)"

clean.log: .FORCE
	rm -f $(BASE.DIR)/debug.log

clean:. clean.log
	rm -rf $(TEST.ENV)
	rm -rf $(BUILD.DIR)
	rm -f $(BASE.DIR)/tags

.FORCE:

