DROP DATABASE IF EXISTS OOO_Polus;
CREATE DATABASE IF NOT EXISTS OOO_Polus;
USE OOO_Polus;

CREATE TABLE user_info (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    fio varchar(255) NOT NULL,
    phone int(15) NOT NULL UNIQUE,
    role_log ENUM('Клиент', 'Мастер', 'Администратор') NOT NULL,
    login VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

	CREATE TABLE master_info(
	master_id int primary key,
	master_fio varchar(255),
    master_phone int(15)
);

INSERT INTO master_info (master_id, master_fio, master_phone) 
VALUES 
(1, 'Иванов Иван Иванович', 799912367),
(2, 'Петров Петр Петрович', 799998765),
(3, 'Сидоров Сидор Сидорович', 799955544);

CREATE TABLE components (
    component_id INT PRIMARY KEY AUTO_INCREMENT,
    component_name VARCHAR(255) NOT NULL UNIQUE,
    component_quantity INT DEFAULT 0
);
-- Вставка данных в таблицу components
INSERT INTO components (component_name, component_quantity) VALUES
('Printer Cartridge', 20),      -- Картриджи для принтера
('Printer Roller', 15),         -- Ролики для принтера
('Printer Belt', 10),           -- Приводные ремни для принтера
('Laptop Screen', 8),           -- Экраны для ноутбуков
('Laptop Keyboard', 12),        -- Клавиатуры для ноутбуков
('Laptop Battery', 10),         -- Батареи для ноутбуков
('Laptop Charger', 14),         -- Зарядные устройства для ноутбуков
('Computer Power Supply', 6),   -- Блоки питания для ПК
('Computer RAM Module', 25),    -- Модули оперативной памяти
('Computer Motherboard', 5),    -- Материнские платы
('Computer CPU Fan', 18),       -- Вентиляторы для процессоров
('Computer Hard Drive', 9);     -- Жесткие диски


CREATE TABLE application (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
	start_date DATE,
    org_tech_type ENUM('Компьютер', 'Ноутбук', 'Принтер'),
    org_tech_model VARCHAR(255) ,
    problem_description TEXT ,
	client_fio varchar(255),
    application_status ENUM('В процессе ремонта', 'Готова к выдаче', 'Новая заявка') DEFAULT 'Новая заявка',
	completion_date DATE,
    repair_name varchar(255),
    master_id int,
    repair_quantity int

);

CREATE TABLE message(
comment_id int primary key auto_increment,
message text,
master_id int,
order_id int

);

CREATE TABLE orders_status (
    order_status_id INT PRIMARY KEY AUTO_INCREMENT,
    start_date DATE,
    org_tech_type ENUM('Компьютер', 'Ноутбук', 'Принтер'),
    org_tech_model VARCHAR(255) NOT NULL,
	client_fio varchar(255),
    repair_name varchar(255)
);

DELIMITER $$

CREATE TRIGGER trg_application_status_update
AFTER UPDATE ON application
FOR EACH ROW
BEGIN
    IF NEW.application_status = 'Готова к выдаче' THEN
        INSERT INTO orders_status (start_date, org_tech_type, org_tech_model, client_fio, repair_name)
        VALUES (NEW.start_date, NEW.org_tech_type, NEW.org_tech_model, NEW.client_fio, NEW.repair_name);
    END IF;
END$$

DELIMITER ;


