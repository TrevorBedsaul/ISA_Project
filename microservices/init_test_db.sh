#!/bin/bash

mysql -uroot -p'$3cureUS' -e "grant all on test_cs4501.* to 'www'@'%';"
