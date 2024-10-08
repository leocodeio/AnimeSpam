// Import Swiper React components
import { Swiper, SwiperSlide } from "swiper/react";

// Import Swiper styles
import "swiper/css";
import "swiper/css/effect-cards";

import "./SmallSlider.css";

// import required modules
import { EffectCards } from "swiper/modules";
import { items } from "../../constants";
import { useNavigate } from "react-router-dom";

const SmallSlider = () => {
  const navigate = useNavigate();
  return (
    <>
      <Swiper
        effect="cards"
        grabCursor={true}
        modules={[EffectCards]}
        className="mySwiper"
        autoplay
      >
        {items.map((item) => (
          <SwiperSlide key={item.id}>
            <div className="item">
              <img
                id={item.id}
                src={item.src}
                alt={item.alt}
                onClick={(e) => {
                  e.preventDefault();
                  navigate(`/anime/${item.alt}`);
                  console.log("HI");
                }}
              />
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </>
  );
};

export default SmallSlider;
