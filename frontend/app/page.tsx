"use client";

import { useState } from "react";

export default function Home() {
  const [fileName, setFileName] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<
    { role: string; content: string }[]
  >([]);

  const handleUpload = async () => {
    const input = document.querySelector(
      'input[type="file"]'
    ) as HTMLInputElement;

    if (!input?.files?.[0]) {
      alert("Choose PDF first");
      return;
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      console.log(data);

      alert("PDF uploaded successfully");
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    }
  };

  const handleAsk = async () => {
    if (!question) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
        },
      ]);

      setQuestion("");
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Error connecting to AI backend.",
        },
      ]);
    }
  };

  return (
    <main className="min-h-screen bg-[#0f172a] text-white flex">
      {/* Sidebar */}
      <div className="w-64 bg-[#111827] border-r border-gray-800 p-6">
        <h1 className="text-2xl font-bold mb-10">
          Project Lyra
        </h1>

        <div className="space-y-4">
          <button className="w-full bg-blue-600 hover:bg-blue-700 transition p-3 rounded-xl">
            New Chat
          </button>

          <button
            onClick={handleUpload}
            className="w-full bg-blue-600 hover:bg-blue-700 transition p-3 rounded-xl"
          >
            Upload PDF
          </button>
        </div>
      </div>

      {/* Main */}
      <div className="flex-1 flex flex-col items-center justify-center px-8">
        <div className="w-full max-w-4xl">

          {/* Hero */}
          <div className="text-center mb-10">
            <h1 className="text-5xl font-bold mb-4">
              AI Learning Intelligence
            </h1>

            <p className="text-gray-400 text-lg">
              Upload PDFs, research papers, notes and chat with AI.
            </p>
          </div>

          {/* Upload */}
          <div className="bg-[#1e293b] border border-gray-700 rounded-3xl p-10 shadow-2xl mb-8">

            <div className="border-2 border-dashed border-gray-600 rounded-2xl p-12 text-center">

              <h2 className="text-2xl font-semibold mb-4">
                Upload Your PDF
              </h2>

              <p className="text-gray-400 mb-6">
                Drag & drop files or choose from device
              </p>

              <input
                type="file"
                accept=".pdf"
                onChange={(e) => {
                  if (e.target.files) {
                    setFileName(e.target.files[0].name);
                  }
                }}
                className="mb-6"
              />

              {fileName && (
                <p className="text-green-400 mb-6">
                  Selected: {fileName}
                </p>
              )}

              <button
                onClick={handleUpload}
                className="bg-blue-600 hover:bg-blue-700 transition px-8 py-3 rounded-xl text-lg font-medium"
              >
                Upload PDF
              </button>
            </div>
          </div>

          {/* Chat */}
          <div className="bg-[#1e293b] border border-gray-700 rounded-2xl p-6">

            <h2 className="text-2xl font-bold mb-6">
              Ask AI
            </h2>

            {/* Messages */}
            <div className="space-y-4 mb-6 max-h-[400px] overflow-y-auto">

              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-2xl ${
                    msg.role === "user"
                      ? "bg-cyan-500 text-white ml-auto max-w-[80%]"
                      : "bg-[#0f172a] border border-gray-700 text-gray-200 max-w-[80%]"
                  }`}
                >
                  {msg.content}
                </div>
              ))}
            </div>

            {/* Input */}
            <div className="flex gap-4">
              <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask questions about uploaded documents..."
                className="flex-1 bg-[#0f172a] border border-gray-700 rounded-2xl p-5 text-lg outline-none"
              />

              <button
                onClick={handleAsk}
                className="bg-cyan-500 hover:bg-cyan-600 transition px-8 rounded-2xl font-semibold"
              >
                Send
              </button>
            </div>

          </div>
        </div>
      </div>
    </main>
  );
}