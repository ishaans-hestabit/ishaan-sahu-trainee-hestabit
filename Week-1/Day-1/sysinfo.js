const { exec } = require('child_process');
const os = require('os');
const fs = require('fs');

const sysInfo = {
    hostname: os.hostname()
};

function getDiskSpaceDf(){
    // returning a promise because os operations are async so that we not get empty value of disk space
    return new Promise((resolve,reject)=>{

        exec('df -k /',(error,stdout)=>{
            if(error){
                return reject(error);
            }
            
            // parsing to extract what we need from data
            const lines = stdout.trim().split("\n");
            const dataLine = lines[1].split(/\s+/);
            const availableKB = parseInt(dataLine[3],10);
            const availableGB = (availableKB / 1024 / 1024).toFixed(2);
    
            
            resolve({
                method: "df",
                availableGB
            });
            
        });
    });
}

function getDiskSpaceStatfs(){
    // returning a promise because os operations are async so that we not get empty value of disk space
    // if we dont then due to async operation we will not get any value of disk space
    return new Promise((resolve,reject)=>{

        fs.statfs('/',(err,stats)=>{
            if(err){
                return reject(err);
            }
    
            // applying maths to conver to gb
            const availableBytes = stats.bavail * stats.bsize;
            const availableGB = (availableBytes / 1024 / 1024 / 1024).toFixed(2);
    
            resolve({
                method: "statfs",
                availableGB
            });
            
        });
    })

}


async function getDiskSpace(){
    try {
        // Statfs is more new so first using that
        const diskSpace = await getDiskSpaceStatfs();
        sysInfo.availableDiskSpace = diskSpace.availableGB + " GB";
        
        return;
    }
    
    catch (err){
        // older node versions dont support statfs so using this shell command version
        const diskSpace = await getDiskSpaceDf();
        
        sysInfo.availableDiskSpace = diskSpace.availableGB + " GB";
        return;
    }
}


function getOpenPorts(){
    return new Promise((resolve,reject)=>{
        // linux command to get 5 unique listening ports
        exec("ss -tunl | awk 'NR>1 {print $5}' | grep -oE '[0-9]+$' | sort -u | head -n 5",(error,stdout)=>{
            if(error){
                return reject(error);
            }
            
            // filtering it the number of ports out of the reulst
            const ports = stdout.trim().split('\n').filter(p => p);
            resolve(ports);
        })
    })
}


function getDefaultGateway() {
    return new Promise((resolve, reject) => {
        exec("ip route show default", (error, stdout) => {
            if (error) {
                return reject(error);
            }

            const line = stdout.trim();
            if (!line) {
                return reject(new Error("No default route found"));
            }

            const parts = line.split(" ");
            const viaIndex = parts.indexOf("via");

            if (viaIndex === -1 || !parts[viaIndex + 1]) {
                return reject(new Error("Gateway not found in route output"));
            }

            resolve(parts[viaIndex + 1]);
        });
    });
}

function getLoggedInUsers(){
    return new Promise((resolve, reject) => {
        // "who" gives the sessions of users but there can be duplicates
        // so we removed that
        
        exec("who | awk '{print $1}' | sort -u", (error, stdout) => {
            if(error){
                return reject(error);
            }
            
            // parsing the output to get array of users
            const users = stdout.trim().split('\n').filter(u => u);
            
            // now sending length which is the number of users
            resolve(users.length);
        });
    });
}

// check is file existing? 

function ensureLogsDir() {
    if (!fs.existsSync("logs")) {
        fs.mkdirSync("logs");
    }
}

// calculated runtime metric
function getRuntimeMetrics() {
    return {
        timestamp: new Date().toISOString(),
        cpuUsage: process.cpuUsage(),
        resourceUsage: process.resourceUsage()
    };
}

// now finally writting in the file

function writeMetricsToFile(metrics) {
    ensureLogsDir();

    const filePath = "logs/day1-sysmetrics.json";
    fs.writeFileSync(filePath, JSON.stringify(metrics, null, 2));
}



// we are wrapping this so that we can make an async call to this function
async function main() {
    
    await getDiskSpace(); 

    try {
        sysInfo.openPorts = await getOpenPorts();
    
    } catch {
        sysInfo.openPorts = [];
    }

    try {
        sysInfo.defaultGateway = await getDefaultGateway();
    } catch {
        sysInfo.defaultGateway = "unavailable";
    }

    try{
        sysInfo.loggedInUsers = await getLoggedInUsers();
    }
    catch{
        sysInfo.loggedInUsers = 0;
    }

    const runtimeMetrics = getRuntimeMetrics();
    writeMetricsToFile(runtimeMetrics);

    console.log(sysInfo);
}

main();

