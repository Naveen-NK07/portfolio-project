import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

export default function ReviewPage() {
  const [form, setForm] = useState({ name: "", email: "", message: "", rating: 5 });
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/api/reviews").then(res => setReviews(res.data));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post("http://localhost:5000/api/review", form);
    alert("Review submitted!");
    const res = await axios.get("http://localhost:5000/api/reviews");
    setReviews(res.data);
    setForm({ name: "", email: "", message: "", rating: 5 });
  };

  return (
    <div className="review-page">
      <h2>Leave a Review</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" value={form.name} onChange={handleChange} />
        <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
        <textarea name="message" placeholder="Message" value={form.message} onChange={handleChange}></textarea>
        <div>
          Rating:{" "}
          {[1, 2, 3, 4, 5].map((n) => (
            <span
              key={n}
              className={form.rating >= n ? "star filled" : "star"}
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
    </div>
  );
}
