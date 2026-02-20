import Footer from "@/components/ui/footer";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>   
          {children}
          <Footer/>
      </body>
    </html>
  );
}
