-- Write a script that creates the database hbtn_0c_0 in your MySQL server.
CREATE DATABASE IF NOT EXISTS `loginform` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;mys
USE `loginform`;;


CREATE  USER IF NOT EXISTS 'loginform'@'localhost' IDENTIFIED BY 'loginform';
GRANT ALL PRIVILEGES ON `loginform`.* TO 'loginform'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'loginform'@'localhost';

-- Write a script that creates a table called first_table in the current database in your MySQL server.
CREATE TABLE IF NOT EXISTS `accounts`(
     `id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com');