const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const port = 3000;
const app = express();

app.use(cors({
  origin: '*'
}));
app.use(express.json());

mongoose.connect(process.env.MONGO_URL)
.then(() => console.log("Connected to MongoDB via Docker!"))
.catch(err => console.error("Connection error:", err));

const BlogSchema = new mongoose.Schema({ blog: String }, { timestamps: true });
const Blog = mongoose.model('Blog', BlogSchema);

app.get("/", async (req, res) => {
    try {
        const blogs = await Blog.find({}).sort({ createdAt: -1 });
        return res.status(200).json(blogs);
    } catch (err) {
        res.status(500).send(err.message);
    }
})

app.post("/", async (req, res) => {
    try {
        const newBlog = new Blog(req.body);
        await newBlog.save();
        res.status(200).json({ message: "Blog saved to mongo!" });
    } catch (err) {
        res.status(500).send(err.message);
    }
});

app.listen(port, () => {
    console.log(`Server Listening on port ${port}`);
})