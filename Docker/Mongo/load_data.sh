#!/bin/bash
cd ../data
mongorestore -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin -d my_database -c rlt_data sample_collection.bson