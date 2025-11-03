-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: mysql-yusurus.alwaysdata.net    Database: yusurus_enviar_email
-- ------------------------------------------------------
-- Server version	5.5.5-10.11.14-MariaDB

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
-- Table structure for table `Eventos`
--

DROP TABLE IF EXISTS `Eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Eventos` (
  `idEvento` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`idEvento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Eventos`
--

LOCK TABLES `Eventos` WRITE;
/*!40000 ALTER TABLE `Eventos` DISABLE KEYS */;
/*!40000 ALTER TABLE `Eventos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Log_perticipantesNotificados`
--

DROP TABLE IF EXISTS `Log_perticipantesNotificados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Log_perticipantesNotificados` (
  `idLog_perticipanteNotificado` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `fecha` datetime NOT NULL,
  `estadoAnterior` varchar(45) NOT NULL,
  `estadoDespues` varchar(45) NOT NULL,
  PRIMARY KEY (`idLog_perticipanteNotificado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Log_perticipantesNotificados`
--

LOCK TABLES `Log_perticipantesNotificados` WRITE;
/*!40000 ALTER TABLE `Log_perticipantesNotificados` DISABLE KEYS */;
/*!40000 ALTER TABLE `Log_perticipantesNotificados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Perticipantes`
--

DROP TABLE IF EXISTS `Perticipantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Perticipantes` (
  `idPerticipante` int(11) NOT NULL AUTO_INCREMENT,
  `nombresCompleto` varchar(60) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `estadoNotificado` enum('si','no') NOT NULL,
  `fk_idEvento` int(11) NOT NULL,
  PRIMARY KEY (`idPerticipante`),
  KEY `fk_Perticipantes_Eventos_idx` (`fk_idEvento`),
  CONSTRAINT `fk_Perticipantes_Eventos` FOREIGN KEY (`fk_idEvento`) REFERENCES `Eventos` (`idEvento`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Perticipantes`
--

LOCK TABLES `Perticipantes` WRITE;
/*!40000 ALTER TABLE `Perticipantes` DISABLE KEYS */;
/*!40000 ALTER TABLE `Perticipantes` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`yusurus_sms`@`%`*/ /*!50003 TRIGGER tr_auditoria_notificacion
AFTER UPDATE ON yusurus_enviar_email.Perticipantes
FOR EACH ROW
BEGIN
    -- Solo registrar si cambió el estado de notificación
    IF OLD.estadoNotificado != NEW.estadoNotificado THEN
        INSERT INTO yusurus_enviar_email.Log_perticipantesNotificados (
            idLog_perticipanteNotificado,
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
-- Temporary view structure for view `v_eventos_resumen`
--

DROP TABLE IF EXISTS `v_eventos_resumen`;
/*!50001 DROP VIEW IF EXISTS `v_eventos_resumen`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_eventos_resumen` AS SELECT 
 1 AS `idEvento`,
 1 AS `nombreEvento`,
 1 AS `fechaEvento`,
 1 AS `totalParticipantes`,
 1 AS `notificados`,
 1 AS `pendientes`,
 1 AS `porcentajeNotificado`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_historial_notificaciones`
--

DROP TABLE IF EXISTS `v_historial_notificaciones`;
/*!50001 DROP VIEW IF EXISTS `v_historial_notificaciones`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_historial_notificaciones` AS SELECT 
 1 AS `idLog_perticipanteNotificado`,
 1 AS `nombre`,
 1 AS `correo`,
 1 AS `fechaNotificacion`,
 1 AS `estadoAnterior`,
 1 AS `estadoDespues`,
 1 AS `fechaFormateada`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_participantes_pendientes`
--

DROP TABLE IF EXISTS `v_participantes_pendientes`;
/*!50001 DROP VIEW IF EXISTS `v_participantes_pendientes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_participantes_pendientes` AS SELECT 
 1 AS `idPerticipante`,
 1 AS `nombresCompleto`,
 1 AS `correo`,
 1 AS `nombreEvento`,
 1 AS `fechaEvento`,
 1 AS `diasRestantes`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'yusurus_enviar_email'
--

--
-- Dumping routines for database 'yusurus_enviar_email'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_crear_evento` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`yusurus_sms`@`%` PROCEDURE `sp_crear_evento`(
    IN p_nombre VARCHAR(45),
    IN p_fecha DATE
)
BEGIN
    DECLARE v_mensaje VARCHAR(100);
    
    -- Validar que la fecha no sea pasada
    IF p_fecha < CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha del evento no puede ser anterior a hoy';
    END IF;
    
    INSERT INTO yusurus_enviar_email.Eventos (nombre, fecha)
    VALUES (p_nombre, p_fecha);
    
    SELECT CONCAT('Evento "', p_nombre, '" creado exitosamente con ID: ', LAST_INSERT_ID()) AS mensaje;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_estadisticas_generales` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`yusurus_sms`@`%` PROCEDURE `sp_estadisticas_generales`()
BEGIN
    SELECT 
        (SELECT COUNT(*) FROM yusurus_enviar_email.Eventos) AS totalEventos,
        (SELECT COUNT(*) FROM yusurus_enviar_email.Eventos WHERE fecha >= CURDATE()) AS eventosProximos,
        (SELECT COUNT(*) FROM yusurus_enviar_email.Perticipantes) AS totalParticipantes,
        (SELECT COUNT(*) FROM yusurus_enviar_email.Perticipantes WHERE estadoNotificado = 'si') AS participantesNotificados,
        (SELECT COUNT(*) FROM yusurus_enviar_email.Perticipantes WHERE estadoNotificado = 'no') AS participantesPendientes,
        (SELECT COUNT(*) FROM yusurus_enviar_email.Log_perticipantesNotificados) AS totalNotificacionesEnviadas;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_marcar_notificado` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`yusurus_sms`@`%` PROCEDURE `sp_marcar_notificado`(
    IN p_idParticipante INT
)
BEGIN
    DECLARE v_existe INT;
    DECLARE v_estado_actual VARCHAR(10);
    
    -- Validar que el participante existe
    SELECT COUNT(*), estadoNotificado INTO v_existe, v_estado_actual
    FROM yusurus_enviar_email.Perticipantes
    WHERE idPerticipante = p_idParticipante;
    
    IF v_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El participante especificado no existe';
    END IF;
    
    IF v_estado_actual = 'si' THEN
        SELECT 'El participante ya fue notificado anteriormente' AS mensaje;
    ELSE
        UPDATE yusurus_enviar_email.Perticipantes
        SET estadoNotificado = 'si'
        WHERE idPerticipante = p_idParticipante;
        
        SELECT 'Participante marcado como notificado exitosamente' AS mensaje;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_notificar_evento_completo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`yusurus_sms`@`%` PROCEDURE `sp_notificar_evento_completo`(
    IN p_idEvento INT
)
BEGIN
    DECLARE v_notificados INT;
    
    UPDATE yusurus_enviar_email.Perticipantes
    SET estadoNotificado = 'si'
    WHERE fk_idEvento = p_idEvento 
    AND estadoNotificado = 'no';
    
    SET v_notificados = ROW_COUNT();
    
    SELECT CONCAT(v_notificados, ' participante(s) notificado(s) exitosamente') AS mensaje;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_obtener_participantes_evento` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`yusurus_sms`@`%` PROCEDURE `sp_obtener_participantes_evento`(
    IN p_idEvento INT
)
BEGIN
    SELECT 
        p.idPerticipante,
        p.nombresCompleto,
        p.correo,
        p.estadoNotificado,
        e.nombre AS nombreEvento,
        e.fecha AS fechaEvento
    FROM yusurus_enviar_email.Perticipantes p
    INNER JOIN yusurus_enviar_email.Eventos e ON p.fk_idEvento = e.idEvento
    WHERE p.fk_idEvento = p_idEvento
    ORDER BY p.estadoNotificado ASC, p.nombresCompleto ASC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_registrar_participante` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`yusurus_sms`@`%` PROCEDURE `sp_registrar_participante`(
    IN p_nombreCompleto VARCHAR(60),
    IN p_correo VARCHAR(45),
    IN p_idEvento INT
)
BEGIN
    DECLARE v_existe_evento INT;
    DECLARE v_existe_correo INT;
    
    -- Validar que el evento existe
    SELECT COUNT(*) INTO v_existe_evento
    FROM yusurus_enviar_email.Eventos
    WHERE idEvento = p_idEvento;
    
    IF v_existe_evento = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El evento especificado no existe';
    END IF;
    
    -- Verificar si el correo ya está registrado para este evento
    SELECT COUNT(*) INTO v_existe_correo
    FROM yusurus_enviar_email.Perticipantes
    WHERE correo = p_correo AND fk_idEvento = p_idEvento;
    
    IF v_existe_correo > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Este correo ya está registrado para el evento';
    END IF;
    
    INSERT INTO yusurus_enviar_email.Perticipantes (nombresCompleto, correo, estadoNotificado, fk_idEvento)
    VALUES (p_nombreCompleto, p_correo, 'no', p_idEvento);
    
    SELECT CONCAT('Participante registrado exitosamente con ID: ', LAST_INSERT_ID()) AS mensaje;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_reporte_notificaciones_periodo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`yusurus_sms`@`%` PROCEDURE `sp_reporte_notificaciones_periodo`(
    IN p_fecha_inicio DATETIME,
    IN p_fecha_fin DATETIME
)
BEGIN
    SELECT 
        DATE(fecha) AS fecha,
        COUNT(*) AS totalNotificaciones,
        COUNT(DISTINCT correo) AS participantesUnicos
    FROM yusurus_enviar_email.Log_perticipantesNotificados
    WHERE fecha BETWEEN p_fecha_inicio AND p_fecha_fin
    AND estadoDespues = 'si'
    GROUP BY DATE(fecha)
    ORDER BY fecha DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `v_eventos_resumen`
--

/*!50001 DROP VIEW IF EXISTS `v_eventos_resumen`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`yusurus_sms`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `v_eventos_resumen` AS select `e`.`idEvento` AS `idEvento`,`e`.`nombre` AS `nombreEvento`,`e`.`fecha` AS `fechaEvento`,count(`p`.`idPerticipante`) AS `totalParticipantes`,sum(case when `p`.`estadoNotificado` = 'si' then 1 else 0 end) AS `notificados`,sum(case when `p`.`estadoNotificado` = 'no' then 1 else 0 end) AS `pendientes`,concat(round(sum(case when `p`.`estadoNotificado` = 'si' then 1 else 0 end) / count(`p`.`idPerticipante`) * 100,2),'%') AS `porcentajeNotificado` from (`Eventos` `e` left join `Perticipantes` `p` on(`e`.`idEvento` = `p`.`fk_idEvento`)) group by `e`.`idEvento`,`e`.`nombre`,`e`.`fecha` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_historial_notificaciones`
--

/*!50001 DROP VIEW IF EXISTS `v_historial_notificaciones`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`yusurus_sms`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `v_historial_notificaciones` AS select `l`.`idLog_perticipanteNotificado` AS `idLog_perticipanteNotificado`,`l`.`nombre` AS `nombre`,`l`.`correo` AS `correo`,`l`.`fecha` AS `fechaNotificacion`,`l`.`estadoAnterior` AS `estadoAnterior`,`l`.`estadoDespues` AS `estadoDespues`,date_format(`l`.`fecha`,'%d/%m/%Y %H:%i:%s') AS `fechaFormateada` from `Log_perticipantesNotificados` `l` order by `l`.`fecha` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_participantes_pendientes`
--

/*!50001 DROP VIEW IF EXISTS `v_participantes_pendientes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`yusurus_sms`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `v_participantes_pendientes` AS select `p`.`idPerticipante` AS `idPerticipante`,`p`.`nombresCompleto` AS `nombresCompleto`,`p`.`correo` AS `correo`,`e`.`nombre` AS `nombreEvento`,`e`.`fecha` AS `fechaEvento`,to_days(`e`.`fecha`) - to_days(curdate()) AS `diasRestantes` from (`Perticipantes` `p` join `Eventos` `e` on(`p`.`fk_idEvento` = `e`.`idEvento`)) where `p`.`estadoNotificado` = 'no' order by `e`.`fecha` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-03 12:08:56
