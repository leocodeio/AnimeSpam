import {
  benefitIcon1,
  benefitIcon2,
  benefitIcon3,
  benefitIcon4,
  benefitImage2,
  chromecast,
  disc02,
  discord,
  discordBlack,
  facebook,
  figma,
  file02,
  framer,
  homeSmile,
  instagram,
  notification2,
  notification3,
  notification4,
  notion,
  photoshop,
  plusSquare,
  protopie,
  raindrop,
  recording01,
  recording03,
  roadmap1,
  roadmap2,
  roadmap3,
  roadmap4,
  searchMd,
  slack,
  sliders04,
  telegram,
  twitter,
  yourlogo,
} from "../assets";

export const navigation = [
  {
    id: "0",
    title: "Twixtors",
    url: "#slider",
  },
  {
    id: "1",
    title: "Upscale",
    url: "#pricing",
  },
  // {
  //   id: "2",
  //   title: "How to use",
  //   url: "#how-to-use",
  // },
  // {
  //   id: "3",
  //   title: "How to use",
  //   url: "#roadmap",
  // },
  {
    id: "4",
    title: "New account",
    url: "#signup",
    onlyMobile: true,
  },
  {
    id: "5",
    title: "Sign in",
    url: "#login",
    onlyMobile: true,
  },
];

export const heroIcons = [homeSmile, file02, searchMd, plusSquare];

export const notificationImages = [notification4, notification3, notification2];

export const companyLogos = [yourlogo, yourlogo, yourlogo, yourlogo, yourlogo];

export const brainwaveServices = [
  "Photo generating",
  "Photo enhance",
  "Seamless Integration",
];

export const brainwaveServicesIcons = [
  recording03,
  recording01,
  disc02,
  chromecast,
  sliders04,
];

export const roadmap = [
  {
    id: "0",
    title: "Voice recognition",
    text: "Enable the chatbot to understand and respond to voice commands, making it easier for users to interact with the app hands-free.",
    date: "May 2023",
    status: "done",
    imageUrl: roadmap1,
    colorful: true,
  },
  {
    id: "1",
    title: "Gamification",
    text: "Add game-like elements, such as badges or leaderboards, to incentivize users to engage with the chatbot more frequently.",
    date: "May 2023",
    status: "progress",
    imageUrl: roadmap2,
  },
  {
    id: "2",
    title: "Chatbot customization",
    text: "Allow users to customize the chatbot's appearance and behavior, making it more engaging and fun to interact with.",
    date: "May 2023",
    status: "done",
    imageUrl: roadmap3,
  },
  {
    id: "3",
    title: "Integration with APIs",
    text: "Allow the chatbot to access external data sources, such as weather APIs or news APIs, to provide more relevant recommendations.",
    date: "May 2023",
    status: "progress",
    imageUrl: roadmap4,
  },
];

export const collabText =
  "With smart automation and top-notch security, it's the perfect solution for teams looking to work smarter.";

export const collabContent = [
  {
    id: "0",
    title: "Seamless Integration",
    text: collabText,
  },
  {
    id: "1",
    title: "Smart Automation",
  },
  {
    id: "2",
    title: "Top-notch Security",
  },
];

export const collabApps = [
  {
    id: "0",
    title: "Figma",
    icon: figma,
    width: 26,
    height: 36,
  },
  {
    id: "1",
    title: "Notion",
    icon: notion,
    width: 34,
    height: 36,
  },
  {
    id: "2",
    title: "Discord",
    icon: discord,
    width: 36,
    height: 28,
  },
  {
    id: "3",
    title: "Slack",
    icon: slack,
    width: 34,
    height: 35,
  },
  {
    id: "4",
    title: "Photoshop",
    icon: photoshop,
    width: 34,
    height: 34,
  },
  {
    id: "5",
    title: "Protopie",
    icon: protopie,
    width: 34,
    height: 34,
  },
  {
    id: "6",
    title: "Framer",
    icon: framer,
    width: 26,
    height: 34,
  },
  {
    id: "7",
    title: "Raindrop",
    icon: raindrop,
    width: 38,
    height: 32,
  },
];

