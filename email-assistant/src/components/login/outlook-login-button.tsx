import { Button } from "@/components/ui/button"

export default function OutlookLoginButton() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/login"; // your FastAPI backend
  };

  return (
    <Button
      onClick={handleLogin}
      variant="outline" className="w-full"
    >
      <img src="https://maxcdn.icons8.com/filters/icons/Windows-Logo.svg" alt="logo"></img>
      Sign in with Outlook
    </Button>
  );
}
