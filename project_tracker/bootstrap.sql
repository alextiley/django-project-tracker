BEGIN;

CREATE TABLE `projects_project` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(120) NOT NULL UNIQUE,
    `deployment_date` datetime NOT NULL,
    `is_complete` bool NOT NULL
);

COMMIT;