export const pricing = [
  {
    id: "0",
    title: "Basic",
    description: "Download upscaled Twixtor clips",
    price: "0",
    features: [
      "Download upscaled Twixtor clips without any cost",
      "Create free account to download 4k clips",
      "Use the clips without any watermarks",
    ],
  },
  {
    id: "1",
    title: "Premium",
    description: "Download upscaled Twixtor clips with premium features",
    price: "9.99",
    features: [
      "Upscale your own video through AnimeSpam dashboard",
      "Calulate the quality score of you video",
      "Direct contact with admin to get you own personolized upscaled clips",
    ],
  },
  // {
  //   id: "2",
  //   title: "Enterprise",
  //   description: "Custom AI chatbot, advanced analytics, dedicated account",
  //   price: null,
  //   features: [
  //     "An AI chatbot that can understand your queries",
  //     "Personalized recommendations based on your preferences",
  //     "Ability to explore the app and its features without any cost",
  //   ],
  // },
];

export const socials = [
  {
    id: "0",
    title: "Discord",
    iconUrl: discordBlack,
    url: "https://discord.gg/H99Fb9QH",
  },
  {
    id: "1",
    title: "Twitter",
    iconUrl: twitter,
    url: "https://x.com/leocodeio",
  },
  {
    id: "2",
    title: "Instagram",
    iconUrl: instagram,
    url: "https://www.instagram.com/animeleo_leo/",
  },
  {
    id: "3",
    title: "Telegram",
    iconUrl: telegram,
    url: "#",
  },
  {
    id: "4",
    title: "Facebook",
    iconUrl: facebook,
    url: "#",
  },
];

export const items = [
  {
    id: "onepiece",
    src: "/assets/slider/artifacts/luffy.jpg",
    alt: "one piece",
  },
  {
    id: "sololevel",
    src: "/assets/slider/artifacts/sololev.jpg",
    alt: "Solo Leveling",
  },
  {
    id: "naruto",
    src: "/assets/slider/artifacts/naruto.jpg",
    alt: "naruto",
  },
  {
    id: "jjk",
    src: "/assets/slider/artifacts/jjk.png",
    alt: "Jujutsu Kaisen",
  },
  {
    id: "sololevel2",
    src: "/assets/slider/artifacts/comingsoon.jpg",
    alt: "Coming Soon",
  },
  {
    id: "ani1",
    src: "/assets/slider/artifacts/comingsoon.jpg",
    alt: "Coming Soon",
  },
  {
    id: "ani2",
    src: "/assets/slider/artifacts/comingsoon.jpg",
    alt: "Coming Soon",
  },
];

export const benefits = [
  {
    id: "0",
    title: "Ask anything",
    text: "Lets users quickly find answers to their questions without having to search through multiple sources.",
    backgroundUrl: "/assets/benefits/card-1.svg",
    iconUrl: benefitIcon1,
    imageUrl: benefitImage2,
  },
  {
    id: "1",
    title: "Improve everyday",
    text: "The app uses natural language processing to understand user queries and provide accurate and relevant responses.",
    backgroundUrl: "/assets/benefits/card-2.svg",
    iconUrl: benefitIcon2,
    imageUrl: benefitImage2,
    light: true,
  },
  {
    id: "2",
    title: "Connect everywhere",
    text: "Connect with the AI chatbot from anywhere, on any device, making it more accessible and convenient.",
    backgroundUrl: "/assets/benefits/card-3.svg",
    iconUrl: benefitIcon3,
    imageUrl: benefitImage2,
  },
  {
    id: "3",
    title: "Fast responding",
    text: "Lets users quickly find answers to their questions without having to search through multiple sources.",
    backgroundUrl: "/assets/benefits/card-4.svg",
    iconUrl: benefitIcon4,
    imageUrl: benefitImage2,
    light: true,
  },
  {
    id: "4",
    title: "Ask anything",
    text: "Lets users quickly find answers to their questions without having to search through multiple sources.",
    backgroundUrl: "/assets/benefits/card-5.svg",
    iconUrl: benefitIcon1,
    imageUrl: benefitImage2,
  },
  {
    id: "5",
    title: "Improve everyday",
    text: "The app uses natural language processing to understand user queries and provide accurate and relevant responses.",
    backgroundUrl: "/assets/benefits/card-6.svg",
    iconUrl: benefitIcon2,
    imageUrl: benefitImage2,
  },
];

