import React from "react";
import ButtonSlider from "../components/pc_slider/ButtonSlider";
import SmallSlider from "../components/mobile_slider/SmallSlider";

const Slider = () => {
  return (
    <div className="h-[500px] w-[1000px] z-10">
      <ButtonSlider />
      <SmallSlider />
    </div>
  );
};

export default Slider;
