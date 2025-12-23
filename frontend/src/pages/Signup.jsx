import React, { useState } from "react";

const Signup = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGoogleSignup = async () => {
    try {
      setLoading(true);
      setError("");

      // Call your FastAPI backend
      const res = await fetch("http://localhost:9000/auth/google/login", {
        credentials: "include", // just in case you set cookies later
      });

      if (!res.ok) {
        throw new Error("Failed to start Google login");
      }

      const data = await res.json();

      if (!data.auth_url) {
        throw new Error("No auth_url returned from backend");
      }

      // Redirect browser to Google
      window.location.href = data.auth_url;
    } catch (err) {
      console.error(err);
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Please Signup</h1>

      <button onClick={handleGoogleSignup} disabled={loading}>
        {loading ? "Redirecting to Google..." : "Continue with Google"}
      </button>

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}
    </div>
  );
};

export default Signup;
