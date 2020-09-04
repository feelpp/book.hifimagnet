#!/bin/bash

antora antora-local-feelpp-doc.yml
echo "INFO: File generated in 'build/site/feelpp-doc/'"
npm i -g live-server
live-server build/site
