import React, { useState } from "react";
import "./App.css";

export default function Collapsible({ title, items }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="collapsible">
      <div className="collapsible-header" onClick={() => setOpen(!open)}>
        <h3>{title}</h3>
        <span>{open ? "−" : "+"}</span>
      </div>
      {open && (
        <ul className="collapsible-body">
          {items.map((it, idx) => (
            <li key={idx}>{it}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
