import { Search } from "@/components/header/search"
import { UserNav } from "@/components/header/user-nav"

const Header = () => {
  return (
    <div className="border-b">
        <div className="flex h-16 items-center px-4">
        <h1 className="text-3xl font-bold tracking-tight">email.ai</h1>
        <div className="ml-auto flex items-center space-x-4">
            <Search />
            <UserNav />
        </div>
        </div>
    </div>
  );
};

export default Header;
