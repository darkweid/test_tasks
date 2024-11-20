# Parameters
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
TASK1_DIR = task1
TASK2_DIR = task2
TASK3_DIR = task3

# Create virtual environment and install dependencies
install:
	python3 -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt

# Run all tests (for task1, task2, task3)
test_all:
	$(PYTHON) -m unittest discover $(TASK1_DIR)
	$(PYTHON) -m unittest discover $(TASK2_DIR)
	$(PYTHON) -m unittest discover $(TASK3_DIR)

# Run tests for task1
test_task1:
	$(PYTHON) -m unittest discover $(TASK1_DIR)

# Run tests for task2
test_task2:
	$(PYTHON) -m unittest discover $(TASK2_DIR)

# Run tests for task3
test_task3:
	$(PYTHON) -m unittest discover $(TASK3_DIR)


# Clean temporary files
clean:
	rm -rf $(VENV_DIR)

# Run everything (create venv, run all tests)
all: venv test_all
