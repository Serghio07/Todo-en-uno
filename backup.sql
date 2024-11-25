-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: mydatabase
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `almacenamiento`
--

DROP TABLE IF EXISTS `almacenamiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `almacenamiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `espacio_utilizado` float NOT NULL,
  `fecha_almacenamiento` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_almacenamiento_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacenamiento`
--

LOCK TABLES `almacenamiento` WRITE;
/*!40000 ALTER TABLE `almacenamiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `almacenamiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documento`
--

DROP TABLE IF EXISTS `documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `contenido` text NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `almacenamiento_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `almacenamiento_id` (`almacenamiento_id`),
  KEY `ix_documento_id` (`id`),
  CONSTRAINT `documento_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `documento_ibfk_2` FOREIGN KEY (`almacenamiento_id`) REFERENCES `almacenamiento` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documento`
--

LOCK TABLES `documento` WRITE;
/*!40000 ALTER TABLE `documento` DISABLE KEYS */;
/*!40000 ALTER TABLE `documento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `impresion`
--

DROP TABLE IF EXISTS `impresion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `impresion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_programada` datetime NOT NULL,
  `estado` varchar(20) NOT NULL,
  `numero_copias` int NOT NULL,
  `documento_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `documento_id` (`documento_id`),
  KEY `ix_impresion_id` (`id`),
  CONSTRAINT `impresion_ibfk_1` FOREIGN KEY (`documento_id`) REFERENCES `documento` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `impresion`
--

LOCK TABLES `impresion` WRITE;
/*!40000 ALTER TABLE `impresion` DISABLE KEYS */;
/*!40000 ALTER TABLE `impresion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pago`
--

DROP TABLE IF EXISTS `pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pago` (
  `id` int NOT NULL AUTO_INCREMENT,
  `monto` float NOT NULL,
  `fecha_pago` datetime NOT NULL,
  `metodo` varchar(20) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `ix_pago_id` (`id`),
  CONSTRAINT `pago_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pago`
--

LOCK TABLES `pago` WRITE;
/*!40000 ALTER TABLE `pago` DISABLE KEYS */;
/*!40000 ALTER TABLE `pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plantilla`
--

DROP TABLE IF EXISTS `plantilla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plantilla` (
  `id` int NOT NULL AUTO_INCREMENT,
  `numero_version` varchar(100) NOT NULL,
  `contenido` text NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `documento_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `documento_id` (`documento_id`),
  KEY `ix_plantilla_id` (`id`),
  CONSTRAINT `plantilla_ibfk_1` FOREIGN KEY (`documento_id`) REFERENCES `documento` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plantilla`
--

LOCK TABLES `plantilla` WRITE;
/*!40000 ALTER TABLE `plantilla` DISABLE KEYS */;
/*!40000 ALTER TABLE `plantilla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(120) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `saldo` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_usuario_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `versioncontrol`
--

DROP TABLE IF EXISTS `versioncontrol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `versioncontrol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `version` varchar(20) NOT NULL,
  `fecha_version` datetime NOT NULL,
  `comentario` text,
  `documento_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `documento_id` (`documento_id`),
  KEY `ix_versioncontrol_id` (`id`),
  CONSTRAINT `versioncontrol_ibfk_1` FOREIGN KEY (`documento_id`) REFERENCES `documento` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `versioncontrol`
--

LOCK TABLES `versioncontrol` WRITE;
/*!40000 ALTER TABLE `versioncontrol` DISABLE KEYS */;
/*!40000 ALTER TABLE `versioncontrol` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-25  3:28:25
