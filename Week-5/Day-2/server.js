const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const port = 3000;
const app = express();

app.use(cors());
app.use(express.json());


mongoose.connect(process.env.MONGO_URL)
.then(() => console.log("Connected to MongoDB via Docker!"))
.catch(err => console.error("Connection error:", err));

// mongoose.connect("mongodb://localhost:27018/week-5")
// .then(() => console.log("Connected to MongoDB via Docker!"))
// .catch(err => console.error("Connection error:", err));


const UserSchema = new mongoose.Schema({ name: String, email: String });
const User = mongoose.model('User', UserSchema);

app.post("/",async (req,res)=>{
    try{
        const newUser = new User(req.body);
        // console.log(req.body);
        console.log(newUser);
        await newUser.save();
        res.status(200).send("User saved to mongo!");
    } catch(err){
        res.status(500).send(err.message);
    }
});

app.listen(port,()=>{
    console.log(`Server Listening on port ${port}`);
})