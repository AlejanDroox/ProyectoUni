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
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `idCliente` int NOT NULL,
  `Datos_cliente_idDatos_cliente` int NOT NULL,
  PRIMARY KEY (`idCliente`),
  UNIQUE KEY `idCliente_UNIQUE` (`idCliente`),
  KEY `fk_Cliente_Datos_cliente1_idx` (`Datos_cliente_idDatos_cliente`),
  CONSTRAINT `fk_Cliente_Datos_cliente1` FOREIGN KEY (`Datos_cliente_idDatos_cliente`) REFERENCES `datos_cliente` (`idDatos_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

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
  PRIMARY KEY (`id_cliente`),
  KEY `ix_datos_clientes_id_cliente` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_clientes`
--

LOCK TABLES `datos_clientes` WRITE;
/*!40000 ALTER TABLE `datos_clientes` DISABLE KEYS */;
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
  `Image` text,
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `ix_productos_nom_producto` (`nom_producto`),
  KEY `ix_productos_id_producto` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$12$5AMCfyLS8eHCwiYb0V7UfuBQG2yTns/UPVjQCyOCB3qtj2anzijXq',1,'administrador'),(11,'admin2','$2b$12$vMSouOSihrCPzKTUpW1oVusmFxC5e.PmEPJgBUhHbRqyPYshu5pZa',1,'administrador');
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
  PRIMARY KEY (`idVentas`),
  KEY `ix_ventas_idVentas` (`idVentas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_productos`
--

LOCK TABLES `ventas_productos` WRITE;
/*!40000 ALTER TABLE `ventas_productos` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas_productos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-28 12:43:14
