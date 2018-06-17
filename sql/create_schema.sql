# mysql -u username -p
# password: password

USE coinexplorer;

CREATE TABLE IF NOT EXISTS timetable (
    name VARCHAR(20) PRIMARY KEY,
    lastupdated INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS block (
    blockhash CHAR(64) PRIMARY KEY,
    size MEDIUMINT UNSIGNED NOT NULL,
    strippedsize MEDIUMINT UNSIGNED NOT NULL,
    weight MEDIUMINT UNSIGNED NOT NULL,
    height MEDIUMINT UNSIGNED NOT NULL,
    version TINYINT UNSIGNED NOT NULL,
    merkleroot CHAR(64) NOT NULL,
    txcount SMALLINT UNSIGNED NOT NULL,
    time INT(11) NOT NULL,
    nonce BIGINT UNSIGNED NOT NULL,
    bits CHAR(10) NOT NULL,
    difficulty DOUBLE NOT NULL,
    chainwork CHAR(64) NOT NULL,
    previousblockhash CHAR(64),
    nextblockhash CHAR(64),
    fees FLOAT NOT NULL,
    confirmations MEDIUMINT UNSIGNED
);

CREATE TABLE IF NOT EXISTS transaction (
     txid CHAR(64) PRIMARY KEY,
     txhash CHAR(64) NOT NULL,
     version TINYINT UNSIGNED NOT NULL,
     size MEDIUMINT UNSIGNED NOT NULL,
     vsize MEDIUMINT UNSIGNED NOT NULL,
     locktime MEDIUMINT UNSIGNED NOT NULL,
     fees FLOAT NOT NULL,
     confirmations MEDIUMINT UNSIGNED
);

CREATE TABLE IF NOT EXISTS transaction_input (
    coinbase VARCHAR(400),
    txid CHAR(64),
    input_index SMALLINT UNSIGNED,
    prev_txid CHAR(64),
    prev_output_index SMALLINT UNSIGNED,
    script_signature JSON NOT NULL,
    sequence INT NOT NULL,
    PRIMARY KEY(txid, input_index)
);

CREATE TABLE IF NOT EXISTS transaction_output (
    txid CHAR(64),
    output_value INT NOT NULL,
    output_index SMALLINT UNSIGNED,
    scriptpubkey JSON NOT NULL,
    PRIMARY KEY(txid, output_index)
);
