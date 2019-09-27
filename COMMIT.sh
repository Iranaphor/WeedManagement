#!/bin/sh

@ECHO off
git config user.name "Iranaphor"
git config user.email "Primordia@live.com"

git config --global user.name "Iranaphor"
git config --global user.email "Primordia@live.com"

git add .

git commit -am "Automatic Commit"

git push origin


git config unset user.name 
git config unset user.email
git config --global unset user.name 
git config --global unset user.email
