import { useState, useEffect } from 'react';
import axios from 'axios';

const BASE_URL = "/api/";

function App() {
  const [blog, setBlog] = useState("");
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);

 
  const fetchBlogs = async () => {
    try {
      const response = await axios.get(BASE_URL); 
      setBlogs(response.data);
    } catch (error) {
      console.error("Error fetching blogs:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBlogs();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!blog.trim()) return;

    try {
      const response = await axios.post(BASE_URL, { blog });
      console.log("Success:", response.data);
      
      setBlog("");
      fetchBlogs(); 
    } catch (error) {
      console.error("Error saving data:", error);
    }
  };

  return (
    <div style={styles.wrapper}>
      {/* Creation Section */}
      <div style={styles.container}>
        <form onSubmit={handleSubmit} style={styles.card}>
          <h2 style={styles.title}>Create a Post</h2>
          <textarea
            rows="5" 
            placeholder="What's on your mind?" 
            value={blog}
            onChange={(e) => setBlog(e.target.value)} 
            style={styles.textarea}
          />
          <button type="submit" style={styles.button}>Publish</button>
        </form>

        <hr style={styles.divider} />

        {/* Feed Section */}
        <div style={styles.feed}>
          <h2 style={styles.title}>Recent Thoughts</h2>
          {loading ? (
            <p style={{textAlign: 'center'}}>Loading blogs...</p>
          ) : (
            blogs.map((item) => (
              <div key={item._id} style={styles.blogCard}>
                
                <p style={styles.blogText}>{item.blog}</p>
                
                <span style={styles.blogDate}>

                  {item.createdAt ? new Date(item.createdAt).toLocaleString() : "Just now"}
                </span>
              </div>
            ))
          )}
          {!loading && blogs.length === 0 && (
            <p style={{textAlign: 'center', color: '#6b7280'}}>No blogs yet. Start writing!</p>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    padding: "40px 20px",
    minHeight: "100vh",
    backgroundColor: "#f9fafb",
    fontFamily: "Inter, system-ui, sans-serif",
    display: "flex",
    justifyContent: "center"
  },
  container: {
    width: "100%",
    maxWidth: "600px"
  },
  card: {
    backgroundColor: "white",
    padding: "24px",
    borderRadius: "16px",
    boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
    marginBottom: "32px"
  },
  title: {
    margin: "0 0 20px 0",
    color: "#111827",
    fontSize: "20px",
    fontWeight: "700"
  },
  textarea: {
    width: "100%",
    padding: "16px",
    marginBottom: "16px",
    border: "1px solid #e5e7eb",
    borderRadius: "8px",
    fontSize: "16px",
    resize: "vertical",
    boxSizing: "border-box",
    outline: "none",
    transition: "border-color 0.2s"
  },
  button: {
    width: "100%",
    padding: "12px",
    backgroundColor: "#111827",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "15px",
    fontWeight: "600",
    cursor: "pointer"
  },
  divider: {
    border: "0",
    borderTop: "1px solid #e5e7eb",
    margin: "40px 0"
  },
  blogCard: {
    backgroundColor: "white",
    padding: "20px",
    borderRadius: "12px",
    marginBottom: "16px",
    border: "1px solid #e5e7eb"
  },
  blogText: {
    color: "#374151",
    lineHeight: "1.6",
    whiteSpace: "pre-wrap",
    margin: "0 0 12px 0"
  },
  blogDate: {
    fontSize: "12px",
    color: "#9ca3af",
    textTransform: "uppercase",
    letterSpacing: "0.05em"
  }
};

export default App; 