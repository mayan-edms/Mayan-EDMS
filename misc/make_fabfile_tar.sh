#!/bin/sh
find 'fabfile' -depth -name '*.pyc' -exec rm {} \;
tar -czvf contrib/fabfile.tar.gz fabfile
