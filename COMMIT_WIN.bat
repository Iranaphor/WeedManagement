@echo off

git config user.name "Iranaphor"
git config user.email "Primordia@live.com"

git config --global user.name "Iranaphor"
git config --global user.email "Primordia@live.com"

git add .

git commit -am "Automatic Commit"

git push origin


git config user.name unset
git config user.email unset
git config --global user.name unset
git config --global user.email unset
