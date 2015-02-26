deploy:
	appcfg.py --oauth2 update .

requirements: clean
	pip install -r requirements.txt -t lib/

clean:
	rm -Rf $(PWD)/lib/*
