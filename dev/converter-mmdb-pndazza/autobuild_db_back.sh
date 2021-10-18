#!/usr/bin/bash

# -*- coding: utf-8 -*-
# _ https://tipitaka.eu.org _
# Ref https://stackoverflow.com/a/37296788
# Ref https://stackoverflow.com/a/20014210


# ------- USER INPUT ENDS ----------
NEWPALI_SCRIPT_DB=tipitaka_ro.db
CONVERTED_MARK=_cvted.sql
OUT=sql_files_dir

echo -e "Output DB name: $NEWPALI_SCRIPT_DB"
echo -e "SQL files in: $OUT"
echo -e "Only files end with: $CONVERTED_MARK will be used for building new script db."

buildBackDB='yes'

if [ "$buildBackDB" == 'yes' ];then
    # Building back Sqlite3 DB
    echo -e "\n\n----------------------------------"
    echo -e "Building back Sqlite3 DB in new pali script"
    rm -f $NEWPALI_SCRIPT_DB
    rm -f converted_all_table.sql

    cat $OUT/*$CONVERTED_MARK > converted_all_table.sql
    sqlite3 $NEWPALI_SCRIPT_DB < converted_all_table.sql
else
    echo -e "\n\n----------------------------------"
    echo -e "Change buildBackDB='yes' at the end of this file, if you want to repack the new script db"
    echo -e "You can add more dictionries"
    echo -e "Following the format in: $OUT/dictionary_x.sql"
    echo -e "----------------------------------"
fi

echo "Done all! => $NEWPALI_SCRIPT_DB"

