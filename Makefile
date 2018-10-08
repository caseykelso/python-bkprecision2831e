PWD=$(shell pwd)
BASE.DIR=$(PWD)
TEST.DIR=$(PWD)/tests
TEST.BIN=$(TEST.DIR)/tests.py
TEST.ENV=$(PWD)/pyenv
TEST.SH=$(PWD)/test.sh
PYTHON.BIN=$(TEST.ENV)/bin/python
SETUP.PY=$(PWD)/setup.py
ACTIVATE=$(TEST.ENV)/env/bin/activate
BUILD.DIR=$(PWD)/build

bootstrap: .FORCE
	virtualenv $(TEST.ENV)
	pip install serial --target=$(TEST.ENV)

install: .FORCE
	$(PYTHON.BIN) $(SETUP.PY) install 	

test: .FORCE
	$(PYTHON.BIN) $(TEST.BIN)

gdb: .FORCE
	gdb $(PYTHON.BIN) -ex "run $(TEST.BIN)"

clean:. .FORCE
	rm -rf $(TEST.ENV)
	rm -rf $(BUILD.DIR)
	rm -f $(BASE.DIR)/debug.log
	rm -f $(BASE.DIR)/tags

.FORCE:

