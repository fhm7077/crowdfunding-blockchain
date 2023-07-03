/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - crowdfunding
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`crowdfunding` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `crowdfunding`;

/*Table structure for table `charity` */

DROP TABLE IF EXISTS `charity`;

CREATE TABLE `charity` (
  `charity id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `subject` varchar(20) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`charity id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `charity` */

insert  into `charity`(`charity id`,`Name`,`email`,`subject`,`description`) values 
(6,'fhm','ffhm@gmail.com','faah','haaf'),
(7,'Mohammed Faheem','Fhm@gmail.com','Charity needed','Kidney Patient');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `comp_id` int(11) NOT NULL AUTO_INCREMENT,
  `complaint` varchar(200) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `reply` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`comp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`comp_id`,`complaint`,`userid`,`reply`,`date`,`status`) values 
(1,'Refund issue',2,'will solve','1970-01-14','replied'),
(2,'abcd',0,'pending','2023-03-03','pending'),
(3,'ssssss',0,'pending','2023-03-03','pending'),
(4,'abcd',9,'Sorry for the inconvenience, we will solve the issue soon. Thanks for the patients ','2023-03-03','replied'),
(5,'hiii\r\n',2,'issued','2023-04-08','replied');

/*Table structure for table `donation_request` */

DROP TABLE IF EXISTS `donation_request`;

CREATE TABLE `donation_request` (
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `date_entry` date DEFAULT NULL,
  `amount` int(20) DEFAULT NULL,
  `needed_beforedate` date DEFAULT NULL,
  `purpose` varchar(100) DEFAULT NULL,
  `orglid` int(11) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `status` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `donation_request` */

insert  into `donation_request`(`did`,`date_entry`,`amount`,`needed_beforedate`,`purpose`,`orglid`,`description`,`status`) values 
(4,'2023-03-02',5,'2023-03-01','abcd',1,'asdsddryht','refunddone'),
(5,'2023-02-28',4,'2023-03-16','jkll',8,'.kjh','refunddone'),
(6,'2023-04-05',2,'2023-04-05','fff',1,'fff','refunddone'),
(7,'2023-04-13',3,'2023-04-26','ertre',1,'tree','approved'),
(8,'2023-04-24',6,'2023-04-19','frd',4,'dr','refunddone'),
(9,'2023-04-20',7,'2023-04-22','abcd',1,'abcd','approved'),
(10,'2023-04-12',3,'2023-04-09','abc',1,'abc','approved'),
(11,'2023-04-27',7,'2023-04-22','abcd',10,'abcddd','approved'),
(12,'2023-05-04',20,'2023-05-31','Charity',4,'Charity puposes medical','approved'),
(13,'2023-05-05',21,'2023-05-30','charity kozhikode',10,'Treatment','approved'),
(14,'2023-05-05',12,'2023-05-29','admin check',1,'checking','approved'),
(15,'2023-05-06',7,'2023-05-26','abc',1,'tatt','approved');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`type`) values 
(1,'admin ','admin','admin'),
(2,'nimmy','123','user'),
(3,'fhmm7','1234 ','organization '),
(4,'hiba7','1234','organization'),
(5,'org77','123','organization'),
(6,'org66','123','organization'),
(7,'hiba123','123','user'),
(8,'abcd','abc','organization'),
(9,'hiba7077','123','user'),
(10,'org','123','organization'),
(13,'user','123','user'),
(14,'nm','123','user');

/*Table structure for table `organization` */

DROP TABLE IF EXISTS `organization`;

CREATE TABLE `organization` (
  `organization_id` int(11) NOT NULL AUTO_INCREMENT,
  `org_lid` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `aboutus` varchar(100) DEFAULT NULL,
  `estd` varchar(100) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `organization` */

insert  into `organization`(`organization_id`,`org_lid`,`name`,`place`,`city`,`state`,`email`,`aboutus`,`estd`,`status`) values 
(2,4,'hiba muhammed','hh','hh','hh','hh','hh','hh','accepted'),
(5,8,'abcd','mpm','mpm','kerxxx','ff@gmail.com','abc','1022','accepted'),
(6,10,'ILA','Kuttippuram','Malappuram','Kerala','ila@gmail.com','Palliative care','2011','accepted'),
(7,11,'ff','ff','ff','ff','ff@gmail.com','ff','ff','pending'),
(8,12,'ff','ff','ff','ff','ff@gmail.com','ff','ff','rejected'),
(9,1,'Admin','Place','city','state','crowdfunding@mail.com','Crowdfunding Admin','2023','accepted');

/*Table structure for table `refund_status` */

DROP TABLE IF EXISTS `refund_status`;

CREATE TABLE `refund_status` (
  `refund_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`refund_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=latin1;

/*Data for the table `refund_status` */

insert  into `refund_status`(`refund_id`,`user_id`,`request_id`,`amount`) values 
(3,13,14,'8.0'),
(4,13,14,'12.0'),
(5,13,14,'24.0'),
(6,13,14,'2.0'),
(7,13,14,'3.0'),
(8,13,14,'6.0'),
(9,13,14,'2.0'),
(10,13,14,'3.0'),
(11,13,14,'6.0'),
(12,13,14,'2.0'),
(13,13,14,'3.0'),
(14,13,14,'6.0'),
(15,13,14,'2.0'),
(16,13,14,'3.0'),
(17,13,14,'6.0'),
(18,13,7,'3'),
(19,13,7,'3'),
(20,2,11,'14.0'),
(21,13,11,'7.0'),
(22,2,11,'14.0'),
(23,13,6,'1'),
(24,2,11,'14.0'),
(25,13,11,'7.0'),
(26,2,11,'7.0'),
(27,13,11,'3.5'),
(28,13,6,'2'),
(29,2,11,'14.0'),
(30,13,11,'7.0'),
(31,2,11,'21.0'),
(32,13,11,'10.5'),
(33,2,11,'14.0'),
(34,13,11,'7.0'),
(35,2,11,'7.0'),
(36,13,11,'3.5'),
(37,2,11,'0.2857142857142857'),
(38,13,11,'0.5714285714285714'),
(39,2,11,'0.2857142857142857'),
(40,13,11,'0.5714285714285714'),
(41,2,11,'0.2857142857142857'),
(42,13,11,'0.5714285714285714'),
(43,2,11,'0.42857142857142855'),
(44,13,11,'0.8571428571428571'),
(45,2,11,'0.42857142857142855'),
(46,13,11,'0.8571428571428571'),
(47,2,11,'0.2857142857142857'),
(48,13,11,'0.5714285714285714'),
(49,13,11,'1.0'),
(50,13,11,'1.0'),
(51,13,7,'1'),
(52,13,7,'1'),
(53,13,4,'1'),
(54,13,4,'1'),
(55,13,14,'2.0'),
(56,13,14,'3.0'),
(57,13,14,'6.0'),
(58,9,4,'8.333333333333334'),
(59,14,4,'25.0'),
(60,13,4,'25.0'),
(61,13,8,'2.0'),
(62,9,8,'2.0'),
(63,13,8,'2.0'),
(64,9,8,'2.0'),
(65,13,8,'2.0'),
(66,9,8,'2.0'),
(67,13,8,'2.0'),
(68,9,8,'2.0'),
(69,13,8,'2.0'),
(70,9,8,'2.0'),
(71,13,8,'2.0'),
(72,9,8,'2.0'),
(73,13,8,'2.0'),
(74,9,8,'2.0'),
(75,13,8,'2.0'),
(76,9,8,'2.0'),
(77,13,8,'2.0'),
(78,9,8,'2.0'),
(79,9,6,'4.0'),
(80,13,6,'4.0'),
(81,9,6,'1.0'),
(82,13,6,'1.0'),
(83,9,6,'1.0'),
(84,13,6,'1.0'),
(85,13,8,'3.0'),
(86,9,8,'3.0'),
(87,13,8,'3.0'),
(88,9,8,'3.0'),
(89,13,8,'3.0'),
(90,9,8,'3.0'),
(91,13,8,'3.0'),
(92,9,8,'3.0'),
(93,2,5,'1.0'),
(94,13,5,'1.0'),
(95,2,5,'0.5'),
(96,13,5,'0.5'),
(97,2,5,'0.5'),
(98,13,5,'0.5'),
(99,2,5,'0.5'),
(100,13,5,'0.5');

/*Table structure for table `user_account` */

DROP TABLE IF EXISTS `user_account`;

CREATE TABLE `user_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `account_no` varchar(100) DEFAULT NULL,
  `key` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `user_account` */

insert  into `user_account`(`id`,`uid`,`account_no`,`key`) values 
(1,2,'0x0Bad3413ff89981905136E3B157789278D89C18e','0x46579eebc1f8f4c59c21b4aef79d95566c489dff28317f790777bc14a857d40c'),
(2,7,'0x936F22DB9D7dFD2a85eBACcD4E00e4C0a127ABa8','0x2ca24c637473f5ddc40b96ad7d13f167921fbe21963450ce6779cb154bbaae3c'),
(3,9,'0x971f5177Dc07c86166b30426F199e3C1C2A8B3cC','0xf8890091a57cd47c3109f73015bfe2bd441d40894557117cd2c785b96794a9c9'),
(4,13,'0xCa7Ea411ca62F64B43b05d697a24dc4641f49076','0xd29d77535ab82965934e908a3493b3ae8c08f3a5ba916a333e7e129e6fbccb94'),
(5,14,'0x483FF128E2a98b4D0185c3A1BD04dA9575131360','0x71bd81e11695b25d9f9e8aa12186d1b36036289e08e7ce817a39eef3d4ec200b');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `lid` int(11) DEFAULT NULL,
  `place` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `pincode` int(20) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`uid`,`name`,`email`,`phone`,`photo`,`lid`,`place`,`state`,`city`,`pincode`) values 
(1,'nishma','nishma@gmail.com','766566','/static/userphoto/20230209130831.jpg',2,'tanur','tirur','ker',676552),
(2,'hibutty','hibutty@gmail.com','975678909','/static/userphoto/20230224121353.jpg',7,'vadakkekad','askdf','kerala',45678),
(3,'Hiba','hibahmq@gmail.com','86061559112','/static/userphoto/20230303121254.jpg',9,'Thrissur','Vadakkekad','Kerala',679562),
(4,'user','nm@gmail.com','nm','/static/userphoto/20230408132852.jpg',13,'nm','nm','nm',0),
(5,'nm','nm@gmail.com','nm','/static/userphoto/20230408133019.jpg',14,'nm','nm','nm',0);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
