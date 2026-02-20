import "../globals.css";

export default function ({children}){
    return (
        <html lang="en">
              <body className={`flex bg-gray-100`}>
                  <main className="flex-1">{children}</main>
              </body>
            </html>
    )
}