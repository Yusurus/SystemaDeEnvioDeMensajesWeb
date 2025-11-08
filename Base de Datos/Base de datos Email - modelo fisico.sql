USE `yusurus_enviar_email`;

CREATE TABLE `Facultades` (
  `idFacultad` INT NOT NULL AUTO_INCREMENT,
  `nombreFacultad` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idFacultad`)
);

CREATE TABLE `Eventos` (
  `idEvento` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `fecha` DATE NOT NULL,
  PRIMARY KEY (`idEvento`)
);

CREATE TABLE `Log_participantesNotificados` (
  `idLog_participanteNotificado` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `correo` VARCHAR(45) NOT NULL,
  `fecha` DATETIME NOT NULL,
  `estadoAnterior` VARCHAR(45) NOT NULL,
  `estadoDespues` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idLog_participanteNotificado`)
);

CREATE TABLE `Escuelas` (
  `idEscuela` INT NOT NULL AUTO_INCREMENT,
  `nombreEscuela` VARCHAR(100) NOT NULL,
  `fk_idFacultad` INT NOT NULL,
  PRIMARY KEY (`idEscuela`),
  KEY `fk_Escuelas_Facultades1_idx` (`fk_idFacultad`),
  CONSTRAINT `fk_Escuelas_Facultades1` FOREIGN KEY (`fk_idFacultad`) REFERENCES `Facultades` (`idFacultad`)
);

CREATE TABLE `Participantes` (
  `idParticipante` INT NOT NULL AUTO_INCREMENT,
  `nombresCompleto` VARCHAR(60) NOT NULL,
  `correo` VARCHAR(45) NOT NULL,
  `estadoNotificado` ENUM('si','no') NOT NULL,
  `fk_idEvento` INT NOT NULL,
  PRIMARY KEY (`idParticipante`),
  KEY `fk_Perticipantes_Eventos1_idx` (`fk_idEvento`),
  CONSTRAINT `fk_Perticipantes_Eventos1` FOREIGN KEY (`fk_idEvento`) REFERENCES `Eventos` (`idEvento`)
);

CREATE TABLE `ParticipantesEscuelas` (
  `fk_idParticipante` INT NOT NULL,
  `fk_idEscuela` INT NOT NULL,
  KEY `fk_ParticipantesEscuelas_Participantes1_idx` (`fk_idParticipante`),
  KEY `fk_ParticipantesEscuelas_Escuelas1_idx` (`fk_idEscuela`),
  CONSTRAINT `fk_ParticipantesEscuelas_Escuelas1` FOREIGN KEY (`fk_idEscuela`) REFERENCES `Escuelas` (`idEscuela`),
  CONSTRAINT `fk_ParticipantesEscuelas_Participantes1` FOREIGN KEY (`fk_idParticipante`) REFERENCES `Participantes` (`idParticipante`)
);

CREATE TABLE `ParticipantesFacultades` (
  `fk_idParticipante` INT NOT NULL,
  `fk_idFacultad` INT NOT NULL,
  KEY `fk_ParticipantesFacultades_Participantes1_idx` (`fk_idParticipante`),
  KEY `fk_ParticipantesFacultades_Facultades1_idx` (`fk_idFacultad`),
  CONSTRAINT `fk_ParticipantesFacultades_Facultades1` FOREIGN KEY (`fk_idFacultad`) REFERENCES `Facultades` (`idFacultad`),
  CONSTRAINT `fk_ParticipantesFacultades_Participantes1` FOREIGN KEY (`fk_idParticipante`) REFERENCES `Participantes` (`idParticipante`)
);

DELIMITER $$
CREATE TRIGGER `tr_auditoria_notificacion` AFTER UPDATE ON `Participantes`
FOR EACH ROW
BEGIN
    -- Solo registrar si cambió el estado de notificación.
    IF OLD.estadoNotificado != NEW.estadoNotificado THEN
        INSERT INTO `Log_participantesNotificados` (
            `idLog_participanteNotificado`,
            `nombre`,
            `correo`,
            `fecha`,
            `estadoAnterior`,
            `estadoDespues`
        )
        VALUES (
            NULL, -- Auto-increment
            NEW.nombresCompleto,
            NEW.correo,
            NOW(),
            OLD.estadoNotificado,
            NEW.estadoNotificado
        );
    END IF;
END$$
DELIMITER ;

INSERT INTO `Facultades` (nombreFacultad) VALUES
('Facultad de Ciencias Agrarias'),
('Facultad de Ingeniería de Minas, Geología y Metalurgia'),
('Facultad de Ingeniería Civil'),
('Facultad de Ingeniería de Industrias Alimentarias'),
('Facultad de Ciencias del Ambiente'),
('Facultad de Economía y Contabilidad'),
('Facultad de Administración y Turismo'),
('Facultad de Ciencias Médicas'),
('Facultad de Medicina Humana'),
('Facultad de Ciencias sociales, Educación y de la Comunicación'),
('Facultad de Ciencias'),
('Facultad de Derecho y Ciencias Políticas');

INSERT INTO `Escuelas` (nombreEscuela, fk_idFacultad) VALUES
('Ingeniería Agrícola',1),
('Agronomía',1),
('Ingeniería de Minas',2),
('Ingeniería Civil',3),
('Arquitectura',3),
('Ingeniería de Industrias Alimentarias',4),
('Ingeniería Industrial',4),
('Ingeniería Ambiental',5),
('Ingeniería Sanitaria',5),
('Economía',6),
('Contabilidad',6),
('Administración',7),
('Turismo',7),
('Enfermería',8),
('Obstetricia',8),
('Medicina Humana (en creación)',9),
('Comunicación Lingüística y Literatura',10),
('Lengua Extranjera: Inglés',10),
('Primaria y Educación Bilingüe Intercultural',10),
('Matemática e Informática',10),
('Ciencias de la Comunicación',10),
('Arqueología',10),
('Matemática',11),
('Estadística e Informática',11),
('Ingeniería de Sistemas e Informática',1),
('Derecho',12);