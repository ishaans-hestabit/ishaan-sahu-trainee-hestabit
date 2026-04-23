import AuthNavbar from "@/components/ui/AuthNavBar";
import SignUpBox from "@/components/ui/SignUpBox";
import Image from "next/image";

export default function SignUp() {
  return (

    <div >
        <AuthNavbar page="signup"/>
    
    <div className="w-full min-h-screen bg-white flex flex-col items-center pb-20">
      
      
      <div className="relative w-[96%] h-100 mt-4 rounded-4xl overflow-hidden flex flex-col items-center pt-24">
        <Image src="/signupBackground.png" alt="Signup Background" fill className="object-cover brightness-110" priority/>


        <div className="relative text-center px-6 ">
          <h1 className="text-white text-4xl md:text-5xl font-bold mb-4 ">
            Welcome!
          </h1>
          <p className="text-white text-sm md:text-base font-medium max-w-md mx-auto ">
            Use these awesome forms to login or create new account in your project for free.
          </p>
        </div>
      </div>

      <div className="relative z-20 -mt-48 w-full flex justify-center px-4 ">
        <SignUpBox />
      </div>

    </div>
    </div>
  );
}