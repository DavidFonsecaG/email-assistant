import { createBrowserRouter } from "react-router-dom";
import App from "@/App";
// import Home from "@/pages/Home";
// import About from "@/pages/About";
import MailPage from "@/pages/Mail/MailPage";
// import ErrorPage from "@/pages/ErrorPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <MailPage />,
    children: [
      { index: true, element: <MailPage /> },
      { path: "mail", element: <MailPage /> },
      { path: "mail/:mailId", element: <MailPage /> },
      { path: "about", element: <MailPage /> },
    ],
  },
]);
