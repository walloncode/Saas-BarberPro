import { Github, Instagram, Mail, ArrowUpRight } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

const Contact = () => {
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

  const contacts = [
    {
      name: 'GitHub',
      handle: 'walloncode',
      url: 'https://github.com/walloncode',
      icon: Github,
      color: 'cyan',
    },
    {
      name: 'Instagram',
      handle: '@walloncode',
      url: 'https://instagram.com/walloncode',
      icon: Instagram,
      color: 'pink',
    },
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      cyan: 'border-cyan-400 hover:border-cyan-300 hover:shadow-cyan-500/50 text-cyan-400',
      pink: 'border-pink-400 hover:border-pink-300 hover:shadow-pink-500/50 text-pink-400',
    };
    return colors[color as keyof typeof colors];
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <section id="contact" ref={sectionRef} className="min-h-screen py-20 px-4 relative overflow-hidden flex items-center">
      <div className="absolute inset-0 bg-gradient-to-b from-black via-gray-900 to-black"></div>

      <div className="relative z-10 max-w-4xl mx-auto w-full">
        <div className={`text-center mb-16 ${isVisible ? 'fade-in-up' : 'opacity-0'}`}>
          <h2 className="text-5xl md:text-6xl font-bold mb-4 glow-text">Contato</h2>
          <div className="h-1 w-24 bg-gradient-to-r from-cyan-400 to-pink-400 mx-auto rounded-full glow-bar"></div>
        </div>

        <div className={`glass-card p-8 md:p-12 ${isVisible ? 'fade-in' : 'opacity-0'}`}>
          <p className="text-center text-xl text-gray-300 mb-12">
            Vamos construir algo incrível juntos?
          </p>

          <div className="grid md:grid-cols-2 gap-6 mb-12">
            {contacts.map((contact, index) => (
              <a
                key={contact.name}
                href={contact.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`contact-card flex items-center justify-between p-6 rounded-lg border-2 ${getColorClasses(
                  contact.color
                )} bg-black/30 group transition-all duration-300 ${isVisible ? 'slide-in-up' : 'opacity-0'}`}
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <div className="flex items-center gap-4">
                  <div className="p-3 rounded-lg bg-black/50 group-hover:scale-110 transition-transform duration-300">
                    <contact.icon className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="font-semibold text-white">{contact.name}</p>
                    <p className="text-sm text-gray-400">{contact.handle}</p>
                  </div>
                </div>
                <ArrowUpRight className="w-5 h-5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              </a>
            ))}
          </div>

          <div className="text-center">
            <a
              href="mailto:wall@example.com"
              className="inline-flex items-center gap-2 px-8 py-4 bg-green-500/20 border-2 border-green-400 text-green-400 rounded-lg font-semibold hover:bg-green-500/40 hover:shadow-green-500/50 shadow-xl transition-all duration-300"
            >
              <Mail className="w-5 h-5" />
              Enviar Email
            </a>
          </div>
        </div>

        <div className="text-center mt-12">
          <button
            onClick={scrollToTop}
            className="text-cyan-400 hover:text-green-400 transition-colors duration-300 flex items-center gap-2 mx-auto"
          >
            <span>Voltar ao topo</span>
            <ArrowUpRight className="w-4 h-4 rotate-45" />
          </button>
        </div>

        <div className="text-center mt-8 text-gray-500 text-sm">
          <p>
            &copy; {new Date().getFullYear()} Wellyson (Wall). Desenvolvido com React + Vite durante uma madrugada qualquer
          </p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
