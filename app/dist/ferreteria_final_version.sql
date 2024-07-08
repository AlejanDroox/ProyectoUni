CREATE DATABASE  IF NOT EXISTS `dbferreteria` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dbferreteria`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: dbferreteria
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `datos_cliente`
--

DROP TABLE IF EXISTS `datos_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_cliente` (
  `idDatos_cliente` int NOT NULL,
  `Nom_cliente` varchar(45) DEFAULT NULL,
  `Apellido_cliente` varchar(45) DEFAULT NULL,
  `Apellido2_cliente` varchar(45) DEFAULT NULL,
  `CI` int NOT NULL,
  `Telf_cliente` varchar(45) NOT NULL,
  `Estado_cl` varchar(45) DEFAULT NULL,
  `municipio` varchar(45) DEFAULT NULL,
  `parroquia_cl` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idDatos_cliente`),
  UNIQUE KEY `idDatos_cliente_UNIQUE` (`idDatos_cliente`),
  UNIQUE KEY `CI_UNIQUE` (`CI`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_cliente`
--

LOCK TABLES `datos_cliente` WRITE;
/*!40000 ALTER TABLE `datos_cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `datos_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_clientes`
--

DROP TABLE IF EXISTS `datos_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre_cliente` varchar(255) NOT NULL,
  `numero_identificacion` varchar(50) NOT NULL,
  `telefono` int DEFAULT NULL,
  PRIMARY KEY (`id_cliente`),
  KEY `ix_datos_clientes_id_cliente` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_clientes`
--

LOCK TABLES `datos_clientes` WRITE;
/*!40000 ALTER TABLE `datos_clientes` DISABLE KEYS */;
INSERT INTO `datos_clientes` VALUES (1,'pedro','12344',123),(2,'juan','12345',214),(3,'pedro','1',NULL),(4,'pedro','471234',NULL),(5,'pedro','25789335',NULL),(6,'hola','123456',NULL),(7,'a','12346',1),(8,'a','1234566',3),(9,'a','',12);
/*!40000 ALTER TABLE `datos_clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados` (
  `idEmpleados` int NOT NULL AUTO_INCREMENT,
  `Nom_empleado` varchar(45) DEFAULT NULL,
  `Apellido_empleado` varchar(45) DEFAULT NULL,
  `Apellido2_empleado` varchar(45) DEFAULT NULL,
  `Telefono` int DEFAULT NULL,
  `Local_idLocal` int NOT NULL,
  `Datos_cliente_idDatos_cliente` int NOT NULL,
  PRIMARY KEY (`idEmpleados`),
  UNIQUE KEY `idEmpleados_UNIQUE` (`idEmpleados`),
  KEY `fk_Empleados_Local1_idx` (`Local_idLocal`),
  KEY `fk_Empleados_Datos_cliente1_idx` (`Datos_cliente_idDatos_cliente`),
  CONSTRAINT `fk_Empleados_Datos_cliente1` FOREIGN KEY (`Datos_cliente_idDatos_cliente`) REFERENCES `datos_cliente` (`idDatos_cliente`),
  CONSTRAINT `fk_Empleados_Local1` FOREIGN KEY (`Local_idLocal`) REFERENCES `local` (`idLocal`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados`
--

LOCK TABLES `empleados` WRITE;
/*!40000 ALTER TABLE `empleados` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `local`
--

DROP TABLE IF EXISTS `local`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `local` (
  `idLocal` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(45) NOT NULL,
  `Estado_lc` varchar(45) NOT NULL,
  `municipio` varchar(45) NOT NULL,
  `parroquia_Lc` varchar(45) NOT NULL,
  `RIF` varchar(45) NOT NULL,
  PRIMARY KEY (`idLocal`),
  UNIQUE KEY `RIF_UNIQUE` (`RIF`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `local`
--

LOCK TABLES `local` WRITE;
/*!40000 ALTER TABLE `local` DISABLE KEYS */;
/*!40000 ALTER TABLE `local` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nom_producto` varchar(255) DEFAULT NULL,
  `Existencia` int NOT NULL,
  `Desc_Producto` text,
  `Valor_Producto_C` decimal(10,2) NOT NULL,
  `Valor_Producto_V` decimal(10,2) NOT NULL,
  `Proveedor` text,
  `Image` text,
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `ix_productos_nom_producto` (`nom_producto`),
  KEY `ix_productos_id_producto` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Tornillos Para Madera',36,'Longitud: 1/2 pulgada. Diámetro: 1/8 pulgada',30.00,30.00,'STANLEY','assets/productos/Tornillo para Madera.jpg'),(12,'Pala Cudrada.',8,'Medida: 12 pulgadas (30.5 cm)',490.00,490.00,'MADECO','assets/productos/Pala Cuadrada.jpg'),(13,'Palustre para Albañilería',12,'Medida: 10 pulgadas (25.4 cm)',180.00,180.00,NULL,'app/assets/productos/Palustre.jpg'),(15,'Llana para lisa',15,'Medida: 10 pulgadas (25.4 cm)',180.00,180.00,NULL,'app/assets/productos/LLana de Lisa.jpg'),(16,'Taladro de mano Recargable',15,'batería recargable de iones de litio de 18V. Ofrece una autonomía de hasta 2 horas de uso continuo. Tiempo de carga de la batería: 1 hora',950.00,950.00,NULL,'app/assets/productos/LLana de Lisa.jpg'),(17,'Taladro de Cable Stanley',25,'con cable de alimentación de 110V. Potente motor de 750W para trabajos pesados. Incluye mandril de 1/2 pulgada y tope de profundidad ajustable.',350.00,350.00,NULL,'app/assets/productos/Taladro de cable.jpg'),(18,'Tuvos PVC',84,'Medida: 1/2 pulgada (12.7 mm)\nSe vende por metro',25.00,25.00,NULL,'app/assets/productos/Tubos PVC.jpg'),(19,'de Estria',20,'Medida: 1/2 pulgada (12.7 mm)\nSe vende por metro',120.00,120.00,NULL,'app/assets/productos/Destornillador de Estria.jpg'),(20,'Ponchadora Truper',8,'Para hacer orificios y colocar remaches en cinturones, correas, cuero y materiales similares.',350.00,350.00,NULL,'app/assets/productos/Ponchadora.jpg'),(21,'Pala Cuadrada',3,'Medida: 12 pulgadas (30.5 cm)',2.00,2.00,NULL,'assets/productos/agregar_imagen.png'),(22,'a',3,'a',2.00,2.00,NULL,'assets/productos/Captura de pantalla 2024-06-27 102435.png'),(23,'Tornillos Para Madera.',46,'Longitud: 1/2 pulgada. Diámetro: 1/8 pulgada.',30.00,30.00,NULL,'app\\assets\\productos\\agregar_imagen.png');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `Id_provedor` int NOT NULL AUTO_INCREMENT,
  `Nom_proveedor` varchar(45) NOT NULL,
  `Telf_proveedor` int NOT NULL,
  PRIMARY KEY (`Id_provedor`),
  UNIQUE KEY `Nom_proveedor_UNIQUE` (`Nom_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `idUsers` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `contrasena` varchar(200) NOT NULL,
  `Status` tinyint NOT NULL DEFAULT '1',
  `Rol` varchar(45) NOT NULL,
  PRIMARY KEY (`idUsers`),
  UNIQUE KEY `idUsers_UNIQUE` (`idUsers`),
  UNIQUE KEY `Username_UNIQUE` (`username`),
  UNIQUE KEY `Userscol_UNIQUE` (`contrasena`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$12$5AMCfyLS8eHCwiYb0V7UfuBQG2yTns/UPVjQCyOCB3qtj2anzijXq',1,'administrador'),(11,'admin2','$2b$12$vMSouOSihrCPzKTUpW1oVusmFxC5e.PmEPJgBUhHbRqyPYshu5pZa',1,'administrador'),(19,'juan','$2b$12$MIlXDjht/xkk4/kfJwfMVO0FOgJ14pbVJyxgbtXfIA.ftGWs0L2Z6',1,'empleado'),(20,'damin','$2b$12$OcRr3b1ZopQG7wtoXGT7C.TSC5aWQPWAwgUrMT24zIHmeiFlIw8ey',1,'gerente');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `idVentas` int NOT NULL AUTO_INCREMENT,
  `Fecha_Venta` datetime DEFAULT NULL,
  `Monto_venta` decimal(10,2) NOT NULL,
  `Desc_compra` text,
  `cantidad` int NOT NULL,
  `Metodo` enum('BS','COP','USD') NOT NULL,
  `id_Datos_Cliente` int DEFAULT NULL,
  PRIMARY KEY (`idVentas`),
  KEY `ix_ventas_idVentas` (`idVentas`),
  KEY `fk_ventas_datos_cliente` (`id_Datos_Cliente`),
  CONSTRAINT `fk_ventas_datos_cliente` FOREIGN KEY (`id_Datos_Cliente`) REFERENCES `datos_clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (3,'2024-06-30 00:00:00',490.00,'Pala Cudrada',1,'COP',1),(4,'2024-07-01 00:00:00',1030.00,'Palustre para Albañilería, Pala Cudrada',4,'BS',2),(5,'2024-07-07 00:00:00',60.00,'Tornillos Para Madera',2,'USD',8),(6,'2024-07-07 00:00:00',60.00,'Tornillos Para Madera',2,'COP',8);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_productos`
--

DROP TABLE IF EXISTS `ventas_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ventas_idventas1` int DEFAULT NULL,
  `productos_idproductos1` int DEFAULT NULL,
  `Users_idUsers` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  `grupo` int NOT NULL,
  `cliente_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ventas_idventas1` (`ventas_idventas1`),
  KEY `productos_idproductos1` (`productos_idproductos1`),
  KEY `Users_idUsers` (`Users_idUsers`),
  KEY `cliente_id` (`cliente_id`),
  KEY `ix_ventas_productos_id` (`id`),
  CONSTRAINT `ventas_productos_ibfk_1` FOREIGN KEY (`ventas_idventas1`) REFERENCES `ventas` (`idVentas`),
  CONSTRAINT `ventas_productos_ibfk_2` FOREIGN KEY (`productos_idproductos1`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `ventas_productos_ibfk_3` FOREIGN KEY (`Users_idUsers`) REFERENCES `users` (`idUsers`),
  CONSTRAINT `ventas_productos_ibfk_4` FOREIGN KEY (`cliente_id`) REFERENCES `datos_clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_productos`
--

LOCK TABLES `ventas_productos` WRITE;
/*!40000 ALTER TABLE `ventas_productos` DISABLE KEYS */;
INSERT INTO `ventas_productos` VALUES (4,3,12,11,1,1,4),(5,4,13,11,3,2,5),(6,4,12,11,1,2,5),(7,5,1,11,2,3,8),(8,6,1,11,2,4,8);
/*!40000 ALTER TABLE `ventas_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'dbferreteria'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-07 21:32:47
