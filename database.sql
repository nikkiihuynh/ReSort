-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: resort
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Compost`
--

DROP TABLE IF EXISTS `Compost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Compost` (
  `compost_ID` int NOT NULL AUTO_INCREMENT,
  `c_material` varchar(255) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`compost_ID`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `compost_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Compost`
--

LOCK TABLES `Compost` WRITE;
/*!40000 ALTER TABLE `Compost` DISABLE KEYS */;
INSERT INTO `Compost` VALUES (6,'cheese crumbs',NULL),(7,'cheese crumbs',NULL),(10,'cheese crumbs',14),(11,'Candied Ginger',14),(12,'apple core',14),(13,'Pizza Box',14),(14,'apple core',14);
/*!40000 ALTER TABLE `Compost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Recycle`
--

DROP TABLE IF EXISTS `Recycle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recycle` (
  `recycle_ID` int NOT NULL AUTO_INCREMENT,
  `r_material` varchar(255) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`recycle_ID`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `recycle_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Recycle`
--

LOCK TABLES `Recycle` WRITE;
/*!40000 ALTER TABLE `Recycle` DISABLE KEYS */;
INSERT INTO `Recycle` VALUES (6,'plastic bottle',NULL),(7,'plastic can',NULL),(8,'newspaper',NULL),(9,'pizza box',NULL),(10,'pizza box',NULL),(13,'pizza box',14),(14,'plastic bottle',14),(15,'diet coke',14),(16,' Plastic Bag ',14),(17,' plastic bag ',14),(18,'paper bin',14);
/*!40000 ALTER TABLE `Recycle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sorted`
--

DROP TABLE IF EXISTS `Sorted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sorted` (
  `user_ID` int NOT NULL,
  `trash_ID` int DEFAULT NULL,
  `recycle_ID` int DEFAULT NULL,
  `compost_ID` int DEFAULT NULL,
  PRIMARY KEY (`user_ID`),
  KEY `trash_ID` (`trash_ID`),
  KEY `recycle_ID` (`recycle_ID`),
  KEY `compost_ID` (`compost_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sorted`
--

LOCK TABLES `Sorted` WRITE;
/*!40000 ALTER TABLE `Sorted` DISABLE KEYS */;
/*!40000 ALTER TABLE `Sorted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SortingHistory`
--

DROP TABLE IF EXISTS `SortingHistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SortingHistory` (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `item` varchar(255) NOT NULL,
  `disposal_method` enum('trash','recycle','compost') NOT NULL,
  `sort_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`history_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sortinghistory_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SortingHistory`
--

LOCK TABLES `SortingHistory` WRITE;
/*!40000 ALTER TABLE `SortingHistory` DISABLE KEYS */;
INSERT INTO `SortingHistory` VALUES (5,14,'pizza box','recycle','2025-04-29 07:18:53'),(6,14,'cheese crumbs','compost','2025-04-29 07:24:20'),(7,14,'plastic bottle','recycle','2025-04-29 22:32:44'),(8,14,'Pizza Box','trash','2025-04-29 22:55:20'),(9,14,'Candied Ginger','compost','2025-04-29 23:00:24'),(10,14,'apple core','compost','2025-04-30 00:26:21'),(11,14,'Pizza Box','compost','2025-04-30 03:15:25'),(12,14,'apple core','compost','2025-05-01 05:10:35'),(13,14,'Pizza Box','trash','2025-05-01 05:11:17'),(14,14,'diet coke','recycle','2025-05-10 04:10:46'),(15,14,' Plastic Bag ','recycle','2025-05-10 04:14:08'),(16,14,' plastic bag ','recycle','2025-05-10 05:20:08'),(17,14,'paper bin','recycle','2025-05-10 05:20:56');
/*!40000 ALTER TABLE `SortingHistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Trash`
--

DROP TABLE IF EXISTS `Trash`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Trash` (
  `trash_ID` int NOT NULL AUTO_INCREMENT,
  `t_material` varchar(255) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`trash_ID`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `trash_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Trash`
--

LOCK TABLES `Trash` WRITE;
/*!40000 ALTER TABLE `Trash` DISABLE KEYS */;
INSERT INTO `Trash` VALUES (6,'trash bag',NULL),(7,'Taco bell',NULL),(8,'Pizza Box',14),(9,'Pizza Box',14);
/*!40000 ALTER TABLE `Trash` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `user_ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_ID`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `password` (`password`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (14,'Rajiv','$2b$12$SAk7CafrOIPisayqsIRC0eZFCi5pHYa6Of5WW4HPEhTKv3HASTDQm','rajiv.mohan@gmail.com'),(15,'Mohan','$2b$12$ost.awmHmZ/YZ0OrAWFPAO0hLgsbDTuwMXo9/wwGR8BhEXzzZlzl6','mohan@gmail.com'),(16,'Johnny','$2b$12$34D.KGodrJDUNVEZq0sTsunKtFuVU6GaSIzt0AHtWNoDhglpTGI3G','johndoe@gmail.com'),(17,'Manas','$2b$12$51j8bG9XoYOFS6r7W5SUzOHscg3CjBXMP9cxgVDLX8X2BhFxiyhVm','manas@gmail.com');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-13 14:27:32
