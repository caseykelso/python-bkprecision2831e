SHELL := /bin/bash
PWD=$(shell pwd)
BASE.DIR=$(PWD)
TEST.DIR=$(PWD)/tests
TEST.BIN=$(TEST.DIR)/tests.py
TEST.ENV=$(PWD)/pyenv
TEST.SH=$(PWD)/test.sh
PYTHON.BIN=$(TEST.ENV)/bin/python
SETUP.PY=$(PWD)/setup.py
ACTIVATE=$(TEST.ENV)/bin/activate
BUILD.DIR=$(PWD)/build

bootstrap: .FORCE
	virtualenv $(TEST.ENV)
	source $(ACTIVATE) && pip install pyserial

install: .FORCE
	source $(ACTIVATE) && python $(SETUP.PY) install 	

test: install
	$(PYTHON.BIN) $(TEST.BIN)

gdb: .FORCE
	gdb $(PYTHON.BIN) -ex "run $(TEST.BIN)"

clean:. .FORCE
	rm -rf $(TEST.ENV)
	rm -rf $(BUILD.DIR)
	rm -f $(BASE.DIR)/debug.log
	rm -f $(BASE.DIR)/tags

.FORCE:

