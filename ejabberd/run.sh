#!/bin/sh

print_usage() {
  # Prints script usage

  cat <<EOF
Usage: $0 [-p PASSWORD] [-h]
    -p, --password                        admin password (default: $EJABBERD_ADMIN_PASSWORD or admin)
    -h, --help                            prints this message
EOF
}

password="${EJABBERD_ADMIN_PASSWORD:-admin}"

while [ "$#" -gt 0 ]; do
  case "$1" in
  -p | --password)
    shift
    password="$1"
    ;;
  -h | --help)
    print_usage
    exit
    ;;
  esac
  shift
done

./bin/ejabberdctl start   # start the server (asynchronously)
./bin/ejabberdctl started # wait for the server to finish starting

./bin/ejabberdctl register admin localhost "$password"

tail -f ./logs/ejabberd.log # follow logs
