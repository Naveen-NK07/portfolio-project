import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Collapsible from "./Collapsible";
import ReviewPage from "./ReviewPage";
import "./App.css";

const BASE_URL = "https://portfolio-project-2o22.onrender.com";

function Home() {
  const [personal, setPersonal] = useState({});
  const [education, setEducation] = useState([]);
  const [skills, setSkills] = useState([]);
  const [certificates, setCertificates] = useState([]);

  // ⬇⬇ NEW — Retry function to handle Render cold start
  async function fetchWithRetry(url, retries = 6) {
    for (let i = 0; i < retries; i++) {
      try {
        const response = await fetch(url);
        if (response.ok) return await response.json();
      } catch (error) {
        console.log(`Retrying: ${url}`);
      }
      await new Promise((r) => setTimeout(r, 2000)); // wait 2 seconds
    }
    return null;
  }

  useEffect(() => {
    async function loadData() {
      // PERSONAL INFO
      const p = await fetchWithRetry(`${BASE_URL}/api/personal-info`);
      if (p) setPersonal(p);

      // EDUCATION
      const edu = await fetchWithRetry(`${BASE_URL}/api/education`);
      if (edu) {
        setEducation(
          edu.map(
            (e) =>
              `${e.institution} — ${e.degree} (${e.start_year}–${e.end_year}) ${e.grade}`
          )
        );
      }

      // SKILLS
      const skl = await fetchWithRetry(`${BASE_URL}/api/skills`);
      if (skl) {
        setSkills(skl.map((s) => `${s.skill_name} (${s.proficiency})`));
      }

      // CERTIFICATES
      const cert = await fetchWithRetry(`${BASE_URL}/api/certificates`);
      if (cert) {
        setCertificates(
          cert.map(
            (c) =>
              `${c.certificate_name} — ${c.issuer} (${c.issue_year})`
          )
        );
      }
    }

    loadData();
  }, []);

  return (
    <div className="home">
      {/* Sidebar */}
      <div className="sidebar">
        <img src="/profile.jpg" alt="Profile" className="profile-pic" />

        <h2>{personal.full_name}</h2>
        <p>{personal.headline}</p>
        <p>
          Email: <a href={`mailto:${personal.email}`}>{personal.email}</a>
        </p>
        <p>Phone: {personal.phone}</p>

        <div className="links">
          <a href="https://github.com/Naveen-NK07" target="_blank" rel="noreferrer">
            GitHub
          </a>
          <a
            href="https://www.linkedin.com/in/naveen-kumar-905aa7265"
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

      {/* Content */}
      <div className="content">
        <h1>Welcome!</h1>

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
