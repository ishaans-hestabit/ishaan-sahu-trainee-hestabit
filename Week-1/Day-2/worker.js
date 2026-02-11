const { workerData, parentPort } = require('worker_threads');
const fs = require("fs/promises");
const path = require("path");

// the main processing of file based on the flag
async function processFile({ flag, file ,outputDir}) {
  const start = process.hrtime.bigint();
  const data = await fs.readFile(file, "utf-8");

  if (flag === "--lines") {
    console.log(`${file} → Lines:`, countLines(data));
  }

  if (flag === "--words") {
    console.log(`${file} → Words:`, countWords(data));
  }

  if (flag === "--chars") {
    console.log(`${file} → Characters:`, countChars(data));
  }

  if (flag === "--unique") {
    const uniqueLines = [...new Set(data.split("\n"))].join("\n");
    const outFile = path.join(
      outputDir,
      `unique-${path.basename(file)}`
    );
    await fs.writeFile(outFile, uniqueLines);
    console.log(`Unique file written → ${outFile}`);
  }

  const end = process.hrtime.bigint();

  return {
    file,
    executionTimeMs: Number(end - start) / 1_000_000,
    memoryMB: Number(
      process.memoryUsage().heapUsed / 1024 / 1024
    ).toFixed(2),
  };
}

processFile(workerData)
.then(result => parentPort.postMessage(result))
.catch(err => {
    console.error(err);
    process.exit(1);
});

// the real logical functions

function countLines(data) {
  return data.split("\n").length;
}

function countWords(data) {
  return data.trim().split(/\s+/).length;
}

function countChars(data) {
  return data.length;
}