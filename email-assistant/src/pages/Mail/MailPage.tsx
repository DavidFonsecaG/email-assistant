import Cookies from "js-cookie"
import useEmails from '@/hooks/useEmails'

import { Mail } from "@/components/mail/mail"
import { accounts } from "@/pages/Mail/data"

export default function MailPage() {
  const layout = Cookies.get("react-resizable-panels:layout:mail")
  const collapsed = Cookies.get("react-resizable-panels:collapsed")

  const defaultLayout = layout ? JSON.parse(layout) : undefined
  const defaultCollapsed = collapsed ? JSON.parse(collapsed) : undefined

  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useEmails();
  const mails = data?.pages.flatMap(page => page.emails) ?? [];
 
  return (
    <div className="flex-col md:flex overflow-hidden h-full">
      <Mail
        accounts={accounts}
        mails={mails}
        defaultLayout={defaultLayout}
        defaultCollapsed={defaultCollapsed}
        navCollapsedSize={4}
      />
    </div>
  )
}