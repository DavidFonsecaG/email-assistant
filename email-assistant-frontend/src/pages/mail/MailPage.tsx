import Cookies from "js-cookie"

import { Mail } from "@/components/mail/mail"
import { accounts, mails } from "@/pages/mail/data"

export default function MailPage() {
  const layout = Cookies.get("react-resizable-panels:layout:mail")
  const collapsed = Cookies.get("react-resizable-panels:collapsed")

  const defaultLayout = layout ? JSON.parse(layout) : undefined
  const defaultCollapsed = collapsed ? JSON.parse(collapsed) : undefined

  return (
    <>
      <div className="flex-col md:flex overflow-hidden">
        <Mail
          accounts={accounts}
          mails={mails}
          defaultLayout={defaultLayout}
          defaultCollapsed={defaultCollapsed}
          navCollapsedSize={4}
        />
      </div>
    </>
  )
}