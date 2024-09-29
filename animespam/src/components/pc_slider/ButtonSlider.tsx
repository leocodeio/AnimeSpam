import React, { useEffect, useState } from "react";
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";
import "./ButtonSlider.css";

// Define the item type
interface SliderItem {
  id: string;
  src: string;
  alt: string;
}

const ButtonSlider: React.FC = () => {
  const items: SliderItem[] = [
    { id: "ani1", src: "artifacts/comingsoon.jpg", alt: "Coming Soon" },
    { id: "ani2", src: "artifacts/comingsoon.jpg", alt: "Coming Soon" },
    { id: "onepiece", src: "artifacts/luffy.jpg", alt: "Luffy" },
    { id: "sololevel", src: "artifacts/sololev.jpg", alt: "Solo Leveling" },
    { id: "naruto", src: "artifacts/naruto.jpg", alt: "Naruto" },
    { id: "jjk", src: "artifacts/jjk.png", alt: "Jujutsu Kaisen" },
    { id: "sololevel2", src: "artifacts/comingsoon.jpg", alt: "Coming Soon" },
  ];

  const [active, setActive] = useState<number>(3);

  const loadShow = (): void => {
    const itemElements = document.querySelectorAll(
      ".slider .item"
    ) as NodeListOf<HTMLElement>;
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
  }, [active]); // Run loadShow whenever active changes

  const handleNext = (): void => {
    setActive((prevActive) => (prevActive + 1) % items.length);
  };

  const handlePrev = (): void => {
    setActive((prevActive) => (prevActive - 1 + items.length) % items.length);
  };

  return (
    <div className="container">
      <div className="btn">
        <button id="prev" onClick={handlePrev}>
          <FaArrowLeft />
        </button>
        <button id="next" onClick={handleNext}>
          <FaArrowRight />
        </button>
      </div>

      <div className="slider">
        {items.map((item) => (
          <div className="item" key={item.id}>
            <img id={item.id} src={item.src} alt={item.alt} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ButtonSlider;
