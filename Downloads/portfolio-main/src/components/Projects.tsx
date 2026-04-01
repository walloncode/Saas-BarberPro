import { ExternalLink, Users, Database, LayoutGrid as Layout } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

const Projects = () => {
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

  const projects = [
    {
      title: 'Kiuseven',
      description: 'projeto desenvolvido como freelancer',
      icon: Users,
      color: 'cyan',
      tags: ['Elementor', 'Figma', 'Wordpress','Html, CSS e JS','Tailwind', 'UI/UX'],
      link: 'https://www.kiuseven.com.br'
    },
    {
      title: 'WKCode',
      description: 'projeto focado em desenvolvimento e soluções digitais',
      icon: Database,
      color: 'green',
      tags: ['Elementor', 'Figma', 'Wordpress','Html, CSS e Js', 'UI/UX'],
      link: 'https://www.wkcode.com.br'
    },
    {
      title: 'Interfaces UI',
      description: 'Inspiradas em Facebook e Starbucks',
      icon: Layout,
      color: 'pink',
      tags: ['HTML, CSS e JS','Tailwind', 'UI/UX'],
    },
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      cyan: 'border-cyan-400 hover:border-cyan-300 hover:shadow-cyan-500/50',
      green: 'border-green-400 hover:border-green-300 hover:shadow-green-500/50',
      pink: 'border-pink-400 hover:border-pink-300 hover:shadow-pink-500/50',
    };
    return colors[color as keyof typeof colors];
  };

  const getIconColor = (color: string) => {
    const colors = {
      cyan: 'text-cyan-400 bg-cyan-500/20',
      green: 'text-green-400 bg-green-500/20',
      pink: 'text-pink-400 bg-pink-500/20',
    };
    return colors[color as keyof typeof colors];
  };

  const getTagColor = (color: string) => {
    const colors = {
      cyan: 'bg-cyan-500/20 text-cyan-400 border-cyan-400/30',
      green: 'bg-green-500/20 text-green-400 border-green-400/30',
      pink: 'bg-pink-500/20 text-pink-400 border-pink-400/30',
    };
    return colors[color as keyof typeof colors];
  };

  return (
    <section id="projects" ref={sectionRef} className="min-h-screen py-20 px-4 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-black via-gray-900 to-black"></div>

      <div className="relative z-10 max-w-6xl mx-auto">
        <div className={`text-center mb-16 ${isVisible ? 'fade-in-up' : 'opacity-0'}`}>
          <h2 className="text-5xl md:text-6xl font-bold mb-4 glow-text">Projetos</h2>
          <div className="h-1 w-24 bg-gradient-to-r from-cyan-400 via-green-400 to-pink-400 mx-auto rounded-full glow-bar"></div>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {projects.map((project, index) => (
            <a
              href={project.link}
              target="_blank"
              rel="noopener noreferrer"
              key={project.title}
              className={`project-card glass-card p-6 border-2 ${getColorClasses(project.color)} group cursor-pointer ${
                isVisible ? 'slide-in-up' : 'opacity-0'
              }`}
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <div className="flex flex-col h-full">
                <div className={`p-4 rounded-lg ${getIconColor(project.color)} w-fit mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  <project.icon className="w-8 h-8" />
                </div>

                <h3 className="text-2xl font-bold mb-3 text-white group-hover:glow-text transition-all duration-300">
                  {project.title}
                </h3>

                <p className="text-gray-400 mb-4 flex-grow">{project.description}</p>

                <div className="flex flex-wrap gap-2 mb-4">
                  {project.tags.map((tag) => (
                    <span
                      key={tag}
                      className={`px-3 py-1 rounded-full text-xs border ${getTagColor(project.color)}`}
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="flex items-center gap-2 text-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <ExternalLink className="w-4 h-4" />
                  <span>Ver detalhes</span>
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Projects;