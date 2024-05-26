CREATE DATABASE  IF NOT EXISTS `dbferreteria` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dbferreteria`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dbferreteria
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
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `idCategoria` int NOT NULL AUTO_INCREMENT,
  `desc_Categoria` varchar(100) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  PRIMARY KEY (`idCategoria`),
  UNIQUE KEY `idCategoria_UNIQUE` (`idCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'lo que sea man','lol lmao');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

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
  `id_Productos` int NOT NULL AUTO_INCREMENT,
  `nom_Producto` varchar(45) NOT NULL,
  `Existencia` int NOT NULL,
  `Desc_Producto` varchar(100) NOT NULL,
  `Valor_Producto` double NOT NULL,
  `Marca` varchar(30) NOT NULL,
  `Categoria_idCategoria` int DEFAULT NULL,
  `Proveedor_Id_provedor` int DEFAULT NULL,
  `Users_idUsers` int DEFAULT NULL,
  PRIMARY KEY (`id_Productos`),
  UNIQUE KEY `idProductos_UNIQUE` (`id_Productos`),
  UNIQUE KEY `nom_Producto_UNIQUE` (`nom_Producto`),
  KEY `fk_Productos_Categoria_idx` (`Categoria_idCategoria`),
  KEY `fk_Productos_Proveedor1_idx` (`Proveedor_Id_provedor`),
  KEY `fk_Productos_Users1_idx` (`Users_idUsers`),
  CONSTRAINT `fk_Productos_Categoria` FOREIGN KEY (`Categoria_idCategoria`) REFERENCES `categoria` (`idCategoria`),
  CONSTRAINT `fk_Productos_Proveedor1` FOREIGN KEY (`Proveedor_Id_provedor`) REFERENCES `proveedor` (`Id_provedor`),
  CONSTRAINT `fk_Productos_Users1` FOREIGN KEY (`Users_idUsers`) REFERENCES `users` (`idUsers`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Tornillos',10,'xd',15,'?',NULL,NULL,NULL),(6,'Tornillos4',100,'xd',20,'?',1,1,NULL);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_ventas`
--

DROP TABLE IF EXISTS `productos_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_ventas` (
  `Ventas_idVentas` int NOT NULL,
  `Productos_id_Productos` int NOT NULL,
  KEY `fk_Productos_Ventas_Ventas1_idx` (`Ventas_idVentas`),
  KEY `fk_Productos_Ventas_Productos1_idx` (`Productos_id_Productos`),
  CONSTRAINT `fk_Productos_Ventas_Productos1` FOREIGN KEY (`Productos_id_Productos`) REFERENCES `productos` (`id_Productos`),
  CONSTRAINT `fk_Productos_Ventas_Ventas1` FOREIGN KEY (`Ventas_idVentas`) REFERENCES `ventas` (`idVentas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_ventas`
--

LOCK TABLES `productos_ventas` WRITE;
/*!40000 ALTER TABLE `productos_ventas` DISABLE KEYS */;
/*!40000 ALTER TABLE `productos_ventas` ENABLE KEYS */;
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
INSERT INTO `proveedor` VALUES (1,'YO',424737724);
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'yosnelaaaaaaaaaaaaaa','$2b$12$uf9h1okutBRHRzUSuewsGe1V0T7/c/nMJZlfijzVbu88b3LU5qRDq',1,''),(3,'AAAAAAAAyosnelaaaaaaaaaaaaaa','$2b$12$3yB4ZUn8dYW.XtWlPUql.el.XvWu/unAM97X0t9D4O3301hGhJxbG',1,''),(5,'azael','$2a$12$5AMCfyLS8eHCwiYb0V7UfuBQG2yTns/UPVjQCyOCB3qtj2anzijXq',1,'administrador'),(7,'nuevo_usuario','$2b$12$POZQhzJs971w206NKOQd3.a7WUxfrqhPfdarhdDRDzJtqKjURBhHK',1,'empleado'),(8,'nuevo_usuario2','$2b$12$1i42h4VMsh3b98G0iWK.jew816cdcFpqR.ntij.MPdoe2qA56c8Si',1,'empleado'),(9,'nuevo_usuario1','$2b$12$Y3VzwVModRZ.0PoyStNj1u3Jc.Dw4gsQ5fQvSD.WSNs.D/wALltCS',1,'empleado');
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
  `Fecha_Venta` date DEFAULT NULL,
  `Monto_venta` double NOT NULL,
  `Desc_Compra` varchar(100) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `Empleados_idEmpleados` int NOT NULL,
  PRIMARY KEY (`idVentas`),
  KEY `fk_Ventas_Empleados1_idx` (`Empleados_idEmpleados`),
  CONSTRAINT `fk_Ventas_Empleados1` FOREIGN KEY (`Empleados_idEmpleados`) REFERENCES `empleados` (`idEmpleados`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-26 19:12:03
