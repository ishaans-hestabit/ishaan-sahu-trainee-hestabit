const fs = require("fs/promises");
const path = require("path");


// whenever we pass arguments from cli they are stored in argv array and 
// first one is the path of node
// second one is the path of your js file
// after that we can access arguments after first two
const args = process.argv.slice(2);
// run logs

const LOG_DIR = "logs";

// the output if we run --unique flag
const OUTPUT_DIR = "output";


// existential check for the intended directories
async function ensureDirs() {
  await fs.mkdir(LOG_DIR, { recursive: true });
  await fs.mkdir(OUTPUT_DIR, { recursive: true });
}

//how we pre process the cli arguments to make a json array

function parseArgs(args) {
  const tasks = [];

  for (let i = 0; i < args.length; i += 2) {
    tasks.push({  flag: args[i],
                  file: args[i + 1],
    });
  }
  return tasks;
}

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


// the main processing of file based on the flag
async function processFile({ flag, file }) {
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
      OUTPUT_DIR,
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



async function main() {
  await ensureDirs();

  // here data is converted into the tasks array in which the file name and tag is given
  const tasks = parseArgs(args);

  
  // all files are processed 
  const results = await Promise.all(
    tasks.map(processFile)
  );

  // now we create new log file that will contain all the system data

  const logFile = path.join(
    LOG_DIR,
    `performance-${Date.now()}.json`
  );

  // now writing system info in log file
  await fs.writeFile(
    logFile,
    JSON.stringify(results, null, 2)
  );

  console.log(`\n Performance log saved → ${logFile}`);
};

main()
