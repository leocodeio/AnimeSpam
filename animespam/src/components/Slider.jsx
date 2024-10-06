import React from "react";
import ButtonSlider from "./pc_slider/ButttonSlider";
import SmallSlider from "./mobile_slider/SmallSlider";

const Slider = () => {
  return (
    <div className="m-10 mt-32">
      <ButtonSlider />
      <SmallSlider />
    </div>
  );
};

export default Slider;
