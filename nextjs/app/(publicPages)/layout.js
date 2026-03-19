import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function Layout({ children }) {
    return (
        <div className="flex flex-col min-h-screen bg-[#121212]">
            <Navbar />
            <div className="flex-1 w-full">
                {children}
            </div>
            <Footer />
        </div>
    );
}