export const animeContent = {
  "SOLO LEVELING": [
    {
      id: 0,
      title: "Solo Leveling",
      text: "Solo Leveling Episode 6 - 4K Upscaled",
      videoUrl:
        "https://download1321.mediafire.com/5msjxdv9cx2giQxO3QviBr8YM6F3-VpJG6f4b8QqBVOnEzLvnrcn9iGUeXo6gyA-RIySXfx7Xmq__65xjJ7bIhSRTy87qTaNUThyy25KaIRJUCBOxh8Nxf1IwITLh17Y_aOwnIU2L3ZJEUVyfr0a4sjQGcqG2Y_9sLkCgNI4RZPTkGo/4axdn7dcv4288va/sololeving_ep6_4k_upscaled.mp4",
      iconUrl: benefitIcon2,
      imageUrl: "/assets/slider/artifacts/sololev.jpg",
      light: true,
    },
  ],
  NARUTO: [
    {
      id: 1,
      title: "Obito 4K-Upscaled Twixtor",
      videoUrl:
        "https://download1334.mediafire.com/0r54368dqqbg1B_kDQiXRwxTeTpeygs0szjcx_DLEkoKzRcenLBT06XzMCkEjhT-O_uNeKoc5ITRb_LxjUiOlUbI0ymuG2_fEd1v46h9PnfAJg93QK0kCuFdp21aJFlHrpCoghY9GzGla72c1POVu45E0l5RP7_et7dkKpMkfZtvHvSG/kpa8ogv1d4dwin4/obito_twixtor_4k_upscaled.mp4",
      imageUrl: "/assets/slider/artifacts/naruto/obito.jpg",
      description: "Naruto Obito 4K Upscaled Twixtor",
    },
  ],
  "ONE PIECE": [
    {
      id: 1,
      title: "Luffy Gear 5 Ep 1070+ 4K-Upscaled Twixtor",
      videoUrl:
        "https://download1590.mediafire.com/c7gav8l90t6gqz3dV11W5pnGGYbvZsRVKfDTiRzW_-rF37e8-9op-MYbyOen23rDqCmStvlYBsnPCesE0S6QUn6ZiBrjmKtLu51VXBGMuZ2mEAA1d06IZ7MfApmmaLoPKxvOi7ktoXWCkr49Muqvfh39C_V5XwyUL9r4L-5g_EKCWVQ/ecx3pjvl9z30amb/luffy_gear5_ep1070%2B_4k_upscaled.mp4",
        imageUrl: "/assets/slider/artifacts/onepiece/luffy_sample.png",
      description: "One Piece Luffy Gear 5 4K Upscaled",
    },
    {
      id: 2,
      title: "Zoro 4K-Upscaled Twixtor",
      videoUrl:
        "https://download1585.mediafire.com/bcmuyqhog5wgRBF4xIlt4u-RSKcvTJr4V-mRAvsnah4eyPCGa0iN4EKPRG8nXQb7dh7vM3TVjZlfq_aplM-RqdhGBF5_Z_KQNAzqd9awzZnx7EFMEsZUgFKlBNkb40yImeY0Zu09gwOi7WCkJqd3505nt4yjNuTmHiJTmgavV26K8AID/6gsbd2svuqw2udn/zoro_twixtor_4k.mp4",
      imageUrl: "/assets/slider/artifacts/onepiece/zoro.jpg",
      description: "One Piece Zoro 4K Upscaled Twixtor",
    },
  ],
  "JUJUTSU KAISEN": [
    {
      id: 1,
      title: "Sukuna 4K-Upscaled Twixtor",
      videoUrl:
        "https://download1336.mediafire.com/748e06x45kagcqBtPNajsjQtYq2EMZjKYVR2Igo-7d5B5AgdyIPbrH-qwWij4quxDXTe64nc4oE50TLBDZhF7k91zzy7rcdJJHaUv00fa5D8PbAK_yKSkfvk8zzcQzQaK9Th7zjwLNmzH6Xpm1sPxiRXGRMPj475iBPyg2UAMjNFKVhU/ohnu35cv1ii6f7u/sukuna_upscaled_twixtor.mp4",
      imageUrl: "/assets/slider/artifacts/jjk/sukuna.jpg",
      description: "Jujutsu Kaisen Sukuna 4K Upscaled Twixtor",
    },
  ],
};
