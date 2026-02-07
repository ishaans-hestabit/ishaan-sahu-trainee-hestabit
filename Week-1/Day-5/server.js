const http = require('http');
const PORT = 3000;

const server = http.createServer((req,res)=>{

    if(req.url === '' || req.url === '/'){
        res.statusCode = 200;
        res.end("server working fine\n");
    }
    else {
        res.statusCode = 404;
        res.end("bad request\n");
    }
});

server.listen(PORT,()=>{
    console.log(`Server Running at port ${PORT}`);
});