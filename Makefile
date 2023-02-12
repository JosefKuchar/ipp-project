clean:
	rm -f xkucha28.zip

zip: clean
	zip -j xkucha28.zip php/parse.php python/*.py doc/*.pdf

submit_test: zip
	yes | ./is_it_ok.sh xkucha28.zip tmp

test_php:
	cd php && php8.1 test.php
