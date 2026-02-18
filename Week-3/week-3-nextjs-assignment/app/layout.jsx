import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/ui/Sidebar/Sidebar";



export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`flex bg-gray-100`}>
          <Sidebar></Sidebar>
          {/* the navbar is not used here because we need to pass differnt props for each page so we have implemented that in the page.jsx for this reason */}
          <main className="flex-1">{children}</main>
      </body>
    </html>
  );
}
