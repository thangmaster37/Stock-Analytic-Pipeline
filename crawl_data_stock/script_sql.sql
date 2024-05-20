SELECT * FROM stock;

DROP TABLE stock;

TRUNCATE stock;

CREATE TABLE IF NOT EXISTS stock(
    code VARCHAR(5) PRIMARY KEY,
    reference_price FLOAT(2),
    celling_price FLOAT(2),
    floor_price FLOAT(2),
    price FLOAT(2),
    volume FLOAT(2),
    total_volume FLOAT(2),
    total_value BIGINT,
    highest_price FLOAT(2),
    lowest_price FLOAT(2),
    average_price FLOAT(2),
    created_at DATETIME,
    updated_at DATETIME
);

CREATE TABLE `vnindex`.`stock` (
  `code` VARCHAR(5) NOT NULL,
  `reference_price` FLOAT(2) NULL,
  `celling_price` FLOAT(2) NULL,
  `floor_price` FLOAT(2) NULL,
  `price` FLOAT(2) NULL,
  `volume` FLOAT(2) NULL,
  `total_volume` FLOAT(2) NULL,
  `total_value` BIGINT NULL,
  `highest_price` FLOAT(2) NULL,
  `lowest_price` FLOAT(2) NULL,
  `average_price` FLOAT(2) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`code`));