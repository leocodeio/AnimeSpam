import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Landing from "./Landing";
import Anime from "./Anime";
import Error from "./Error";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/anime/:name" element={<Anime />} />
        <Route path="*" element={<Error />} />
      </Routes>
    </Router>
  );
};

export default App;
