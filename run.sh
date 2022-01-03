#!/bin/sh

./bin/ejabberdctl start

sleep 15

./bin/ejabberdctl register admin localhost password

./bin/ejabberdctl register sender localhost password
./bin/ejabberdctl register receiver localhost password

tail -f logs/ejabberd.log
