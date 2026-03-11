"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type State = "idle" | "loading" | "success" | "error";

interface ApiResponse {
  success: boolean;
  message?: string;
  error?: string;
  summary?: string;
  rows_parsed?: number;
  email_sent?: boolean;
  email_message?: string;
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [email, setEmail] = useState("");
  const [state, setState] = useState<State>("idle");
  const [data, setData] = useState<ApiResponse | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file || !email.trim()) return;
    setState("loading");
    setData(null);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("recipient_email", email.trim());
    try {
      const res = await fetch(`${API_URL}/api/insight`, {
        method: "POST",
        body: formData,
      });
      const json: ApiResponse = await res.json();
      setData(json);
      setState(json.success ? "success" : "error");
    } catch (err) {
      setData({
        success: false,
        error: err instanceof Error ? err.message : "Request failed",
      });
      setState("error");
    }
  }

  return (
    <main className="container">
      <h1>Sales Insight Automator</h1>
      <p className="subtitle">
        Upload a CSV or XLSX file and receive an executive summary by email.
      </p>

      <form className="form" onSubmit={handleSubmit}>
        <div>
          <label className="label" htmlFor="file">
            Sales data file (.csv or .xlsx)
          </label>
          <input
            id="file"
            type="file"
            accept=".csv,.xlsx"
            className="fileInput"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            required
          />
        </div>
        <div>
          <label className="label" htmlFor="email">
            Recipient email
          </label>
          <input
            id="email"
            type="email"
            className="input"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="btn btnPrimary"
          disabled={state === "loading" || !file || !email.trim()}
        >
          {state === "loading" ? (
            <>
              <span className="spinner" />
              Generating summary…
            </>
          ) : (
            "Generate & send summary"
          )}
        </button>
      </form>

      {state === "success" && data && (
        <div className="message messageSuccess" role="alert">
          {data.message}
          {data.rows_parsed != null && ` (${data.rows_parsed} rows parsed)`}
          {data.email_sent === false && data.email_message && (
            <div style={{ marginTop: "0.5rem", fontSize: "0.875rem" }}>
              {data.email_message}
            </div>
          )}
          {data.summary && (
            <div className="summaryBox" style={{ marginTop: "1rem" }}>
              {data.summary}
            </div>
          )}
        </div>
      )}

      {state === "error" && data?.error && (
        <div className="message messageError" role="alert">
          {data.error}
        </div>
      )}
    </main>
  );
}
