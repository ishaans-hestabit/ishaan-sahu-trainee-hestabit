export default function ChakraCard() {
  return (
    <div className="h-[200px] w-[200px] bg-primary rounded-2xl flex items-center justify-center text-white">
      <div className="flex items-center gap-2">
        <div className="h-9 w-9 rounded-full bg-white/20 flex items-center justify-center">
          ⚡
        </div>
        <span className="text-lg font-semibold">chakra</span>
      </div>
    </div>
  );
}
