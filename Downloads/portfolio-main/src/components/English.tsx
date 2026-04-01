import { Languages, BookOpen, MessageCircle, TrophyIcon } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

const English = () => {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.1 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => {
      if (sectionRef.current) {
        observer.unobserve(sectionRef.current);
      }
    };
  }, []);

  const features = [
    { icon: Languages, text: 'Nível intermediário' },
    { icon: BookOpen, text: 'Boa leitura técnica' },
    { icon: MessageCircle, text: 'Boa comunicação' },
    { icon: TrophyIcon, text: 'Nivel B1/B2' }
  ];

  return (
    <section id="english" ref={sectionRef} className="min-h-screen py-20 px-4 relative overflow-hidden flex items-center">
      <div className="absolute inset-0 bg-gradient-to-b from-black via-gray-900 to-black"></div>

      <div className="relative z-10 max-w-4xl mx-auto w-full">
        <div className={`text-center mb-16 ${isVisible ? 'fade-in-up' : 'opacity-0'}`}>
          <h2 className="text-5xl md:text-6xl font-bold mb-4 glow-text">Inglês</h2>
          <div className="h-1 w-24 bg-gradient-to-r from-pink-400 to-cyan-400 mx-auto rounded-full glow-bar"></div>
        </div>

        <div className={`glass-card-highlight p-8 md:p-12 border-2 border-green-400/50 ${isVisible ? 'scale-in' : 'opacity-0'}`}>
          <div className="flex flex-col items-center gap-8">
            <div className="p-6 rounded-full bg-green-500/20 border-2 border-green-400 glow-icon">
              <Languages className="w-16 h-16 text-green-400" />
            </div>

            <div className="space-y-6 w-full">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="flex items-center gap-4 p-4 rounded-lg bg-black/30 border border-green-400/30 hover:border-green-400 hover:bg-green-500/10 transition-all duration-300 group"
                >
                  <div className="p-3 rounded-lg bg-green-500/20 border border-green-400/50 group-hover:scale-110 transition-transform duration-300">
                    <feature.icon className="w-6 h-6 text-green-400" />
                  </div>
                  <span className="text-lg text-gray-300 group-hover:text-white transition-colors duration-300">
                    {feature.text}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default English;
