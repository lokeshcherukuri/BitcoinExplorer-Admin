# mysql -u root

CREATE USER 'username'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL PRIVILEGES ON coinexplorer.* TO 'username'@'localhost';

# exit
