"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [lyrics, setLyrics] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/transcribe", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    setLyrics(data.lyrics || "No lyrics found");
    setLoading(false);
  };

  return (
    <main style={{ padding: 30 }}>
      <h1>🎧 Lyrics Listener</h1>

      <input
        type="file"
        accept=".mp3,.mp4,.wav,.m4a"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <br /><br />

      <button onClick={handleUpload}>
        {loading ? "Processing..." : "Generate Lyrics"}
      </button>

      <hr style={{ margin: "20px 0" }} />

      <textarea
        value={lyrics}
        onChange={(e) => setLyrics(e.target.value)}
        rows={20}
        style={{ width: "100%" }}
      />
    </main>
  );
}
