export default function Footer() {
  return (
    <footer className="w-full px-8 py-6 flex flex-col md:flex-row justify-between items-center text-sm text-gray-400 font-medium ">
      
      <div className="mb-4 ">
        <span className="mr-1">© 2026, Made with</span>
        <span>❤️</span>
        <span className="ml-1">by</span>
        <span className="ml-1 font-bold text-primary ">Ishaan Sahu</span>
      </div>

     
      <nav className="flex gap-8">
        <span>Ishaan Sahu</span>
        <span>Simple</span>
        <span>Blog</span>
        <span>License</span>
      </nav>
    </footer>
  );
}