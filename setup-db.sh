docker pull mysql:5.7.14
mkdir ~/cs4501/db
docker run --name mysql -d -e MYSQL\_ROOT\_PASSWORD='$3cureUS' -v ~/cs4501/db:/var/lib/mysql  mysql:5.7.14
docker run -it --name mysql-cmdline --link mysql:db mysql:5.7.14 bash
