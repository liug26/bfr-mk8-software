#!/bin/sh
GIT_HTTPS=https://github.com/liug26/BFRDashboard.git
echo "Cloning from repo: ${GIT_HTTPS}..."
if ! git clone $GIT_HTTPS ; then
    echo "Failed to clone repo"
    exit 1
fi
rm -r -f dash
mv BFRDashboard dash
echo "Success"
