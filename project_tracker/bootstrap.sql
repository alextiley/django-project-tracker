BEGIN;

CREATE DATABASE project_tracker default character set utf8;

CREATE TABLE `dashboard_project` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `project_name` varchar(120) NOT NULL UNIQUE,
    `deployment_date` datetime NOT NULL,
    `is_closed` bool NOT NULL
)
;

COMMIT;