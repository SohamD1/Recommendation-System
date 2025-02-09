import React, { useState } from "react";
import "./App.css";

function App() {
  // States for the inputs and the result
  const [input1, setInput1] = useState("");
  const [input2, setInput2] = useState("");
  const [input3, setInput3] = useState("");
  const [result, setResult] = useState("");

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent page reload
    try {
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ input1, input2, input3 }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch recommendation");
      }

      const data = await response.json();
      setResult(data.recommendation); // Assuming the backend sends { recommendation: "..." }
    } catch (error) {
      console.error("Error fetching recommendation:", error);
      setResult("Error fetching recommendation. Please try again.");
    }
  };

  return (
    <div className="App">
      <h1>Recommendation System</h1>
      <form onSubmit={handleSubmit} className="recommendation-form">
        <div className="form-group">
          <label htmlFor="input1">Input 1:</label>
          <input
            type="text"
            id="input1"
            value={input1}
            onChange={(e) => setInput1(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="input2">Input 2:</label>
          <input
            type="text"
            id="input2"
            value={input2}
            onChange={(e) => setInput2(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="input3">Input 3:</label>
          <input
            type="text"
            id="input3"
            value={input3}
            onChange={(e) => setInput3(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="submit-button">
          Get Recommendation
        </button>
      </form>

      {result && (
        <div className="result">
          <h2>Recommendation:</h2>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}

export default App;
