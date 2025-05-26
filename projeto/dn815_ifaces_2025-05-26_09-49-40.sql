# ************************************************************
# Antares - SQL Client
# Version 0.7.34
# 
# https://antares-sql.app/
# https://github.com/antares-sql/antares
# 
# Host: 127.0.0.1 (MySQL Community Server  5.7.44)
# Database: dn815_ifaces
# Generation time: 2025-05-26T09:49:53-03:00
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table employees
# ------------------------------------------------------------

DROP TABLE IF EXISTS `employees`;

CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `autorized` int(11) DEFAULT NULL,
  `employees_code` varchar(45) DEFAULT NULL,
  `fullname` varchar(105) DEFAULT NULL,
  `rg` varchar(45) DEFAULT NULL,
  `cpf` varchar(45) DEFAULT NULL,
  `controller_code` varchar(45) DEFAULT NULL,
  `company_join` varchar(45) DEFAULT NULL,
  `remote_event_code` varchar(200) DEFAULT NULL,
  `remote_uuid` varchar(250) DEFAULT NULL,
  `data_bloqueio_liberacao` varchar(100) NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `iface` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





# Dump of table employees_history
# ------------------------------------------------------------

DROP TABLE IF EXISTS `employees_history`;

CREATE TABLE `employees_history` (
  `employees_code_id` int(11) NOT NULL AUTO_INCREMENT,
  `employees_iface_id` varchar(20) DEFAULT NULL,
  `employees_remote_code` varchar(20) DEFAULT NULL,
  `remote_event_code` varchar(20) DEFAULT NULL,
  `remote_uud` varchar(100) DEFAULT NULL,
  `fullname` varchar(100) DEFAULT NULL,
  `company_join` varchar(100) DEFAULT NULL,
  `readding` varchar(200) DEFAULT NULL,
  `recordType` int(11) DEFAULT NULL,
  `process` datetime DEFAULT NULL,
  `upload` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`employees_code_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;





# Dump of table employees_update
# ------------------------------------------------------------

DROP TABLE IF EXISTS `employees_update`;

CREATE TABLE `employees_update` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operacao` varchar(100) DEFAULT NULL,
  `codigo_funcionario` varchar(100) DEFAULT NULL,
  `data_bloqueio_liberacao` varchar(100) DEFAULT NULL,
  `hash_64_dig_1` text,
  `hash_64_dig_2` text,
  `numero_cracha` varchar(100) DEFAULT NULL,
  `codigo_bloqueio` int(11) DEFAULT NULL,
  `codigoObra` int(11) DEFAULT NULL,
  `employees_code` int(11) NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `employees_update_employees_FK` (`employees_code`),
  CONSTRAINT `employees_update_employees_FK` FOREIGN KEY (`employees_code`) REFERENCES `employees` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





# Dump of table events_bus
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_bus`;

CREATE TABLE `events_bus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(205) DEFAULT NULL,
  `command` varchar(100) DEFAULT NULL,
  `parameters` text,
  `state` varchar(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





# Dump of table events_bus_response
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_bus_response`;

CREATE TABLE `events_bus_response` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(205) DEFAULT NULL,
  `result` longtext,
  `command` varchar(250) NOT NULL,
  `type` varchar(10) DEFAULT NULL,
  `created_at` varchar(20) DEFAULT NULL,
  `process_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





# Dump of table settings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `settings`;

CREATE TABLE `settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(100) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `paramets` text,
  `json` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;

INSERT INTO `settings` (`id`, `type`, `description`, `paramets`, `json`) VALUES
	(5, "SETTING_BLOQUEAR_EMPLOYEES", "*", NULL, "*");

/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;



# Dump of views
# ------------------------------------------------------------

# Creating temporary tables to overcome VIEW dependency errors


/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

# Dump completed on 2025-05-26T09:49:53-03:00
