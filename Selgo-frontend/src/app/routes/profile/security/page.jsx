import SecuritySection from "@/components/profile/SecuritySettings";
const securityData = {
  title: "Security",
  description:
    "Did you know that you can secure your account even more? On this page you will find various security measures that can be used for a safe and secure experience at FINN.",
  buttonText: "Bank id +",
  items: [
    {
      title: "Two-step authentication",
      description: "Authentication app. You will receive a code from your security app.",
      status: "Not activated",
      buttonText: "Activate",
    },
    {
      title: "SMS code",
      description: "We will send a code to your phone number.",
      status: "Not activated",
      buttonText: "Activate",
    },
    {
      title: "Devices you are logged in to",
      description: "Windows 10\nChrome",
      status: "Active",
      buttonText: "Active Now",
    },
  ],
};

export default function SecurityPage() {
    return (
      <div>
        <SecuritySection {...securityData}/>        
      </div>
    );
  }