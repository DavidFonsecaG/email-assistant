import React from "react";
import { Button } from "@/components/ui/button"

export default function OutlookLoginButton() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/login"; // your FastAPI backend
  };

  return (
    <Button
      onClick={handleLogin}
    //   className="px-4 py-2 bg-blue-600 text-white rounded-lg"
    >
      Sign in with Outlook
    </Button>
  );
}
