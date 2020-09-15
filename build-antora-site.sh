#!/bin/bash

antora antora-local-feelpp-doc.yml > log 2>&1
echo "INFO: File generated in 'build/site/feelpp-doc/'"
npm i -g live-server
live-server build/site
