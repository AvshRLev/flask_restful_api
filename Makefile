run:
		python main.py

test: 
		make run & sleep 5 && python -m unittest -v test_main.py