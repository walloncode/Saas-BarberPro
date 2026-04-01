import { Code2, Palette, Server, Boxes, Database, Headphones as HeadphonesIcon, Globe } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

const Skills = () => {
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

  const skills = [
    { name: 'HTML', icon: Code2, color: 'cyan' },
    { name: 'CSS', icon: Palette, color: 'green' },
    { name: 'JavaScript', icon: Code2, color: 'pink' },
    { name: 'React', icon: Boxes, color: 'cyan' },
    { name: 'Node.js', icon: Server, color: 'green' },
    { name: 'APIs', icon: Globe, color: 'pink' },
    { name: 'Banco de Dados', icon: Database, color: 'cyan' },
    { name: 'Suporte Técnico', icon: HeadphonesIcon, color: 'green' },
    { name: 'WordPress', icon: Globe, color: 'pink' },
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      cyan: 'border-cyan-400 text-cyan-400 hover:shadow-cyan-500/50',
      green: 'border-green-400 text-green-400 hover:shadow-green-500/50',
      pink: 'border-pink-400 text-pink-400 hover:shadow-pink-500/50',
    };
    return colors[color as keyof typeof colors];
  };

  return (
    <section id="skills" ref={sectionRef} className="min-h-screen py-20 px-4 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-black via-gray-900 to-black"></div>

      <div className="relative z-10 max-w-6xl mx-auto">
        <div className={`text-center mb-16 ${isVisible ? 'fade-in-up' : 'opacity-0'}`}>
          <h2 className="text-5xl md:text-6xl font-bold mb-4 glow-text">Competências</h2>
          <div className="h-1 w-24 bg-gradient-to-r from-green-400 to-pink-400 mx-auto rounded-full glow-bar"></div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          {skills.map((skill, index) => (
            <div
              key={skill.name}
              className={`skill-card glass-card p-6 flex flex-col items-center gap-4 group cursor-pointer border-2 ${getColorClasses(
                skill.color
              )} ${isVisible ? 'scale-in' : 'opacity-0'}`}
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="p-4 rounded-full bg-black/50 group-hover:scale-110 transition-transform duration-300">
                <skill.icon className="w-8 h-8" />
              </div>
              <span className="font-semibold text-center">{skill.name}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Skills;
