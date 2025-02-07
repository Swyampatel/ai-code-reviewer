import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [code, setCode] = useState("");
  const [review, setReview] = useState("");

  const handleReview = async () => {
    if (!code) return alert("Enter code for review");
    try {
      const response = await axios.post("http://127.0.0.1:5000/review", { code });
      setReview(response.data.review);
    } catch (error) {
      console.error("Error reviewing code", error);
    }
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>AI Code Review Assistant</h1>
      <textarea rows="6" cols="60" value={code} onChange={(e) => setCode(e.target.value)} placeholder="Enter your code here..." />
      <br />
      <button onClick={handleReview}>Review Code</button>
      {review && <pre>{review}</pre>}
    </div>
  );
};

export default App;
