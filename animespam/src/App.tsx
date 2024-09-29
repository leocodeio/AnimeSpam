import React from "react";
import Slider from "./components/mobile_slider/slider";
import ButtonSlider from "./components/pc_slider/ButtonSlider";

const App: React.FC = () => {
  return (
    <div className="h-screen flex flex-col items-center justify-center">
      <p className="text-3xl font-bold text-blue-600">
        Hello, React with Tailwind and TypeScript!
      </p>
      <div className="h-[500px] w-[500px]  sm:hidden">
        <Slider />
      </div>
      <div className="h-[500px] w-[1000px] z-10 hidden sm:block">
        <ButtonSlider />
      </div>
    </div>
  );
};

export default App;
