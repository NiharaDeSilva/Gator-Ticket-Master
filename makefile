PYTHON = python3
PROGRAM = main.py
EXECUTABLE = gatorTicketMaster

# Default file name if not provided
file_name ?= input/Testcase1

all: $(EXECUTABLE)

$(EXECUTABLE): $(PROGRAM)
	echo '#!/usr/bin/env $(PYTHON)' > $(EXECUTABLE)
	cat $(PROGRAM) >> $(EXECUTABLE)
	chmod +x $(EXECUTABLE)

run: $(EXECUTABLE)
	$(PYTHON) $(EXECUTABLE) $(file_name)


clean:
	rm -f $(EXECUTABLE)


help:
	@echo "Usage:"
	@echo "  make all             - Build the executable"
	@echo "  make run file_name=<input_file> - Run the executable with a specified input file"
	@echo "  make clean           - Remove the executable"
	@echo "  make help            - Show this help message"
