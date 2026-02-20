import "../globals.css";

export default function ({children}){
    return (
        
              <div className={`flex bg-gray-100`}>
                  <main className="flex-1">{children}</main>
              </div>
          
    )
}