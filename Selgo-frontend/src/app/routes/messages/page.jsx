import Header from "@/components/layout/Header";
import Messages from "@/components/layout/header-compoents/Messages";

export default function MessagePage() {
  return (
    <div className="flex flex-col h-screen">
      {/* Fixed Header */}
      <Header />

      {/* Push Messages below the fixed header */}
      <div className="pt-16 flex-1 overflow-hidden">
        <Messages />
      </div>
    </div>
  );
}