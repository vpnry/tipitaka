/**
 * Convert tipitaka_pali.db in Myanamar Pali to Latin Roman Pali
 * http://play.google.com/store/apps/details?id=mm.pndaza.tipitakapali
 * @uPNRY 2021 - https://vpnry.github.io/tipitaka/dev/mpali/db_PaliScriptConverter.js
 */
const fs = require("fs");
const path = require("path");
const readline = require("readline");
const events = require("events");

// git clone https://github.com/pnfo/pali-script-converter.git
const CONVERTER = require("./pali-script-converter");

const mmStartChar = String.fromCharCode(0x1000);
const mmEndChar = String.fromCharCode(0x107f);

const mmDictionaryOnceReg = new RegExp(`([${mmStartChar}-${mmEndChar}]+)`);
const mmGlobalReg = new RegExp(`([${mmStartChar}-${mmEndChar}]+)`, "g");

const shellMarkStr = "_cvted.sql";
const dictPrefix = "dictionary";

const FROMSCRIPT = CONVERTER.Script.MY;
let toScript = CONVERTER.Script.RO;

// ---------------------------------
let SQLFILES = lsFilesInDir("sql_files_dir");
SQLFILES = SQLFILES.filter((p) => !p.endsWith(shellMarkStr));
runConverter(SQLFILES.shift(), toScript);
// ---------------------------------

function runConverter(filePath, toScript) {
    let fName = filePath.split(path.sep).pop();
    if (fName.startsWith(dictPrefix)) {
        convertDictionaryLineByLine(filePath, FROMSCRIPT, toScript);
    } else {
        convertLineByLine(filePath, FROMSCRIPT, toScript);
    }
}

async function convertDictionaryLineByLine(filePath, fromScript, toScript) {
    // Note: for dictionary, only transliterate the first word
    // So use mmDictionaryOnceReg to replace 1
    const t1 = Date.now();
    console.log("Converting dictionary:", filePath);
    let res = "";
    try {
        const rl = readline.createInterface({
            input: fs.createReadStream(filePath),
            crlfDelay: Infinity,
        });
        rl.on("line", (line) => {
            // some app may produce this variant: 'INSERT INTO "dictionary" VALUES'
            const yesConvert = line.indexOf("INSERT INTO dictionary VALUES");
            if (yesConvert > -1) {
                line = line.replace(mmDictionaryOnceReg, (_, mmChunk) => {
                    const ro = CONVERTER.convert(mmChunk, fromScript, toScript);
                    return ro.toLowerCase();
                });
            }
            res += line + "\n";
        });

        await events.once(rl, "close");
        // this ending ${shellMarkStr} will be used in the shell script
        const outFileName = `${filePath}_${toScript}${shellMarkStr}`;
        fs.writeFileSync(outFileName, res, { encoding: "utf8" });

        const tookMinute = (Date.now() - t1) / (1000 * 60);
        console.log(
            "Converted:",
            outFileName,
            "\nTook:",
            tookMinute,
            "minutes"
        );
        console.log("\nProcessing other files, pls wait...\n");

        const nextFile = SQLFILES.shift();
        if (nextFile) {
            runConverter(nextFile, toScript);
        }
    } catch (e) {
        console.log("Error when converting", filePath, e);
    }
}

async function convertLineByLine(filePath, fromScript, toScript) {
    const t1 = Date.now();
    console.log("Converting:", filePath);
    let res = "";
    try {
        const rl = readline.createInterface({
            input: fs.createReadStream(filePath),
            crlfDelay: Infinity,
        });

        rl.on("line", (line) => {
            line = line.replace(mmGlobalReg, (_, mmChunk) => {
                const ro = CONVERTER.convert(mmChunk, fromScript, toScript);
                return ro.toLowerCase();
            });
            res += line + "\n";
        });

        await events.once(rl, "close");

        const outFileName = `${filePath}_${toScript}${shellMarkStr}`;
        fs.writeFileSync(outFileName, res, { encoding: "utf8" });

        const tookMinute = (Date.now() - t1) / (1000 * 60);
        console.log(
            "Converted:",
            outFileName,
            "\nTook:",
            tookMinute,
            "minutes"
        );
        console.log("\nProcessing other files, pls wait...\n");

        const nextFile = SQLFILES.shift();
        if (nextFile) {
            runConverter(nextFile, toScript);
        }
    } catch (e) {
        console.log("Error when converting", filePath, e);
    }
}

function lsFilesInDir(dir) {
    /*lsFilesInDir @pnry v.2021*/
    let res = [];
    function doList(d) {
        fs.readdirSync(d).forEach((e) => {
            let ePath = path.join(d, e);
            const s = fs.statSync(ePath);
            if (s.isDirectory()) {
                doList(ePath);
            } else if (s.isFile()) {
                res.push(ePath);
            }
        });
    }
    doList(dir);
    return res;
}
