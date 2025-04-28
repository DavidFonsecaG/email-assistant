import { createBrowserRouter } from "react-router-dom";
import App from "@/App";
// import Home from "@/pages/Home";
// import About from "@/pages/About";
import MailPage from "@/pages/Mail/MailPage";
import LoginPage from "@/pages/Login/LoginPage";
// import ErrorPage from "@/pages/ErrorPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPage/>,
  },
  {
    path: "/mail",
    element: <App />,
    errorElement: <MailPage />,
    children: [
      { index: true, element: <MailPage /> },
      { path: ":mailId", element: <MailPage /> },
    ],
  },
]);
