-- tournaments
CREATE TABLE tournaments (
    tournament_id   SERIAL PRIMARY KEY,
    title           VARCHAR(150) NOT NULL,
    tier            INT NOT NULL,
    country         VARCHAR(50) NULL,
    event_start     DATE NOT NULL,
    event_end       DATE NOT NULL,
    entrants        INT NULL
);

-- tournament index
CREATE TABLE tournament_index (
    index_id        SERIAL PRIMARY KEY,
    liquidpedia_url TEXT UNIQUE NOT NULL,
    startgg_slug    TEXT NULL,
    discovered_at   TIMESTAMP DEFAULT NOW(),
    processed       BOOLEAN DEFAULT FALSE
);