--Base de datos del Sistema AsistOK--
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema SistemaMC
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema SistemaMC
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `SistemaMC` DEFAULT CHARACTER SET utf8 ;
USE `SistemaMC` ;

-- -----------------------------------------------------
-- Table `SistemaMC`.`horarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`horarios` (
  `id_horario` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(100) NOT NULL,
  `entrada_manana` TIME NOT NULL,
  `salida_manana` TIME NOT NULL,
  `tolerancia_manana` TIME NOT NULL,
  `entrada_tarde` TIME NOT NULL,
  `salida_tarde` TIME NOT NULL,
  `tolerancia_tarde` TIME NOT NULL,
  `activo` TINYINT NOT NULL,
  PRIMARY KEY (`id_horario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SistemaMC`.`departamentos`
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
-- Table `SistemaMC`.`empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`empleado` (
  `id_empleado` INT NOT NULL AUTO_INCREMENT,
  `nombre_empleado` VARCHAR(50) CHARACTER SET 'armscii8' NOT NULL,
  `activo` TINYINT NOT NULL,
  `FK_departamento` INT NOT NULL,
  PRIMARY KEY (`id_empleado`),
  INDEX `FK_Departamento_idx` (`FK_departamento` ASC),
  CONSTRAINT `FK_Departamento`
    FOREIGN KEY (`FK_departamento`)
    REFERENCES `SistemaMC`.`departamentos` (`id_departamento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SistemaMC`.`dispositivos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`dispositivos` (
  `id_dispositivo` INT NOT NULL AUTO_INCREMENT,
  `descripcion_dispositivo` VARCHAR(100) NOT NULL,
  `nombre_dispositivo` VARCHAR(50) NOT NULL,
  `activo` TINYINT NOT NULL,
  `puerto` VARCHAR(45) NOT NULL,
  `IP_dispositivo` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_dispositivo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SistemaMC`.`marcados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`marcados` (
  `id_marcacion` INT NOT NULL AUTO_INCREMENT,
  `marcacion` TIMESTAMP NOT NULL,
  `tipo` VARCHAR(50) NOT NULL,
  `detalle` VARCHAR(45) NULL,
  `horas_trabajadas` TIME NULL,
  `FK_empleado` INT NOT NULL,
  `FK_dispositivos` INT NOT NULL,
  PRIMARY KEY (`id_marcacion`),
  INDEX `FK_Empleado_idx` (`FK_empleado`),
  INDEX `FK_dispositivos_idx` (`FK_dispositivos`),
  CONSTRAINT `FK_Empleado`
    FOREIGN KEY (`FK_empleado`)
    REFERENCES `SistemaMC`.`empleado` (`id_empleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_dispositivos`
    FOREIGN KEY (`FK_dispositivos`)
    REFERENCES `SistemaMC`.`dispositivos` (`id_dispositivo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SistemaMC`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SistemaMC`.`usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nombre_usuario` VARCHAR(50) NOT NULL,
  `password_usuario` VARCHAR(255) NOT NULL,
  `activo` TINYINT NOT NULL,
  `rol` TINYINT NULL,
  PRIMARY KEY (`id_usuario`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
