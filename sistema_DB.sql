

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema SistemaMC
-- -----------------------------------------------------

-- -----------------------------------------------------
-- BD SistemaMC
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `SistemaMC` DEFAULT CHARACTER SET utf8 ;
USE `SistemaMC` ;

-- -----------------------------------------------------
-- Tabla horarios
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`horarios` (
  `id_horario` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(100) NOT NULL,
  `entrada` VARCHAR(50) NOT NULL,
  `salida` VARCHAR(50) NOT NULL,
  `tolerancia_minima` TIMESTAMP NULL,
  `tolerancia_maxima` TIMESTAMP NULL,
  `activo` TINYINT NOT NULL,
  PRIMARY KEY (`id_horario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla departamentos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`departamentos` (
  `id_departamento` INT NOT NULL AUTO_INCREMENT,
  `nombre_departamento` VARCHAR(50) NOT NULL,
  `activo` TINYINT NOT NULL,
  `FK_horarios` INT NOT NULL,
  PRIMARY KEY (`id_departamento`),
  INDEX `FK_Horarios_idx` (`FK_horarios`),
  CONSTRAINT `FK_Horarios`
    FOREIGN KEY (`FK_horarios`)
    REFERENCES `SistemaMC`.`horarios` (`id_horario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla empleado
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`empleado` (
  `id_empleado` INT NOT NULL AUTO_INCREMENT,
  `id_empleado_marcador` INT NOT NULL,
  `nombre_empleado` VARCHAR(50) CHARACTER SET 'armscii8' NOT NULL,
  `activo` TINYINT NOT NULL,
  `FK_departamento` INT NOT NULL,
  PRIMARY KEY (`id_empleado`),
  INDEX `FK_Departamento_idx` (`FK_departamento`),
  CONSTRAINT `FK_Departamento`
    FOREIGN KEY (`FK_departamento`)
    REFERENCES `SistemaMC`.`departamentos` (`id_departamento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla marcados
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`marcados` (
  `id_marcacion` INT NOT NULL AUTO_INCREMENT,
  `id_marcador` INT NOT NULL,
  `marcacion` TIMESTAMP NOT NULL,
  `tipo` VARCHAR(50) NOT NULL,
  `FK_empleado` INT NOT NULL,
  PRIMARY KEY (`id_marcacion`),
  INDEX `FK_Empleado_idx` (`FK_empleado`),
  CONSTRAINT `FK_Empleado`
    FOREIGN KEY (`FK_empleado`)
    REFERENCES `SistemaMC`.`empleado` (`id_empleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla usuarios
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nombre_usuario` VARCHAR(50) NOT NULL,
  `password_usuario` VARCHAR(255) NOT NULL,
  `activo` TINYINT NOT NULL,
  PRIMARY KEY (`id_usuario`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
