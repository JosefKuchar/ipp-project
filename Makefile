clean:
	rm -f xkucha28.zip

zip: clean
	zip -j xkucha28.zip php/parse.php python/*.py doc/*.pdf

submit_test: zip
	yes | ./is_it_ok.sh xkucha28.zip tmp

test_php:
	cd php && php8.1 test.php

test_python:
	cd python && php test.php --int-only --directory=ipp-2023-tests/interpret-only/ --recursive > test-results.html

test_python_both:
	cd python && php test.php --parse-script=../php/parse.php --jexampath=../php/jexamxml.jar --directory=ipp-2023-tests/both/ --recursive > test-results.html

test_python_ultratest:
	cd python && python3 interpret.py --source=manual_tests/ultra_test
