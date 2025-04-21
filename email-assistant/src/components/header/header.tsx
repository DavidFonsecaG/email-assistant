import { Link } from "react-router-dom"
import { UserNav } from "@/components/header/user-nav"

const Header = () => {

  return (
    <div className="border-b">
        <div className="flex h-11 items-center px-4">
          <Link to="/mail/">
            <span className="text-2xl font-semibold tracking-tight" >
              email.ai
            </span>
          </Link>
          <div className="ml-auto flex items-center space-x-4">
              <UserNav />
          </div>
        </div>
    </div>
  );
};

export default Header;
