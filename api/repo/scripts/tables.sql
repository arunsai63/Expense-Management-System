CREATE TABLE balance (
    amount FLOAT NOT NULL DEFAULT 0
)

CREATE TABLE tags(
    tagID SERIAL PRIMARY KEY,
    tagText VARCHAR(64) UNIQUE NOT NULL
)

CREATE TABLE subtags(
    tagID INTEGER REFERENCES tags(tagID),
    subtagID SERIAL PRIMARY KEY,
    subtagText VARCHAR(64) NOT NULL
)

CREATE TABLE debits (
    debitID SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    remainingBalance FLOAT NOT NULL,
    description VARCHAR(2000),
    dateDebited TIMESTAMP NOT NULL DEFAULT now(),
    tagID INTEGER REFERENCES tags(tagID) DEFAULT 1 NOT NULL,
    subtagID INTEGER REFERENCES subtags(subtagID)
)

CREATE TABLE credits (
    creditID SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    remainingBalance FLOAT NOT NULL,
    description VARCHAR(2000),
    dateCredited TIMESTAMP NOT NULL DEFAULT now(),
    tagID INTEGER REFERENCES tags(tagID)
)


