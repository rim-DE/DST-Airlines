CREATE DATABASE `dstairlines` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

-- dstairlines.aeroports definition

CREATE TABLE dstairlines.aeroports (
	iCAO varchar(100) NULL,
	IATA varchar(100) NOT NULL,
	nom varchar(100) NULL,
	taille varchar(100) NULL,
	pays varchar(100) NULL,
	ville varchar(100) NULL,
	CONSTRAINT aeroports_PK PRIMARY KEY (IATA)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

