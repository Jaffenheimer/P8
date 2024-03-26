START TRANSACTION;

CREATE TABLE IF NOT EXISTS BusStops
(
    Id          VARCHAR(40)    NOT NULL,
    Latitude    DECIMAL(10, 8) NOT NULL,
    Longitude   DECIMAL(11, 8) NOT NULL,
    PeopleCount INT DEFAULT 0,
    OrderNum    INT            NOT NULL,
    UpdatedAt   TIMESTAMP      NOT NULL,
    PRIMARY KEY (Id)
);
COMMIT;
