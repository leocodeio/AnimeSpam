import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Landing from "./Landing";
import Anime from "./Anime";
const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/anime/:name" element={<Anime />} />
      </Routes>
    </Router>
  );
};

export default App;
