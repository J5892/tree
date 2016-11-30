#!/bin/sh

git remote update

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [[ $LOCAL = $REMOTE ]]; then
    echo "Up-to-date"
elif [[ $LOCAL = $BASE ]]; then
    echo "Need to pull"
    git pull origin master
    sudo killall python
    sudo sh patternlaunch.sh
elif [[ $REMOTE = $BASE ]]; then
    echo "Need to push"
else
    echo "Diverged"
fi
