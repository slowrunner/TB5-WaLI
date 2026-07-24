#!/bin/bash

cd ~/TB5-WaLI/wali_ws

echo "Clear logs/YYYY-MM-DD_hh-mm_test_tour.log"
if ! ls -alt ../logs/tmp/*test_tour.log  2>/dev/null; then
  echo "No files found.  Exiting."
  exit 1
fi
echo "***"
rm -i ../logs/tmp/*test_tour.log < /dev/tty

echo "Done"
