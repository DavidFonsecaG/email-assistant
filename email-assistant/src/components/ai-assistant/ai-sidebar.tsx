import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { CardsChat } from "@/components/ai-assistant/chat"
import { Separator } from "@/components/ui/separator"
import { FullMail } from '@/hooks/useEmailById'
import { useSummaryByEmailId } from '@/hooks/useSummaryByEmailId'
import { useSuggestedReply } from '@/hooks/useSuggestedReply'


interface AiSidebarProps {
  mail: FullMail | null
}

export function AiSidebar({ mail }: AiSidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(true)
  const { data: threadSummary = null } = useSummaryByEmailId(!isCollapsed && mail?.id ? mail.id : null)
  const { data: replyData = null } = useSuggestedReply(!isCollapsed && mail?.body_original ? mail.body_original : null)
  
  return (
    <>
      {!isCollapsed && (
        <>
          <CardsChat summary={threadSummary?.summary ?? null} suggested_reply={replyData?.suggested_reply ?? null} setIsCollapsed={setIsCollapsed}/>
          <Separator orientation = {"vertical"}/>
        </>
      )}

      <div className="flex h-full w-[--sidebar-width] flex-col bg-sidebar text-sidebar-foreground !w-[calc(var(--sidebar-width-icon)_+_1px)] border-r">
        <div data-sidebar="header" className="flex flex-col gap-2 p-2">
          <ul data-sidebar="menu" className="flex w-full min-w-0 flex-col gap-1">
            <li data-sidebar="menu-item" className="group/menu-item relative">
            <Tooltip key={mail?.thread_id} delayDuration={0}>
              <TooltipTrigger asChild>
                <Button variant="ai" className="px-4.5" disabled={!mail} onClick={() => {setIsCollapsed(!isCollapsed)}}></Button>
              </TooltipTrigger>
              <TooltipContent side="right" className="flex items-center gap-4">
                {"Try AI"}
              </TooltipContent>
            </Tooltip>
            </li>
          </ul>
        </div>
      </div>
    </>
  )
}