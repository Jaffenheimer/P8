START TRANSACTION;

CREATE TABLE IF NOT EXISTS BusStops
(
    Id          VARCHAR(40)    NOT NULL,
    Latitude    DECIMAL(10, 8) NOT NULL,
    Longitude   DECIMAL(11, 8) NOT NULL,
    PeopleCount INT DEFAULT 0,
    
    UpdatedAt   TIMESTAMP      NOT NULL,
    PRIMARY KEY (Id)
);
COMMIT;
