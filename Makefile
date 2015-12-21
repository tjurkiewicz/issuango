

.virtualenv: requirements.txt
	rm -fr $@ && virtualenv $@ && . $@/bin/activate && pip install -r $^


test: .virtualenv
	make -C src test

