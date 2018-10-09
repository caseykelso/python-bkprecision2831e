# python-bkprecision2831e
A python program to make measurements with a BK Precision Multimeter 2831E.

# Ubuntu 18.04 Environment Setup
```bash
sudo apt-get install gdb python-dbg git virtualenv
sudo pip install --upgrade pip
```

# Installation
```bash
git clone https://github.com/mrkmedvedev/python-bkprecision2831e.git
make bootstrap
```

# Run Capture Script
```bash
make capture
```

# Debug
```bash
make gdb
```

# Watch Debug Log
```bash
tail -F debug.log
```

# Configure BK Precision 2831E
* Using the menu change the baud rate to 38.4k
* Set TX termination to CR

# References
* [BK Precision 2831E manual](https://bkpmedia.s3.amazonaws.com/downloads/manuals/en-us/2831Eand5491B_manual.pdf)

