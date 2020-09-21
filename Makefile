# Notes Commands

# Push local notes to the origin
p push:
	git push origin "ref/notes/*"

# Fetch origin notes to local
f fetch:
	git fetch origin "refs/notes/*:refs/notes/*"

# Display the notes
s show:
	git notes show

# Git log displays the note attached to the commit
l log:
	git log

# Decode OP_RETURN transaction
exd example-decode:
	echo  7265706f3a2070726f796563746f2d636861756368612f636861756368612d6768612d6f7072657475726e203b206272616e63683a20726566732f68656164732f6d6173746572203b20636f6d6d69743a2037643232656362613964343431663730373539323364353764653037376362346366383137373864 | xxd -p -r