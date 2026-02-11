const fs = require("fs/promises");
const path = require("path");
const {Worker} = require('worker_threads');



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
                  outputDir: OUTPUT_DIR
    });
  }
  return tasks;
}

function runWorker(task){
    return new Promise ((resolve,reject)=>{
        const worker = new Worker(path.join(__dirname,'worker.js'),{workerData:task});

        worker.on('message',(result)=>{
            resolve(result);
        });
        worker.on('error',(err)=>{
            reject(err);
        })
        worker.on('exit',(code)=>{
            if(code) reject(new Error(`Worker stopped with exit code ${code}`))
        })
    });
}


async function main() {
  await ensureDirs();

  // here data is converted into the tasks array in which the file name and tag is given
  const tasks = parseArgs(args);

  
  // all files are processed 

  const results = await Promise.all(tasks.map(runWorker));

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
