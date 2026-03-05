import { useState } from 'react';
import axios from 'axios'

function App() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log(name);
      
      const response = await axios.post("http://localhost:3000/", { name, email });
      console.log("Success:", response.data);
      alert(`Data saved! ${response.data}`);
      setName("");
      setEmail("");
    } catch (error) {
      console.error("Error saving data:", error);
    }
  };

  return (
    <div style={styles.wrapper}>
      <form onSubmit={handleSubmit} style={styles.card}>
        <h2 style={styles.title}>Welcome</h2>
        <input 
          type="text" 
          placeholder="Name" 
          value={name}
          onChange={(e) => setName(e.target.value)} 
          style={styles.input}
        />
        <input 
          type="email" 
          placeholder="Email" 
          value={email}
          onChange={(e) => setEmail(e.target.value)} 
          style={styles.input}
        />
        <button type="submit" style={styles.button}>
          Submit
        </button>
      </form>
    </div>
  );
}

const styles = {
  wrapper: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    backgroundColor: "#f3f4f6",
    fontFamily: "system-ui, sans-serif"
  },
  card: {
    backgroundColor: "white",
    padding: "32px",
    borderRadius: "12px",
    display: "flex",
    flexDirection: "column",
    width: "100%",
    maxWidth: "360px"
  },
  title: {
    marginBottom: "24px",
    textAlign: "center",
    color: "#111827",
    fontSize: "24px"
  },
  input: {
    padding: "12px",
    marginBottom: "16px",
    border: "1px solid #d1d5db",
    borderRadius: "6px",
    fontSize: "16px",
    outline: "none"
  },
  button: {
    padding: "12px",
    backgroundColor: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "6px",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
  }
};

export default App;