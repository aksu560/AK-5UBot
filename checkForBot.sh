cd
cd ShadowBOT
if git fetch --dry-run | grep -q -v 'Already up-to-date.' && changed=1; then
	echo "No updates"
else
	echo "Updates found"
	git pull
fi
