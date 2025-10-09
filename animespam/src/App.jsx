import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import Landing from "./Landing";
import Anime from "./Anime";
import Error from "./Error";

const App = () => {
  return (
    <Router>
      <Helmet>
        <meta
          name="google-site-verification"
          content="qo-ybTK5umqiB8sENeyeypQ6OdMtDTGg1cY6-JVhmxI"
        />
      </Helmet>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/anime/:name" element={<Anime />} />
        <Route path="*" element={<Error />} />
      </Routes>
    </Router>
  );
};

export default App;
