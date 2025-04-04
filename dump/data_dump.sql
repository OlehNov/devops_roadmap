-- MySQL dump 10.13  Distrib 9.2.0, for Linux (x86_64)
--
-- Host: localhost    Database: eventlog
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `eventlog`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `eventlog` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `eventlog`;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'eventlogs','0001_initial','2025-02-20 21:00:19.560695');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventlog`
--

DROP TABLE IF EXISTS `eventlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `user_email` varchar(254) DEFAULT NULL,
  `instance` longtext,
  `operation_type` smallint DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventlog`
--

LOCK TABLES `eventlog` WRITE;
/*!40000 ALTER TABLE `eventlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Current Database: `glamp`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `glamp` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `glamp`;

--
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrator` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` int unsigned NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `status` smallint unsigned DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `administrator_user_id_38af1e1e_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `administrator_chk_1` CHECK ((`id` >= 0)),
  CONSTRAINT `administrator_chk_2` CHECK ((`status` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrator`
--

LOCK TABLES `administrator` WRITE;
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
/*!40000 ALTER TABLE `administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add site',6,'add_site'),(22,'Can change site',6,'change_site'),(23,'Can delete site',6,'delete_site'),(24,'Can view site',6,'view_site'),(25,'Can add crontab',7,'add_crontabschedule'),(26,'Can change crontab',7,'change_crontabschedule'),(27,'Can delete crontab',7,'delete_crontabschedule'),(28,'Can view crontab',7,'view_crontabschedule'),(29,'Can add interval',8,'add_intervalschedule'),(30,'Can change interval',8,'change_intervalschedule'),(31,'Can delete interval',8,'delete_intervalschedule'),(32,'Can view interval',8,'view_intervalschedule'),(33,'Can add periodic task',9,'add_periodictask'),(34,'Can change periodic task',9,'change_periodictask'),(35,'Can delete periodic task',9,'delete_periodictask'),(36,'Can view periodic task',9,'view_periodictask'),(37,'Can add periodic tasks',10,'add_periodictasks'),(38,'Can change periodic tasks',10,'change_periodictasks'),(39,'Can delete periodic tasks',10,'delete_periodictasks'),(40,'Can view periodic tasks',10,'view_periodictasks'),(41,'Can add solar event',11,'add_solarschedule'),(42,'Can change solar event',11,'change_solarschedule'),(43,'Can delete solar event',11,'delete_solarschedule'),(44,'Can view solar event',11,'view_solarschedule'),(45,'Can add clocked',12,'add_clockedschedule'),(46,'Can change clocked',12,'change_clockedschedule'),(47,'Can delete clocked',12,'delete_clockedschedule'),(48,'Can view clocked',12,'view_clockedschedule'),(49,'Can add task result',13,'add_taskresult'),(50,'Can change task result',13,'change_taskresult'),(51,'Can delete task result',13,'delete_taskresult'),(52,'Can view task result',13,'view_taskresult'),(53,'Can add chord counter',14,'add_chordcounter'),(54,'Can change chord counter',14,'change_chordcounter'),(55,'Can delete chord counter',14,'delete_chordcounter'),(56,'Can view chord counter',14,'view_chordcounter'),(57,'Can add group result',15,'add_groupresult'),(58,'Can change group result',15,'change_groupresult'),(59,'Can delete group result',15,'delete_groupresult'),(60,'Can view group result',15,'view_groupresult'),(61,'Can add blacklisted token',16,'add_blacklistedtoken'),(62,'Can change blacklisted token',16,'change_blacklistedtoken'),(63,'Can delete blacklisted token',16,'delete_blacklistedtoken'),(64,'Can view blacklisted token',16,'view_blacklistedtoken'),(65,'Can add outstanding token',17,'add_outstandingtoken'),(66,'Can change outstanding token',17,'change_outstandingtoken'),(67,'Can delete outstanding token',17,'delete_outstandingtoken'),(68,'Can view outstanding token',17,'view_outstandingtoken'),(69,'Can add administrator',18,'add_administrator'),(70,'Can change administrator',18,'change_administrator'),(71,'Can delete administrator',18,'delete_administrator'),(72,'Can view administrator',18,'view_administrator'),(73,'Can add Category',19,'add_category'),(74,'Can change Category',19,'change_category'),(75,'Can delete Category',19,'delete_category'),(76,'Can view Category',19,'view_category'),(77,'Can add event log',20,'add_eventlog'),(78,'Can change event log',20,'change_eventlog'),(79,'Can delete event log',20,'delete_eventlog'),(80,'Can view event log',20,'view_eventlog'),(81,'Can add Picture',21,'add_picture'),(82,'Can change Picture',21,'change_picture'),(83,'Can delete Picture',21,'delete_picture'),(84,'Can view Picture',21,'view_picture'),(85,'Can add Glamp',22,'add_glamp'),(86,'Can change Glamp',22,'change_glamp'),(87,'Can delete Glamp',22,'delete_glamp'),(88,'Can view Glamp',22,'view_glamp'),(89,'Can add tourist',23,'add_tourist'),(90,'Can change tourist',23,'change_tourist'),(91,'Can delete tourist',23,'delete_tourist'),(92,'Can view tourist',23,'view_tourist'),(93,'Can add user',24,'add_user'),(94,'Can change user',24,'change_user'),(95,'Can delete user',24,'delete_user'),(96,'Can view user',24,'view_user'),(97,'Can add glamp owner',25,'add_glampowner'),(98,'Can change glamp owner',25,'change_glampowner'),(99,'Can delete glamp owner',25,'delete_glampowner'),(100,'Can view glamp owner',25,'view_glampowner'),(101,'Can add glamp manager',26,'add_glampmanager'),(102,'Can change glamp manager',26,'change_glampmanager'),(103,'Can delete glamp manager',26,'delete_glampmanager'),(104,'Can view glamp manager',26,'view_glampmanager');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(120) DEFAULT NULL,
  `slug` varchar(120) DEFAULT NULL,
  `title` varchar(120) DEFAULT NULL,
  `description` longtext,
  `is_active` tinyint(1) NOT NULL,
  `is_hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_clockedschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_clockedschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_clockedschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `clocked_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_clockedschedule`
--

LOCK TABLES `django_celery_beat_clockedschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_clockedschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_clockedschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_crontabschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) NOT NULL,
  `hour` varchar(96) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(124) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  `timezone` varchar(63) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_crontabschedule`
--

LOCK TABLES `django_celery_beat_crontabschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_intervalschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `every` int NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_intervalschedule`
--

LOCK TABLES `django_celery_beat_intervalschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictask`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_periodictask` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int DEFAULT NULL,
  `interval_id` int DEFAULT NULL,
  `solar_id` int DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int unsigned DEFAULT NULL,
  `headers` longtext NOT NULL DEFAULT (_utf8mb3'{}'),
  `clocked_id` int DEFAULT NULL,
  `expire_seconds` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`),
  CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`),
  CONSTRAINT `django_celery_beat_periodictask_chk_1` CHECK ((`total_run_count` >= 0)),
  CONSTRAINT `django_celery_beat_periodictask_chk_2` CHECK ((`priority` >= 0)),
  CONSTRAINT `django_celery_beat_periodictask_chk_3` CHECK ((`expire_seconds` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictask`
--

LOCK TABLES `django_celery_beat_periodictask` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictasks`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictasks`
--

LOCK TABLES `django_celery_beat_periodictasks` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_solarschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event` varchar(24) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_solarschedule`
--

LOCK TABLES `django_celery_beat_solarschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_results_chordcounter`
--

DROP TABLE IF EXISTS `django_celery_results_chordcounter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_results_chordcounter` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` varchar(255) NOT NULL,
  `sub_tasks` longtext NOT NULL,
  `count` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`),
  CONSTRAINT `django_celery_results_chordcounter_chk_1` CHECK ((`count` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_results_chordcounter`
--

LOCK TABLES `django_celery_results_chordcounter` WRITE;
/*!40000 ALTER TABLE `django_celery_results_chordcounter` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_results_chordcounter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_results_groupresult`
--

DROP TABLE IF EXISTS `django_celery_results_groupresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_results_groupresult` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` varchar(255) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_done` datetime(6) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`),
  KEY `django_cele_date_cr_bd6c1d_idx` (`date_created`),
  KEY `django_cele_date_do_caae0e_idx` (`date_done`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_results_groupresult`
--

LOCK TABLES `django_celery_results_groupresult` WRITE;
/*!40000 ALTER TABLE `django_celery_results_groupresult` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_results_groupresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_results_taskresult`
--

DROP TABLE IF EXISTS `django_celery_results_taskresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_results_taskresult` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext,
  `meta` longtext,
  `task_args` longtext,
  `task_kwargs` longtext,
  `task_name` varchar(255) DEFAULT NULL,
  `worker` varchar(100) DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `periodic_task_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `django_cele_task_na_08aec9_idx` (`task_name`),
  KEY `django_cele_status_9b6201_idx` (`status`),
  KEY `django_cele_worker_d54dd8_idx` (`worker`),
  KEY `django_cele_date_cr_f04a50_idx` (`date_created`),
  KEY `django_cele_date_do_f59aad_idx` (`date_done`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_results_taskresult`
--

LOCK TABLES `django_celery_results_taskresult` WRITE;
/*!40000 ALTER TABLE `django_celery_results_taskresult` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_results_taskresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(18,'administrators','administrator'),(3,'auth','group'),(2,'auth','permission'),(19,'categories','category'),(4,'contenttypes','contenttype'),(12,'django_celery_beat','clockedschedule'),(7,'django_celery_beat','crontabschedule'),(8,'django_celery_beat','intervalschedule'),(9,'django_celery_beat','periodictask'),(10,'django_celery_beat','periodictasks'),(11,'django_celery_beat','solarschedule'),(14,'django_celery_results','chordcounter'),(15,'django_celery_results','groupresult'),(13,'django_celery_results','taskresult'),(20,'eventlogs','eventlog'),(25,'glamp_owners','glampowner'),(22,'glamps','glamp'),(21,'glamps','picture'),(26,'managers','glampmanager'),(5,'sessions','session'),(6,'sites','site'),(16,'token_blacklist','blacklistedtoken'),(17,'token_blacklist','outstandingtoken'),(23,'tourists','tourist'),(24,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-02-20 20:59:45.307574'),(2,'contenttypes','0002_remove_content_type_name','2025-02-20 20:59:45.914208'),(3,'auth','0001_initial','2025-02-20 20:59:47.708959'),(4,'auth','0002_alter_permission_name_max_length','2025-02-20 20:59:48.178446'),(5,'auth','0003_alter_user_email_max_length','2025-02-20 20:59:48.229781'),(6,'auth','0004_alter_user_username_opts','2025-02-20 20:59:48.294984'),(7,'auth','0005_alter_user_last_login_null','2025-02-20 20:59:48.386180'),(8,'auth','0006_require_contenttypes_0002','2025-02-20 20:59:48.436580'),(9,'auth','0007_alter_validators_add_error_messages','2025-02-20 20:59:48.493296'),(10,'auth','0008_alter_user_username_max_length','2025-02-20 20:59:48.555499'),(11,'auth','0009_alter_user_last_name_max_length','2025-02-20 20:59:48.605902'),(12,'auth','0010_alter_group_name_max_length','2025-02-20 20:59:48.719153'),(13,'auth','0011_update_proxy_permissions','2025-02-20 20:59:48.777238'),(14,'auth','0012_alter_user_first_name_max_length','2025-02-20 20:59:48.900598'),(15,'users','0001_initial','2025-02-20 20:59:51.557970'),(16,'admin','0001_initial','2025-02-20 20:59:52.554151'),(17,'admin','0002_logentry_remove_auto_add','2025-02-20 20:59:52.605042'),(18,'admin','0003_logentry_add_action_flag_choices','2025-02-20 20:59:52.647911'),(19,'administrators','0001_initial','2025-02-20 20:59:52.836364'),(20,'administrators','0002_initial','2025-02-20 20:59:53.235318'),(21,'categories','0001_initial','2025-02-20 20:59:53.442667'),(22,'django_celery_beat','0001_initial','2025-02-20 20:59:54.881089'),(23,'django_celery_beat','0002_auto_20161118_0346','2025-02-20 20:59:55.527342'),(24,'django_celery_beat','0003_auto_20161209_0049','2025-02-20 20:59:55.745729'),(25,'django_celery_beat','0004_auto_20170221_0000','2025-02-20 20:59:55.789910'),(26,'django_celery_beat','0005_add_solarschedule_events_choices','2025-02-20 20:59:55.835302'),(27,'django_celery_beat','0006_auto_20180322_0932','2025-02-20 20:59:56.440257'),(28,'django_celery_beat','0007_auto_20180521_0826','2025-02-20 20:59:57.315151'),(29,'django_celery_beat','0008_auto_20180914_1922','2025-02-20 20:59:57.410777'),(30,'django_celery_beat','0006_auto_20180210_1226','2025-02-20 20:59:57.472164'),(31,'django_celery_beat','0006_periodictask_priority','2025-02-20 20:59:57.901598'),(32,'django_celery_beat','0009_periodictask_headers','2025-02-20 20:59:58.336585'),(33,'django_celery_beat','0010_auto_20190429_0326','2025-02-20 20:59:58.560924'),(34,'django_celery_beat','0011_auto_20190508_0153','2025-02-20 20:59:59.143350'),(35,'django_celery_beat','0012_periodictask_expire_seconds','2025-02-20 20:59:59.544039'),(36,'django_celery_beat','0013_auto_20200609_0727','2025-02-20 20:59:59.608981'),(37,'django_celery_beat','0014_remove_clockedschedule_enabled','2025-02-20 20:59:59.888121'),(38,'django_celery_beat','0015_edit_solarschedule_events_choices','2025-02-20 20:59:59.925420'),(39,'django_celery_beat','0016_alter_crontabschedule_timezone','2025-02-20 20:59:59.981381'),(40,'django_celery_beat','0017_alter_crontabschedule_month_of_year','2025-02-20 21:00:00.016382'),(41,'django_celery_beat','0018_improve_crontab_helptext','2025-02-20 21:00:00.042285'),(42,'django_celery_results','0001_initial','2025-02-20 21:00:00.366473'),(43,'django_celery_results','0002_add_task_name_args_kwargs','2025-02-20 21:00:01.290330'),(44,'django_celery_results','0003_auto_20181106_1101','2025-02-20 21:00:01.329012'),(45,'django_celery_results','0004_auto_20190516_0412','2025-02-20 21:00:01.730182'),(46,'django_celery_results','0005_taskresult_worker','2025-02-20 21:00:02.321784'),(47,'django_celery_results','0006_taskresult_date_created','2025-02-20 21:00:02.886122'),(48,'django_celery_results','0007_remove_taskresult_hidden','2025-02-20 21:00:03.208456'),(49,'django_celery_results','0008_chordcounter','2025-02-20 21:00:03.429246'),(50,'django_celery_results','0009_groupresult','2025-02-20 21:00:04.904310'),(51,'django_celery_results','0010_remove_duplicate_indices','2025-02-20 21:00:04.954981'),(52,'django_celery_results','0011_taskresult_periodic_task_name','2025-02-20 21:00:05.253822'),(53,'eventlogs','0001_initial','2025-02-20 21:00:05.377602'),(54,'glamp_owners','0001_initial','2025-02-20 21:00:05.491061'),(55,'glamp_owners','0002_initial','2025-02-20 21:00:05.795504'),(56,'glamps','0001_initial','2025-02-20 21:00:06.405095'),(57,'glamps','0002_initial','2025-02-20 21:00:07.147020'),(58,'managers','0001_initial','2025-02-20 21:00:07.273155'),(59,'managers','0002_initial','2025-02-20 21:00:07.635771'),(60,'sessions','0001_initial','2025-02-20 21:00:08.045663'),(61,'sites','0001_initial','2025-02-20 21:00:08.227318'),(62,'sites','0002_alter_domain_unique','2025-02-20 21:00:08.336704'),(63,'token_blacklist','0001_initial','2025-02-20 21:00:09.676253'),(64,'token_blacklist','0002_outstandingtoken_jti_hex','2025-02-20 21:00:10.106050'),(65,'token_blacklist','0003_auto_20171017_2007','2025-02-20 21:00:10.226900'),(66,'token_blacklist','0004_auto_20171017_2013','2025-02-20 21:00:10.841521'),(67,'token_blacklist','0005_remove_outstandingtoken_jti','2025-02-20 21:00:11.220886'),(68,'token_blacklist','0006_auto_20171017_2113','2025-02-20 21:00:11.458608'),(69,'token_blacklist','0007_auto_20171017_2214','2025-02-20 21:00:12.725187'),(70,'token_blacklist','0008_migrate_to_bigautofield','2025-02-20 21:00:14.760701'),(71,'token_blacklist','0010_fix_migrate_to_bigautofield','2025-02-20 21:00:14.869539'),(72,'token_blacklist','0011_linearizes_history','2025-02-20 21:00:14.896226'),(73,'token_blacklist','0012_alter_outstandingtoken_user','2025-02-20 21:00:14.927235'),(74,'tourists','0001_initial','2025-02-20 21:00:15.197297'),(75,'tourists','0002_initial','2025-02-20 21:00:15.627979');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventlog`
--

DROP TABLE IF EXISTS `eventlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `user_email` varchar(254) DEFAULT NULL,
  `instance` longtext,
  `operation_type` smallint DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventlog`
--

LOCK TABLES `eventlog` WRITE;
/*!40000 ALTER TABLE `eventlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `glamp`
--

DROP TABLE IF EXISTS `glamp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `glamp` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `glamp_type` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_hidden` tinyint(1) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `rating` double DEFAULT NULL,
  `premium_level` smallint unsigned DEFAULT NULL,
  `priority` double DEFAULT NULL,
  `name` varchar(225) NOT NULL,
  `slug` varchar(225) DEFAULT NULL,
  `description` longtext NOT NULL,
  `capacity` smallint unsigned NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `status` smallint unsigned NOT NULL,
  `street` varchar(255) NOT NULL,
  `building_number` varchar(255) DEFAULT NULL,
  `apartment` varchar(25) DEFAULT NULL,
  `city` varchar(255) NOT NULL,
  `region` varchar(255) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `heating_system` tinyint(1) NOT NULL,
  `cooling_system` tinyint(1) NOT NULL,
  `internet` tinyint(1) NOT NULL,
  `laundry_services` tinyint(1) NOT NULL,
  `tv` tinyint(1) NOT NULL,
  `iron` tinyint(1) NOT NULL,
  `workplace` tinyint(1) NOT NULL,
  `pool` tinyint(1) NOT NULL,
  `spa` tinyint(1) NOT NULL,
  `jacuzzi` tinyint(1) NOT NULL,
  `vat` tinyint(1) NOT NULL,
  `sauna` tinyint(1) NOT NULL,
  `fireplace` tinyint(1) NOT NULL,
  `gazebo` tinyint(1) NOT NULL,
  `terrace` tinyint(1) NOT NULL,
  `barbecue_area` tinyint(1) NOT NULL,
  `hammocks` tinyint(1) NOT NULL,
  `garden_furniture` tinyint(1) NOT NULL,
  `pets_farm` tinyint(1) NOT NULL,
  `riding` tinyint(1) NOT NULL,
  `hiking_walking` tinyint(1) NOT NULL,
  `fishing` tinyint(1) NOT NULL,
  `swimming` tinyint(1) NOT NULL,
  `boating` tinyint(1) NOT NULL,
  `alpine_skiing` tinyint(1) NOT NULL,
  `meditation_yoga` tinyint(1) NOT NULL,
  `sports_area` tinyint(1) NOT NULL,
  `game_area` tinyint(1) NOT NULL,
  `events_excursions` tinyint(1) NOT NULL,
  `national_park` tinyint(1) NOT NULL,
  `sea` tinyint(1) NOT NULL,
  `lake` tinyint(1) NOT NULL,
  `stream` tinyint(1) NOT NULL,
  `waterfall` tinyint(1) NOT NULL,
  `thermal_springs` tinyint(1) NOT NULL,
  `mountains` tinyint(1) NOT NULL,
  `salt_caves` tinyint(1) NOT NULL,
  `beautiful_views` tinyint(1) NOT NULL,
  `number_of_bedrooms` smallint unsigned NOT NULL,
  `number_of_beds` smallint unsigned NOT NULL,
  `cot_for_babies` tinyint(1) NOT NULL,
  `number_of_bathrooms` smallint unsigned NOT NULL,
  `bathroom_in_room` tinyint(1) NOT NULL,
  `kitchen_in_room` tinyint(1) NOT NULL,
  `dining_area` tinyint(1) NOT NULL,
  `microwave` tinyint(1) NOT NULL,
  `plate` tinyint(1) NOT NULL,
  `refrigerator` tinyint(1) NOT NULL,
  `kitchen_on_territory` tinyint(1) NOT NULL,
  `no_kitchen` tinyint(1) NOT NULL,
  `breakfast_included` tinyint(1) NOT NULL,
  `lunch_included` tinyint(1) NOT NULL,
  `dinner_included` tinyint(1) NOT NULL,
  `all_inclusive` tinyint(1) NOT NULL,
  `room_service` tinyint(1) NOT NULL,
  `bar` tinyint(1) NOT NULL,
  `restaurant` tinyint(1) NOT NULL,
  `instant_booking` tinyint(1) NOT NULL,
  `reception_24` tinyint(1) NOT NULL,
  `free_cancellation` tinyint(1) NOT NULL,
  `allowed_with_animals` tinyint(1) NOT NULL,
  `suitable_for_children` tinyint(1) NOT NULL,
  `suitable_for_groups` tinyint(1) NOT NULL,
  `can_order_transfer` tinyint(1) NOT NULL,
  `car_charging_station` tinyint(1) NOT NULL,
  `place_for_car` tinyint(1) NOT NULL,
  `projector_and_screen` tinyint(1) NOT NULL,
  `area_for_events` tinyint(1) NOT NULL,
  `territory_under_protection` tinyint(1) NOT NULL,
  `cloakroom` tinyint(1) NOT NULL,
  `without_thresholds` tinyint(1) NOT NULL,
  `no_ladder` tinyint(1) NOT NULL,
  `bath_with_handrails` tinyint(1) NOT NULL,
  `toilet_with_handrails` tinyint(1) NOT NULL,
  `shower_chair` tinyint(1) NOT NULL,
  `suitable_for_guests_in_wheelchairs` tinyint(1) NOT NULL,
  `room_on_first_flor` tinyint(1) NOT NULL,
  `category_id` bigint DEFAULT NULL,
  `owner_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `glamp_category_id_caa730a6_fk_category_id` (`category_id`),
  KEY `glamp_owner_id_480e6d62_fk_user_id` (`owner_id`),
  CONSTRAINT `glamp_category_id_caa730a6_fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `glamp_owner_id_480e6d62_fk_user_id` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`),
  CONSTRAINT `glamp_chk_1` CHECK ((`glamp_type` >= 0)),
  CONSTRAINT `glamp_chk_2` CHECK ((`premium_level` >= 0)),
  CONSTRAINT `glamp_chk_3` CHECK ((`capacity` >= 0)),
  CONSTRAINT `glamp_chk_4` CHECK ((`status` >= 0)),
  CONSTRAINT `glamp_chk_5` CHECK ((`number_of_bedrooms` >= 0)),
  CONSTRAINT `glamp_chk_6` CHECK ((`number_of_beds` >= 0)),
  CONSTRAINT `glamp_chk_7` CHECK ((`number_of_bathrooms` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `glamp`
--

LOCK TABLES `glamp` WRITE;
/*!40000 ALTER TABLE `glamp` DISABLE KEYS */;
/*!40000 ALTER TABLE `glamp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `glamp_owner`
--

DROP TABLE IF EXISTS `glamp_owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `glamp_owner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `is_hidden` tinyint(1) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `vip_status` smallint unsigned DEFAULT NULL,
  `status` smallint unsigned DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `glamp_owner_user_id_4be04279_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `glamp_owner_chk_1` CHECK ((`vip_status` >= 0)),
  CONSTRAINT `glamp_owner_chk_2` CHECK ((`status` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `glamp_owner`
--

LOCK TABLES `glamp_owner` WRITE;
/*!40000 ALTER TABLE `glamp_owner` DISABLE KEYS */;
/*!40000 ALTER TABLE `glamp_owner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` int unsigned NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `status` smallint unsigned DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `manager_user_id_03d26107_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `manager_chk_1` CHECK ((`id` >= 0)),
  CONSTRAINT `manager_chk_2` CHECK ((`status` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `picture`
--

DROP TABLE IF EXISTS `picture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `picture` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `pic` varchar(2000) NOT NULL,
  `glamp_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `picture_glamp_id_7a60cc4b_fk_glamp_id` (`glamp_id`),
  CONSTRAINT `picture_glamp_id_7a60cc4b_fk_glamp_id` FOREIGN KEY (`glamp_id`) REFERENCES `glamp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `picture`
--

LOCK TABLES `picture` WRITE;
/*!40000 ALTER TABLE `picture` DISABLE KEYS */;
/*!40000 ALTER TABLE `picture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outstandingtoken_user_id_83bc629a_fk_user_id` (`user_id`),
  CONSTRAINT `token_blacklist_outstandingtoken_user_id_83bc629a_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tourist`
--

DROP TABLE IF EXISTS `tourist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tourist` (
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `id` int unsigned NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `status` smallint unsigned DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `tourist_user_id_d2b95967_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `tourist_chk_1` CHECK ((`id` >= 0)),
  CONSTRAINT `tourist_chk_2` CHECK ((`status` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tourist`
--

LOCK TABLES `tourist` WRITE;
/*!40000 ALTER TABLE `tourist` DISABLE KEYS */;
/*!40000 ALTER TABLE `tourist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `role` smallint unsigned DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `user_chk_1` CHECK ((`role` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_groups_user_id_group_id_40beef00_uniq` (`user_id`,`group_id`),
  KEY `user_groups_group_id_b76f8aba_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_groups_group_id_b76f8aba_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_groups_user_id_abaea130_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

LOCK TABLES `user_groups` WRITE;
/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_permissions_user_id_permission_id_7dc6e2e0_uniq` (`user_id`,`permission_id`),
  KEY `user_user_permission_permission_id_9deb68a3_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_user_permission_permission_id_9deb68a3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_user_permissions_user_id_ed4a47ea_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_permissions`
--

LOCK TABLES `user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-03 19:59:59
