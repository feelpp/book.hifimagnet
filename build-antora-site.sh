#!/bin/bash

antora antora-local-feelpp-doc.yml > log 2>&1
echo "INFO: File generated in 'build/site/feelpp-doc/'"
npm i -g live-server
npm i -g live-server-https
live-server --https=/usr/local/lib/node_modules/live-server-https build/site
#live-server build/site
