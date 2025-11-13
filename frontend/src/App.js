import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Collapsible from "./Collapsible";
import ReviewPage from "./ReviewPage";
import "./App.css";

function Home() {
  const education = [
    "Dhanalakshmi College Of Engineering — B.E (CSE) (2021–2025) CGPA: 8.06",
    "Sri Vishwa Vidyalaya — HSC (2021) 81%",
    "Sri Vishwa Vidyalaya — SSLC (2019) 76%",
  ];

  const skills = ["Java", "Python", "HTML", "CSS", "MySQL"];
  const certificates = [
    "AWS Cloud Foundations",
    "TCS ION Career Edge",
    "HR Skills Workshop",
  ];

  return (
    <div className="home">
      {/* ---------- Sidebar ---------- */}
      <div className="sidebar">
        <img src="/profile.jpg" alt="Profile" className="profile-pic" />
        <h2>Naveen Kumar P</h2>
        <p>Aspiring Software Developer</p>

        <div className="links">
          <a
            href="https://github.com/Naveen-NK07"
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>
          <a
            href="https://www.linkedin.com/in/naveen-kumar-905aa7265?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"
            target="_blank"
            rel="noreferrer"
          >
            LinkedIn
          </a>
        </div>

        <a href="/resume.pdf" download className="download-btn">
          Download Resume
        </a>
      </div>

      {/* ---------- Content Section ---------- */}
      <div className="content">
        <h1>Welcome!</h1>
        <p>Passionate about coding and continuous learning.</p>

        <Collapsible title="Education" items={education} />
        <Collapsible title="Skills" items={skills} />
        <Collapsible title="Certificates" items={certificates} />

        <Link to="/reviews" className="btn">
          Go to Reviews
        </Link>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/reviews" element={<ReviewPage />} />
      </Routes>
    </Router>
  );
}
