

## Step 1 -  Pali Myanmar tipitaka_pali.db

Retrieve the **Myanmar Tipitaka Pali** database `tipitaka_pali.db` from
 `Tipitaka Pali` app  ( [Google Play link](http://play.google.com/store/apps/details?id=mm.pndaza.tipitakapali) ).
 
Copy the `tipitaka_pali.db` to your home dir (or any dir). Open Ubuntu terminal and `cd` to this dir.

## Step 2 -  install some utilities

On your Ubuntu terminal, run the below commands to install some tools.

To avoid mysterious bugs, even these tools have already been installed before on your computer, consider updating them to the latest versions, especially the **sqlite3**.

```
sudo apt update
sudo apt install -y sqlite3 git nodejs wget

```

Tested with: SQLite3 version 3.36.0

Note: the command in the shell script is **sqlite3** with number **3**,  sqlite.

## Step 3 -  download scripts files

```
wget -c https://vpnry.github.io/tipitaka/dev/converter-mmdb-pndazza/db_extracter.sh

wget -c https://vpnry.github.io/tipitaka/dev/converter-mmdb-pndazza/autobuild_db_back.sh

wget -c https://vpnry.github.io/tipitaka/dev/converter-mmdb-pndazza/db_PaliScriptConverter.js

git clone https://github.com/pnfo/pali-script-converter.git


```

We now should have the **pali-script-converter** folder and the other files in the same dir like this:


```
.
├── db_extracter.sh
├── autobuild_db_back.sh
├── db_PaliScriptConverter.js
├── tipitaka_pali.db
└── pali-script-converter

```

## Step 4 -  run the converter

Finally run the shell script:

```
bash db_extracter.sh

```

Note: **Don't** run with `sh db_extracter.sh`

It will take time to convert (1x minutes on my phone), so pls wait.

If things go smooth, it will export many .sql files in **sql_files_dir**.

+ You can add more dictionaries following the format in: `sql_files_dir/dictionary_NUMBER.sql_Latn_cvted.sql`. Only files end with **_cvted.sql** will be used for building new script db with the auto script bellow.

+ If you want to auto build the db in new script, run:

```
bash autobuild_db_back.sh

```


