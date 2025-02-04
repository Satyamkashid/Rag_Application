import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./index.css";

const ChatGroqUploader = () => {
  const [file, setFile] = useState(null);
  const [filePath, setFilePath] = useState("");
  const [prompt, setPrompt] = useState("");
  const [llumoResults, setLlumoResults] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modelAnswer, setModelAnswer] = useState("");
  // const [accuracy, setModelAccuracy] = useState();
  // const [bert_score, setModelBertScore] = useState();
  // const [word_matching, setWordMatch] = useState();
  const [final_score, setFinalScore] = useState();
  // const [matched_words, setMatchedWords] = useState();
  // const [reference_words, setReferenceWords] = useState();
  const [unique_words_chunks, setUniqueWordsChunks] = useState();
  const [unique_words_llm, setUniqueWordsLLM] = useState();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFilePath("");
    }
  };

  const handleSubmitFile = async () => {
    if (!file) {
      alert("Please select a file before submitting.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setFilePath(response.data.filePath);
      alert("File uploaded successfully!");
    } catch (error) {
      alert("Error uploading the file");
      console.error(error);
    }

    setLoading(false);
  };

  const handleSubmitPrompt = async () => {
    if (!prompt.trim() || !filePath) {
      alert("Please select a file and enter a prompt before submitting.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5000/process", {
        filePath,
        prompt,
      });

      const { context, modelAnswer, accuracy, bert_score, word_matching, final_score, matched_words, reference_words, unique_words_chunks, unique_words_llm } = response.data;
      alert("Processing completed!");

      // Store the model's answer in the state
      setModelAnswer(modelAnswer);
      // setModelAccuracy(accuracy);
      // setModelBertScore(bert_score);
      // setWordMatch(word_matching);
      setFinalScore(final_score);
      // setMatchedWords(matched_words);
      // setReferenceWords(reference_words);
      setUniqueWordsChunks(unique_words_chunks);
      setUniqueWordsLLM(unique_words_llm);

      // Update history with the context and model's answer
      setHistory([
        ...history,
        {
          fileName: file ? file.name : "No file selected",
          prompt,
        },
      ]);
    } catch (error) {
      alert("Error processing the file");
      console.error(error);
    }

    setLoading(false);
  };

  const handleShowLlumoResults = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/llumo-eval", {
        prompt,
        filePath,
      });

      setLlumoResults(response.data); // Set the returned LLUMO results directly
    } catch (error) {
      console.error("Error fetching LLUMO results", error);
      alert("Failed to fetch LLUMO results.");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      {/* Sidebar for History */}
      <div className="sidebar">
        <h3>History</h3>
        <ul>
          {history.length > 0 ? (
            history.map((entry, index) => (
              <li key={index}>
                <p><strong>File:</strong> {entry.fileName}</p>
                <p><strong>Prompt:</strong> {entry.prompt}</p>
              </li>
            ))
          ) : (
            <p>No history available.</p>
          )}
        </ul>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <h1>ChatGroq</h1>

        {/* Results Section */}
        {modelAnswer && (
          <div className="section">
            <h2>Model's Answer</h2>
            <div className="model-answer">
              <ReactMarkdown>{modelAnswer}</ReactMarkdown>
            </div>
          </div>
        )}

        {/* {accuracy && (
          <div className="section">
            <h2>Model's Accuracy</h2>
            <p>{accuracy}</p>
          </div>
        )}

        {bert_score && (
          <div className="section">
            <h2>Model's BERTScore</h2>
            <p><strong>F1 Score:</strong> {bert_score.f1}</p>
            <p><strong>Precision:</strong> {bert_score.precision}</p>
            <p><strong>Recall:</strong> {bert_score.recall}</p>
          </div>
        )}

        {word_matching && (
          <div className="section">
            <h2>Word Matching</h2>
            <p><strong>Exact Match:</strong> {word_matching.exact_match_percentage.toFixed(2)}%</p>
            <p><strong>Fuzzy Match:</strong> {word_matching.fuzzy_match_percentage.toFixed(2)}%</p>
            <p><strong>Combined Match:</strong> {word_matching.combined_match_percentage.toFixed(2)}%</p>
          </div>
        )} */}

        {final_score && (
          <div className="section">
            <h2>Final Score</h2>
            <p>{final_score}</p>
          </div>
        )}

        {/* {matched_words && (
          <div className="section">
            <h2>Matched Words LLM</h2>
            <p>{matched_words}</p>
          </div>
        )}

        {reference_words && (
          <div className="section">
            <h2>Reference Words Chunks</h2>
            <p>{reference_words}</p>
          </div>
        )} */}

        {unique_words_chunks && (
          <div className="section">
            <h2>Unique Words Chunks</h2>
            <p>{unique_words_chunks}</p>
          </div>
        )}

        {unique_words_llm && (
          <div className="section">
            <h2>Unique Words LLM</h2>
            <p>{unique_words_llm}</p>
          </div>
        )}

        {/* Bottom Section for Inputs and LLUMO Results */}
        <div className="bottom-section">
          {/* File Upload Section */}
          <div className="input-section">
            <h2>Upload PDF</h2>
            <input type="file" accept=".pdf" onChange={handleFileChange} />
            <button onClick={handleSubmitFile} disabled={loading}>
              {loading ? "Uploading..." : "Upload File"}
            </button>
          </div>

          {/* Prompt Input Section */}
          <div className="input-section">
            <h2>Enter Prompt</h2>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your prompt here..."
              rows="4"
            />
            <button onClick={handleSubmitPrompt} disabled={loading}>
              {loading ? "Processing..." : "Submit Prompt"}
            </button>
          </div>

          {/* LLUMO Results Section */}
          <div className="input-section">
            <h2>LLUMO Evaluation</h2>
            <button onClick={handleShowLlumoResults} disabled={loading}>
              {loading ? "Loading..." : "Show LLUMO Results"}
            </button>
            {llumoResults && (
              <pre>{JSON.stringify(llumoResults, null, 2)}</pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatGroqUploader;