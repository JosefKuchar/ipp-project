clean:
	rm -f xkucha28.zip

zip: clean
	zip -j xkucha28.zip php/parse.php php/readme1.pdf

submit_test: zip
	./is_it_ok.sh xkucha28.zip

test_php:
	cd php && php8.1 test.php
