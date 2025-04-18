import { Link } from "react-router-dom"
import { Search } from "@/components/header/search"
import { UserNav } from "@/components/header/user-nav"

const Header = () => {

  return (
    <div className="border-b h-16">
        <div className="flex h-16 items-center px-4">
          <Link to="/mail/">
            <span className="text-3xl font-bold tracking-tight" >
              email.ai
            </span>
          </Link>
          <div className="ml-auto flex items-center space-x-4">
              <Search />
              <UserNav />
          </div>
        </div>
    </div>
  );
};

export default Header;
