import React from "react";
import Slider from "./components/slider";

const App: React.FC = () => {
  return (
    <div className="h-screen flex items-center justify-center bg-blue-100">
      <p className="text-3xl font-bold text-blue-600">
        Hello, React with Tailwind and TypeScript!
      </p>
      <Slider />
    </div>
  );
};

export default App;
