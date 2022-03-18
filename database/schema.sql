
USE db;
/* Валюты, которыми мы будем оперировать */
CREATE TABLE IF NOT EXISTS currency  (
	id INT NOT NULL AUTO_INCREMENT,
	s_title VARCHAR(50) NOT NULL,
	mark VARCHAR(3) NOT NULL COMMENT 'ISO-4217 currency code',
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 DEFAULT COLLATE=utf8_general_ci;

/* Курс валюты к рублю на определенную дату */
CREATE TABLE IF NOT EXISTS currency_cource (
	currency INT NOT NULL,
	`date` DATE NOT NULL,
	src enum('market', 'cb', 'other') NOT NULL,
	rur_cource DECIMAL(10,6) NOT NULL,
	FOREIGN KEY (currency) 
	  REFERENCES currency(id) 
	  ON UPDATE RESTRICT ON DELETE RESTRICT,
	PRIMARY KEY (currency, `date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 DEFAULT COLLATE=utf8_general_ci;

/* Метрики, которые мы будем собирать */
CREATE TABLE IF NOT EXISTS metrics (
	id INT NOT NULL AUTO_INCREMENT,
	s_title VARCHAR(255) NOT NULL,
	period enum('year', 'month', 'week', 'day', 'other') NOT NULL,
	currency INT NOT NULL,
	last_ok_parse DATETIME,
	last_fail_parse DATETIME,
	s_last_parse_error TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (currency) 
	  REFERENCES currency(id) 
	  ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 DEFAULT COLLATE=utf8_general_ci;

/* Собранные по метрикам данные */
CREATE TABLE IF NOT EXISTS metric (
	id INT NOT NULL AUTO_INCREMENT,
	metric INT NOT NULL,
	date_described DATETIME NOT NULL, /* дата, которую описывают данные */
	date_parsed DATETIME NOT NULL, 	  /* дата, когда данные были фактически выгружены в нашу базу */
	value BIGINT NOT NULL, /* собственно, данные. Пока берём длинное целое, вроде дробей в макроэкономике не держат */
	obsolete bool NOT NULL, /*	false для старых данных, по которым новая выгрузка даёт нам новое значение. При этом старое значение останется
								в БД, но с obsolete = true. */
	PRIMARY KEY (id),
	FOREIGN KEY (metric)
      REFERENCES metrics(id)
      ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 DEFAULT COLLATE=utf8_general_ci;

/*	Иерархия показателей. Строго говоря, это скорей должно принадлежать отчету,
	но с вероятностью ~100% оно от отчета к отчету меняться не будет. */
CREATE TABLE IF NOT EXISTS metrics_hierarchy (
	id INT NOT NULL AUTO_INCREMENT,
	s_title VARCHAR(255) NOT NULL,
	metric INT,
	parent INT,

	PRIMARY KEY (id),
	FOREIGN KEY (metric)
      REFERENCES metrics(id)
      ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 DEFAULT COLLATE=utf8_general_ci;
