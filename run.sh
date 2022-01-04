#!/bin/sh

./bin/ejabberdctl start

sleep 15

./bin/ejabberdctl register admin localhost password
./bin/ejabberdctl register receiver localhost receiver_password
./bin/ejabberdctl register sender localhost sender_password

tail -f logs/ejabberd.log
