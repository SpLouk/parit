all:
	mkdir -p ~/.config/parit/
	cp -i config/* ~/.config/parit/
	mkdir -p /usr/local/lib/python2.7/dist-packages/parit/
	cp src/* /usr/local/lib/python2.7/dist-packages/parit/
	cp parit /usr/local/bin/

remove:
	rm -r /usr/local/lib/python2.7/dist-packages/parit
	rm /usr/local/bin/parit
