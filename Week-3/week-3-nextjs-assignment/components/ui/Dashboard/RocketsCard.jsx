import Image from "next/image";

export default function RocketsCard() {
  return (
    <div className="w-full h-full rounded-2xl overflow-hidden relative">
      
      <div  className="absolute inset-0 bg-cover bg-center"/>

      <Image src="/Rockets.png" alt="work with rockets" fill className="object-cover scale-y-120 scale-x-120" />

      <div className="absolute inset-0 bg-black/40" />

      <div className="relative h-full p-6 flex flex-col justify-between text-white max-w-[80%] ">
        <div>
        <h3 className="text-lg font-bold">
          Work with the Rockets
        </h3>

        <p className="mt-1 text-sm opacity-90">
          Wealth creation is an evolutionarily recent positive-sum game.
        </p>
        </div>

        <span className="mt-3 text-sm font-semibold">
          Read more →
        </span>
      </div>
    </div>
  );
}
