PWD=$(shell pwd)
TEST.DIR=$(PWD)/tests
TEST.BIN=$(TEST.DIR)/bkprecision_test.py

gdb: .FORCE
	gdb python -ex "run $(TEST.BIN)"

.FORCE:

