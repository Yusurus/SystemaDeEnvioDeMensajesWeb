-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: yusurus_enviar_email
-- ------------------------------------------------------
-- Server version	9.4.0

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
-- Table structure for table `escuelas`
--

DROP TABLE IF EXISTS `escuelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `escuelas` (
  `idEscuela` int NOT NULL AUTO_INCREMENT,
  `nombreEscuela` varchar(100) NOT NULL,
  `fk_idFacultad` int NOT NULL,
  PRIMARY KEY (`idEscuela`),
  KEY `fk_Escuelas_Facultades1_idx` (`fk_idFacultad`),
  CONSTRAINT `fk_Escuelas_Facultades1` FOREIGN KEY (`fk_idFacultad`) REFERENCES `facultades` (`idFacultad`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `escuelas`
--

LOCK TABLES `escuelas` WRITE;
/*!40000 ALTER TABLE `escuelas` DISABLE KEYS */;
INSERT INTO `escuelas` VALUES (32,'Ingeniería Agrícola',30),(33,'Agronomía',30),(34,'Ingeniería de Minas',31),(35,'Ingeniería Civil',32),(36,'Arquitectura',32),(37,'Ingeniería de Industrias Alimentarias',33),(38,'Ingeniería Industrial',33),(39,'Ingeniería Ambiental',34),(40,'Ingeniería Sanitaria',34),(41,'Economía',35),(42,'Contabilidad',35),(43,'Administración',36),(44,'Turismo',36),(45,'Enfermería',37),(46,'Obstetricia',37),(47,'Medicina Humana (en creación)',38),(48,'Comunicación Lingüística y Literatura',39),(49,'Lengua Extranjera: Inglés',39),(50,'Primaria y Educación Bilingüe Intercultural',39),(51,'Matemática e Informática',39),(52,'Ciencias de la Comunicación',39),(53,'Arqueología',39),(54,'Matemática',40),(55,'Estadística e Informática',40),(56,'Ingeniería de Sistemas e Informática',40),(57,'Derecho',41);
/*!40000 ALTER TABLE `escuelas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos` (
  `idEvento` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`idEvento`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos`
--

LOCK TABLES `eventos` WRITE;
/*!40000 ALTER TABLE `eventos` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facultades`
--

DROP TABLE IF EXISTS `facultades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facultades` (
  `idFacultad` int NOT NULL AUTO_INCREMENT,
  `nombreFacultad` varchar(100) NOT NULL,
  PRIMARY KEY (`idFacultad`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facultades`
--

LOCK TABLES `facultades` WRITE;
/*!40000 ALTER TABLE `facultades` DISABLE KEYS */;
INSERT INTO `facultades` VALUES (30,'Facultad de Ciencias Agrarias'),(31,'Facultad de Ingeniería de Minas, Geología y Metalurgia'),(32,'Facultad de Ingeniería Civil'),(33,'Facultad de Ingeniería de Industrias Alimentarias'),(34,'Facultad de Ciencias del Ambiente'),(35,'Facultad de Economía y Contabilidad'),(36,'Facultad de Administración y Turismo'),(37,'Facultad de Ciencias Médicas'),(38,'Facultad de Medicina Humana'),(39,'Facultad de Ciencias sociales, Educación y de la Comunicación'),(40,'Facultad de Ciencias'),(41,'Facultad de Derecho y Ciencias Políticas');
/*!40000 ALTER TABLE `facultades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_participantesnotificados`
--

DROP TABLE IF EXISTS `log_participantesnotificados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_participantesnotificados` (
  `idLog_participanteNotificado` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `fecha` datetime NOT NULL,
  `estadoAnterior` varchar(45) NOT NULL,
  `estadoDespues` varchar(45) NOT NULL,
  PRIMARY KEY (`idLog_participanteNotificado`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_participantesnotificados`
--

LOCK TABLES `log_participantesnotificados` WRITE;
/*!40000 ALTER TABLE `log_participantesnotificados` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_participantesnotificados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participantes`
--

DROP TABLE IF EXISTS `participantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participantes` (
  `idParticipante` int NOT NULL AUTO_INCREMENT,
  `nombresCompleto` varchar(60) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `estadoNotificado` enum('si','no') NOT NULL,
  `fk_idEvento` int NOT NULL,
  PRIMARY KEY (`idParticipante`),
  KEY `fk_Perticipantes_Eventos1_idx` (`fk_idEvento`),
  CONSTRAINT `fk_Perticipantes_Eventos1` FOREIGN KEY (`fk_idEvento`) REFERENCES `eventos` (`idEvento`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participantes`
--

LOCK TABLES `participantes` WRITE;
/*!40000 ALTER TABLE `participantes` DISABLE KEYS */;
/*!40000 ALTER TABLE `participantes` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tr_auditoria_notificacion` AFTER UPDATE ON `participantes` FOR EACH ROW BEGIN
    -- Solo registrar si cambió el estado de notificación.
    IF OLD.estadoNotificado != NEW.estadoNotificado THEN
        INSERT INTO yusurus_enviar_email.Log_participantesNotificados (
            idLog_participanteNotificado,
            nombre,
            correo,
            fecha,
            estadoAnterior,
            estadoDespues
        )
        VALUES (
            NULL,  -- Auto-increment
            NEW.nombresCompleto,
            NEW.correo,
            NOW(),
            OLD.estadoNotificado,
            NEW.estadoNotificado
        );
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `participantesescuelas`
--

DROP TABLE IF EXISTS `participantesescuelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participantesescuelas` (
  `fk_idParticipante` int NOT NULL,
  `fk_idEscuela` int NOT NULL,
  KEY `fk_ParticipantesEscuelas_Participantes1_idx` (`fk_idParticipante`),
  KEY `fk_ParticipantesEscuelas_Escuelas1_idx` (`fk_idEscuela`),
  CONSTRAINT `fk_ParticipantesEscuelas_Escuelas1` FOREIGN KEY (`fk_idEscuela`) REFERENCES `escuelas` (`idEscuela`),
  CONSTRAINT `fk_ParticipantesEscuelas_Participantes1` FOREIGN KEY (`fk_idParticipante`) REFERENCES `participantes` (`idParticipante`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participantesescuelas`
--

LOCK TABLES `participantesescuelas` WRITE;
/*!40000 ALTER TABLE `participantesescuelas` DISABLE KEYS */;
/*!40000 ALTER TABLE `participantesescuelas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participantesfacultades`
--

DROP TABLE IF EXISTS `participantesfacultades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participantesfacultades` (
  `fk_idParticipante` int NOT NULL,
  `fk_idFacultad` int NOT NULL,
  KEY `fk_ParticipantesFacultades_Participantes1_idx` (`fk_idParticipante`),
  KEY `fk_ParticipantesFacultades_Facultades1_idx` (`fk_idFacultad`),
  CONSTRAINT `fk_ParticipantesFacultades_Facultades1` FOREIGN KEY (`fk_idFacultad`) REFERENCES `facultades` (`idFacultad`),
  CONSTRAINT `fk_ParticipantesFacultades_Participantes1` FOREIGN KEY (`fk_idParticipante`) REFERENCES `participantes` (`idParticipante`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participantesfacultades`
--

LOCK TABLES `participantesfacultades` WRITE;
/*!40000 ALTER TABLE `participantesfacultades` DISABLE KEYS */;
/*!40000 ALTER TABLE `participantesfacultades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'yusurus_enviar_email'
--

--
-- Dumping routines for database 'yusurus_enviar_email'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-07 16:52:49
