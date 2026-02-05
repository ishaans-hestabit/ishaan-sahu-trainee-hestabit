const http = require('http')
let count = 0;

const server = http.createServer((req,res)=>{
    res.setHeader("Content-Type","application/json");

    if(req.url === '/ping'){
        res.statusCode = 200;
        res.end(JSON.stringify({time: Date.now()}));
    }

    else if(req.url === '/headers'){
        res.statusCode = 200;
        res.end(JSON.stringify(req.headers));
    }

    else if(req.url === '/count'){
        count++;
        res.statusCode = 200;
        res.end(JSON.stringify({count}));
    }

    else {
        res.statusCode = 404;
        res.end(JSON.stringify({error : "Not Found"}));
    }
});

server.listen(3000,()=>{
    console.log("Server running on http://localhost:3000");
});