
import Image from "next/image";
import SignInBox from "@/components/ui/SignInBox";
import AuthNavbar from "@/components/ui/AuthNavBar";

export default function SignIn() {
  return (

    <div>
        <AuthNavbar/>
        <div className="w-full min-h-screen flex bg-white">

        <div className="w-full  flex items-center justify-center p-8">
            <SignInBox />
        </div>

        <div className="hidden lg:block w-[70%] relative max-h-175">
            <div className=" flex h-full w-full bg-primary rounded-bl-4xl items-center justify-center">
                <Image src="/chakraLogo.png" width={200} height={200} alt="logo"></Image>
            </div>
        </div>
        </div>
    </div>
  );
}