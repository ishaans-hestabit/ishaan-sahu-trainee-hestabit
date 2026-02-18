import AuthorCard from "./AuthorCard";
import { AUTHORS } from '../../app/tables/dummy_data.js';

export default function AuthorTable() {
  return (
    <div className="bg-white rounded-2xl p-6 pb-2 shadow-sm">
      <h1 className="text-lg font-semibold mb-6">Authors Table</h1>

      <div className="grid grid-cols-[2fr_1.5fr_1fr_1fr_0.5fr] text-xs text-gray-400 border-b pb-3 mb-4">
        <span>AUTHOR</span>
        <span>FUNCTION</span>
        <span>STATUS</span>
        <span>EMPLOYED</span>
        <span></span>
      </div>

      {AUTHORS.map((author) => (
        <AuthorCard
          key={author.email}
          {...author}
        />
      ))}
    </div>
  );
}