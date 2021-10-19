#!/usr/bin/bash

# -*- coding: utf-8 -*-
# Ref https://stackoverflow.com/a/37296788
# Ref https://stackoverflow.com/a/20014210

# ***********************
# INSTALL DEPENDENCES &
# DOWNLOAD SCRIPT
# ***********************

# sudo apt update
# sudo apt install -y git nodejs wget sqlite3
# wget -c https://vpnry.github.io/tipitaka/dev/converter-mmdb-pndazza/db_extracter.sh
# wget -c https://vpnry.github.io/tipitaka/dev/converter-mmdb-pndazza/autobuild_db_back.sh
# wget -c https://vpnry.github.io/tipitaka/dev/converter-mmdb-pndazza/db_PaliScriptConverter.js
# git clone https://github.com/pnfo/pali-script-converter.git

# bash db_extracter.sh


# ------- USER INPUT STARTS ----------

DB=tipitaka_pali.db
# modify this number manually
TOTAL_DICTIONARY_IN_DB=7
NEWPALI_SCRIPT_DB=tipitaka_ro.db
CONVERTED_MARK=_cvted.sql

# ------- USER INPUT ENDS ----------


# ----------------------------------
JS=db_PaliScriptConverter.js
OUT=sql_files_dir
rm -rf $OUT
mkdir -p $OUT

# Extract schema to inspect only, no use
sqlite3 $DB .schema > __schema.sql
# sed "/^CREATE TABLE sqlite_sequence(name,seq);/d" __schema.sql -i_


# dump all tables
for t in $(sqlite3 $DB .tables); do
    echo "Extracting $t"
    echo -e ".dump ${t}" | sqlite3 $DB > $OUT/$t.sql
done


# dictionary.sql
echo 'Moving dictionary file'
    head -n 20 "$OUT/dictionary.sql" > head_dict_7lines.txt
    mv -f "$OUT/dictionary.sql" .

# Extract each dictionary
echo -e "\nSplitting each dictionary, easier to update"

# A trick make them like .dump result
# Get the first 20 lines (head -n 20 dictionary.sql)
# Added: IF NOT EXISTS to handle multi dictionary file

headLines='PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `dictionary` (
	`word`	TEXT,
	`definition`	TEXT,
	`book`	INTEGER
);'

for n in $(seq "$TOTAL_DICTIONARY_IN_DB"); do
    echo -e "Splitting dictionary number $n"
    echo -e "$headLines" > $OUT/dictionary_$n.sql
    echo -e ".mode insert dictionary\nselect * from dictionary where book=$n;" | sqlite3 $DB >> $OUT/dictionary_$n.sql
    echo -e "COMMIT;" >> $OUT/dictionary_$n.sql
done


# transliterating/convert pāli scripts
    echo -e "Running converter, it may take up to 10 minutes or more."
    node $JS

echo "Done all"

echo "Run: bash autobuild_db_back.sh if you want to pack the new script into database"

