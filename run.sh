#!/bin/sh

./bin/ejabberdctl start

sleep 15

./bin/ejabberdctl register admin localhost password

tail -f logs/ejabberd.log
