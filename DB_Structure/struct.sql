
/* Валюты, которыми мы будем оперировать */
create table IF NOT EXISTS currency  (
	id int NOT NULL AUTO_INCREMENT,
	s_title string not null,
	mark string(3) not null,
	PRIMARY KEY (id)
);

/* Курс валюты к рублю на определенную дату */
create table IF NOT EXISTS currency_cource (
	currency int not null,
	`date` date not null,
	src enum('market', 'cb', 'other') not null,
	rur_cource DECIMAL(10,6) not null,
	FOREIGN KEY (currency)
      REFERENCES currency(id)
      ON UPDATE RESTRICT ON DELETE RESTRICT,
	PRIMARY KEY (currency, `date`)
);

/* Метрики, которые мы будем собирать */
create table IF NOT EXISTS metrics (
	id int NOT NULL AUTO_INCREMENT,
	s_title string not null,
	period enum('year', 'month', 'week', 'day', 'other') not null,
	currency int external key currency(id) not null,
	last_ok_parse DATETIME,
	last_fail_parse DATETIME,
	s_last_parse_error TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (currency)
      REFERENCES currency(id)
      ON UPDATE RESTRICT ON DELETE RESTRICT
);

/* Собранные по метрикам данные */
create table IF NOT EXISTS metric (
	id int NOT NULL AUTO_INCREMENT,
	metric int not null,
	date_described DATETIME not null, /* дата, которую описывают данные */
	date_parsed DATETIME not null, 	  /* дата, когда данные были фактически выгружены в нашу базу */
	value BIGINT not null, /* собственно, данные. Пока берём длинное целое, вроде дробей в макроэкономике не держат */
	obsolete bool not null, /*	false для старых данных, по которым новая выгрузка даёт нам новое значение. При этом старое значение останется
								в БД, но с obsolete = true. */
	PRIMARY KEY (id),
	FOREIGN KEY (metric)
      REFERENCES metrics(id)
      ON UPDATE RESTRICT ON DELETE RESTRICT
);

/*	Иерархия показателей. Строго говоря, это скорей должно принадлежать отчету,
	но с вероятностью ~100% оно от отчета к отчету меняться не будет. */
create table IF NOT EXISTS metrics_hirarchy (
	id int NOT NULL AUTO_INCREMENT,
	s_title string not null,
	metric int,
	parent int,
	FOREIGN KEY (metric)
      REFERENCES metrics(id)
      ON UPDATE RESTRICT ON DELETE RESTRICT
);