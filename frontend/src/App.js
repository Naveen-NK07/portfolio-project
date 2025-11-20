import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Collapsible from "./Collapsible";
import ReviewPage from "./ReviewPage";
import "./App.css";

function Home() {
  const [personal, setPersonal] = useState({});
  const [education, setEducation] = useState([]);
  const [skills, setSkills] = useState([]);
  const [certificates, setCertificates] = useState([]);

  useEffect(() => {
    // PERSONAL INFO
    fetch("http://localhost:5000/api/personal-info")
      .then(res => res.json())
      .then(data => setPersonal(data));

    // EDUCATION
    fetch("http://localhost:5000/api/education")
      .then(res => res.json())
      .then(data => {
        const formatted = data.map(e =>
          `${e.institution} — ${e.degree} (${e.start_year}–${e.end_year}) ${e.grade}`
        );
        setEducation(formatted);
      });

    // SKILLS
    fetch("http://localhost:5000/api/skills")
      .then(res => res.json())
      .then(data => {
        const formatted = data.map(s => `${s.skill_name} (${s.proficiency})`);
        setSkills(formatted);
      });

    // CERTIFICATES
    fetch("http://localhost:5000/api/certificates")
      .then(res => res.json())
      .then(data => {
        const formatted = data.map(c =>
          `${c.certificate_name} — ${c.issuer} (${c.issue_year})`
        );
        setCertificates(formatted);
      });
  }, []);

  return (
    <div className="home">
      {/* Sidebar */}
      <div className="sidebar">
        <img src="/profile.jpg" alt="Profile" className="profile-pic" />

        <h2>{personal.full_name}</h2>
        <p>{personal.headline}</p>
        <p>Email:{" "}
              <a href={`mailto:${personal.email}`}>{personal.email}</a>
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

        <Link to="/reviews" className="btn">Go to Reviews</Link>
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
