-- MySQL dump 10.13  Distrib 5.5.52, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: isensit_gw
-- ------------------------------------------------------
-- Server version	5.5.52-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acc_beacons`
--

DROP TABLE IF EXISTS `acc_beacons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acc_beacons` (
  `row_count` int(30) NOT NULL AUTO_INCREMENT,
  `beacon_id` int(11) NOT NULL,
  `beacon_accx` float NOT NULL,
  `beacon_accy` float NOT NULL,
  `beacon_accz` float NOT NULL,
  `beacon_rssi` int(11) NOT NULL,
  `created_at` varchar(30) DEFAULT NULL,
  `bad_lift` int(11) DEFAULT NULL,
  `total_lift` int(11) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `small_count` int(2) DEFAULT NULL,
  `middle_count` int(2) DEFAULT NULL,
  `large_count` int(2) DEFAULT NULL,
  PRIMARY KEY (`row_count`)
) ENGINE=InnoDB AUTO_INCREMENT=3660997 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acc_beacons`
--

LOCK TABLES `acc_beacons` WRITE;
/*!40000 ALTER TABLE `acc_beacons` DISABLE KEYS */;
/*!40000 ALTER TABLE `acc_beacons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fd_sensors`
--

DROP TABLE IF EXISTS `fd_sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fd_sensors` (
  `row_count` int(11) NOT NULL AUTO_INCREMENT,
  `fd_id` varchar(11) NOT NULL,
  `pm` float(10,1) NOT NULL,
  `temp` float(10,2) NOT NULL,
  `hum` float(10,2) NOT NULL,
  `pm_hour` float(10,1) NOT NULL,
  `created_at` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`row_count`)
) ENGINE=InnoDB AUTO_INCREMENT=156023 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fd_sensors`
--

LOCK TABLES `fd_sensors` WRITE;
/*!40000 ALTER TABLE `fd_sensors` DISABLE KEYS */;
/*!40000 ALTER TABLE `fd_sensors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `row_count` int(11) NOT NULL AUTO_INCREMENT,
  `beacon_id` int(11) DEFAULT NULL,
  `cal_val` float(10,2) NOT NULL,
  PRIMARY KEY (`row_count`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,2687,25.00),(2,2834,7.00),(3,3063,7.00),(4,1869,14.00),(5,3262,23.50),(6,2730,24.00),(7,3890,17.00);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-07 11:42:54
