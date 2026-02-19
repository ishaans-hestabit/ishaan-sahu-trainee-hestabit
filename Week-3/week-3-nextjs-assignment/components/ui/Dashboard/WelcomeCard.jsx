import ChakraCard from "./ChakraCard";

export default function WelcomeCard() {
  return (
    <div className="h-[270px] bg-white rounded-2xl px-6 py-5 flex justify-between">
      
      <div className="flex flex-col max-w-[55%]">
        <span className="text-gray-400 text-xs font-semibold">
          Built by developers
        </span>

        <h2 className="mt-1 text-lg font-bold text-gray-700">
          Purity UI Dashboard
        </h2>

        <p className="mt-2 text-sm text-gray-400 leading-relaxed">
          From colors, cards, typography to complex elements, you will find the full documentation.
        </p>

        <span className="mt-auto text-sm font-semibold text-gray-700 cursor-pointer">
          Read more →
        </span>
      </div>

      <div className="flex items-center">
        <ChakraCard />
      </div>

    </div>
  );
}
