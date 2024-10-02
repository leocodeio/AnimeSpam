import React from "react";
import Slider from "./main/Slider";
import Header from "./main/Header";

const App: React.FC = () => {
  return (
    <div className="bg-gray-900 h-screen">
      <Header />
      

      <div className="flex items-center justify-center">
        <Slider />
      </div>
      
    </div>
  );
};

export default App;
