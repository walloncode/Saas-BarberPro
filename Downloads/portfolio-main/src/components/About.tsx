import { Briefcase, Code, Database, BookOpen, Lightbulb, Headphones as HeadphonesIcon } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

const About = () => {
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

  const experiences = [
    { icon: HeadphonesIcon, text: 'Experiência em suporte técnico' },
    { icon: Code, text: 'Desenvolvimento de sistemas' },
    { icon: Database, text: 'Integração de dados escolares' },
    { icon: Briefcase, text: 'Experiência com APIs e interfaces modernas' },
    { icon: BookOpen, text: 'Experiência dando aulas de HTML e CSS' },
    { icon: Lightbulb, text: 'Participação em projetos de inovação e empreendedorismo' },
  ];

  return (
    <section id="about" ref={sectionRef} className="min-h-screen py-20 px-4 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-black via-gray-900 to-black"></div>

      <div className="relative z-10 max-w-6xl mx-auto">
        <div className={`text-center mb-16 ${isVisible ? 'fade-in-up' : 'opacity-0'}`}>
          <h2 className="text-5xl md:text-6xl font-bold mb-4 glow-text">Sobre Mim</h2>
          <div className="h-1 w-24 bg-gradient-to-r from-cyan-400 to-green-400 mx-auto rounded-full glow-bar"></div>
        </div>

        <div className={`glass-card p-8 md:p-12 ${isVisible ? 'slide-in-left' : 'opacity-0'}`}>
          <div className="grid md:grid-cols-2 gap-6">
            {experiences.map((exp, index) => (
              <div
                key={index}
                className="flex items-start gap-4 group hover:translate-x-2 transition-transform duration-300"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="flex-shrink-0 p-3 rounded-lg bg-cyan-500/10 border border-cyan-400/30 group-hover:border-cyan-400 group-hover:shadow-neon transition-all duration-300">
                  <exp.icon className="w-6 h-6 text-cyan-400" />
                </div>
                <p className="text-gray-300 pt-3 group-hover:text-white transition-colors duration-300">
                  {exp.text}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
