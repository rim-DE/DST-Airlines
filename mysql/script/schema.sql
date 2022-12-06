
CREATE DATABASE IF NOT EXISTS `dstairlines` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE dstairlines;
-- dstairlines.aeroports definition

CREATE TABLE IF NOT EXISTS `dstairlines`.`aeroports` (
  `iCAO` varchar(100) DEFAULT NULL,
  `IATA` varchar(100) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `taille` varchar(100) DEFAULT NULL,
  `pays` varchar(100) DEFAULT NULL,
  `ville` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`IATA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- dstairlines.compagnies definition

CREATE TABLE IF NOT EXISTS `compagnies` (
  `icao24` varchar(100) NOT NULL,
  `registration` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `manufacturericao` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `manufacturername` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `model` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `serialnumber` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `ownername` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`icao24`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




