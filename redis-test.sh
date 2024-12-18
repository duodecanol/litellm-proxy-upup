#!/bin/bash
export REDISAUTH=${REDIS_PASSWORD}
export REDISHOST=localhost
export REDISPORT=6379
# echo -e '*2\r\n\$4\r\nAUTH\r\n\$16\r\n$REDISAUTH\r\n*2\r\n\$4\r\nINFO\r\n\$5\r\nSTATS\r\n' | nc $REDISHOST $REDISPORT


redis-cli -h $REDISHOST -p 6379 -a $REDISAUTH