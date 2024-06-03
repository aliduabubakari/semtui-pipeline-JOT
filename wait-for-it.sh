#!/usr/bin/env bash

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 80; do
  >&2 echo "Waiting for $host to be available..."
  sleep 1
done

>&2 echo "$host is available - executing command"
exec $cmd
