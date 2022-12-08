#!/usr/bin/env bash

CMD="mfsmount /mnt/moosefs -f"

#Add host if set
if [ ! -z ${MASTER_HOST+X} ];
    then
        CMD="$CMD -H $MASTER_HOST"
fi

#Add host if set
if [ ! -z ${MASTER_PORT+X} ];
    then
        CMD="$CMD -P $MASTER_PORT"
fi

$CMD &

# Sleep to ensure MySQL database is set up
sleep 10
# Run unit tests
pytest /code/test.py
# Run the server
python3 /code/app.py 

