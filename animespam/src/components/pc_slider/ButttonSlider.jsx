import React, { useEffect, useState } from "react";
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";
import "./ButtonSlider.css";
import { items } from "../../constants";
const ButtonSlider = () => {
  const [active, setActive] = useState(1);

  const loadShow = () => {
    const itemElements = document.querySelectorAll(".slider .item");
    let stt = 0;

    itemElements[active].style.transform = "none";
    itemElements[active].style.zIndex = "1";
    itemElements[active].style.filter = "none";
    itemElements[active].style.opacity = "1";

    for (let i = active + 1; i < itemElements.length; i++) {
      stt++;
      itemElements[i].style.transform = `translateX(${120 * stt}px) scale(${
        1 - 0.2 * stt
      }) perspective(16px) rotateY(-1deg)`;
      itemElements[i].style.zIndex = `${-stt}`;
      itemElements[i].style.filter = "blur(5px)";
      itemElements[i].style.opacity = stt > 2 ? "0" : "0.6";
    }

    stt = 0;
    for (let i = active - 1; i >= 0; i--) {
      stt++;
      itemElements[i].style.transform = `translateX(${-120 * stt}px) scale(${
        1 - 0.2 * stt
      }) perspective(16px) rotateY(1deg)`;
      itemElements[i].style.zIndex = `${-stt}`;
      itemElements[i].style.filter = "blur(5px)";
      itemElements[i].style.opacity = stt > 2 ? "0" : "0.6";
    }
  };

  useEffect(() => {
    loadShow();
    // eslint-disable-next-line
  }, [active]);

  const handleNext = () => {
    setActive((prevActive) => (prevActive + 1) % items.length);
  };

  const handlePrev = () => {
    setActive((prevActive) => (prevActive - 1 + items.length) % items.length);
  };

  return (
    <div className="slider-container ">
      <div className="slider">
        <div className="btn">
          <button id="prev" onClick={handlePrev}>
            <FaArrowLeft />
          </button>
          <button id="next" onClick={handleNext}>
            <FaArrowRight />
          </button>
        </div>
        {items.map((item) => (
          <div className="item" key={item.id}>
            <img
              id={item.id}
              src={item.src}
              alt={item.alt}
              onClick={(e) => {
                e.preventDefault();
                console.log("HI");
              }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ButtonSlider;
