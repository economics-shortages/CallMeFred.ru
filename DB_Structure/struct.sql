
/* Валюты, которыми мы будем оперировать */
create table currency  (
	id int NOT NULL AUTO_INCREMENT,
	title string not null,
	mark string(3) not null,
	PRIMARY KEY (id)
);

/* Курс валюты к рублю на определенную дату */
create table currency_cource (
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
create table metrics (
	id int NOT NULL AUTO_INCREMENT,
	string title not null,
	pariod enum('year', 'month', 'week', 'day', 'other') not null,
	divide_by int not null, /* хинт для отображения, а хранить будем тупо сырое целое */
	currency int external key currency(id) not null,
	last_ok_parse DATETIME,
	last_fail_parse DATETIME,
	last_parse_error TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (currency)
      REFERENCES currency(id)
      ON UPDATE RESTRICT ON DELETE RESTRICT
);

/* Собранные по метрикам данные */
create table metric (
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