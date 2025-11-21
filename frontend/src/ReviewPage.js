import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./App.css";

export default function ReviewPage() {
  const navigate = useNavigate();

  const BASE_URL = "https://portfolio-project-2o22.onrender.com";

  const [form, setForm] = useState({
    name: "",
    email: "",
    message: "",
    rating: 5,
  });

  const [reviews, setReviews] = useState([]);

  // Load all reviews
  useEffect(() => {
    axios
      .get(`${BASE_URL}/api/reviews`)
      .then((res) => setReviews(res.data))
      .catch((err) => console.error("Error loading reviews:", err));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Submit review
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.name || !form.email || !form.message) {
      alert("Please fill all fields.");
      return;
    }

    try {
      await axios.post(`${BASE_URL}/api/reviews`, form);

      alert("Review submitted!");

      // Reload reviews list
      const res = await axios.get(`${BASE_URL}/api/reviews`);
      setReviews(res.data);

      // Reset form
      setForm({ name: "", email: "", message: "", rating: 5 });
    } catch (err) {
      console.error("Submit error:", err);
      alert("Failed to submit review.");
    }
  };

  return (
    <div className="review-page">
      <h2>Leave a Review</h2>

      <form onSubmit={handleSubmit}>
        <input
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
        />

        <input
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
        />

        <textarea
          name="message"
          placeholder="Message"
          value={form.message}
          onChange={handleChange}
        ></textarea>

        <div>
          Rating:{" "}
          {[1, 2, 3, 4, 5].map((n) => (
            <span
              key={n}
              className={n <= form.rating ? "star filled" : "star"}
              onClick={() => setForm({ ...form, rating: n })}
            >
              ★
            </span>
          ))}
        </div>

        <button type="submit">Submit</button>
      </form>

      <h3>All Reviews</h3>

      {reviews.map((r) => (
        <div key={r.id} className="review">
          <strong>{r.name}</strong> ({r.rating}★)
          <p>{r.message}</p>
        </div>
      ))}

      <div style={{ textAlign: "center", marginTop: "40px" }}>
        <button onClick={() => navigate("/")}>Back to Profile</button>
      </div>
    </div>
  );
}
