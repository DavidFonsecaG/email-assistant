import { cn } from "@/lib/utils"
import { Mail } from "@/pages/Mail/data"
import { formatDate } from "@/pages/Mail/format-date"
import { useNavigate, useParams } from "react-router-dom"

interface MailListProps {
  items: Mail[]
}

export function MailList({ items }: MailListProps) {
  const { mailId } = useParams()
  const navigate = useNavigate()

  return (
      <div className="flex flex-col h-full gap-2 p-4 pt-0 overflow-auto">
        {items.map((item) => (
          <button
            key={item.id}
            className={cn(
              "flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all hover:bg-accent",
              mailId === item.id && "bg-muted"
            )}
            onClick={() => {
              navigate(`/mail/${item.id}`)
            }}
          >
            <div className="flex w-full flex-col gap-1">
              <div className="flex items-center">
                <div className="flex items-center gap-2">
                  <div className="font-semibold">{item.sender_name}</div>
                  {!item.is_read && (
                    <span className="flex h-2 w-2 rounded-full bg-blue-600" />
                  )}
                </div>
                <div
                  className={cn(
                    "ml-auto text-xs font-semibold",
                    mailId === item.id
                      ? "text-foreground"
                      : "text-muted-foreground"
                  )}
                >
                  {formatDate(item.timestamp)}
                </div>
              </div>
              <div className="line-clamp-1 text-xs font-medium">{item.subject}</div>
            </div>
            <div className="line-clamp-2 text-xs text-muted-foreground">
              {item.body_preview.substring(0, 300)}
            </div>
          </button>
        ))}
      </div>
  )
}