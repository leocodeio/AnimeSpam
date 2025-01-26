import React from "react";
import ButtonSlider from "./pc_slider/ButttonSlider";
import SmallSlider from "./mobile_slider/SmallSlider";
import Heading from "./Heading";

const Slider = () => {
  return (
    <div className="m-10 my-32" id="slider">
      <Heading tag="Get started with AnimeSpam" title="Select anime and download Twixtors" />
      <ButtonSlider />
      <SmallSlider />
    </div>
  );
};

export default Slider;
