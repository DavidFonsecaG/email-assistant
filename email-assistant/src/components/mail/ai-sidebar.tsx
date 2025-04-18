import { Button } from "@/components/ui/button"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { Textarea } from "@/components/ui/textarea"
import { FullMail } from "@/pages/Mail/data"
import { useSummaryByThreadId } from '@/hooks/useSummaryByThreadId';

interface AiSidebarProps {
  mail: FullMail | null
}

export function AiSidebar({ mail }: AiSidebarProps) {
  const { data: threadSummary = null } = useSummaryByThreadId(mail?.thread_id || "")
  
  return (
    <div className="flex h-full w-[--sidebar-width] flex-col bg-sidebar text-sidebar-foreground !w-[calc(var(--sidebar-width-icon)_+_1px)] border-r">
      <div data-sidebar="header" className="flex flex-col gap-2 p-2">
        <ul data-sidebar="menu" className="flex w-full min-w-0 flex-col gap-1">
          <li data-sidebar="menu-item" className="group/menu-item relative">
          <Tooltip key={mail?.thread_id} delayDuration={0}>
            <Popover>
              <PopoverTrigger asChild>
                <TooltipTrigger asChild>
                  <Button variant="ai" className="px-4.5" disabled={!mail}></Button>
                </TooltipTrigger>
              </PopoverTrigger>
              <PopoverContent className="w-100">
                <div className="grid gap-4">
                  <div className="space-y-2">
                    <h4 className="font-medium leading-none">Email Companion</h4>
                    <p className="text-sm text-muted-foreground">
                    summary
                    </p>
                  </div>
                  <div className="grid gap-2">
                    <Textarea
                      className="p-4"
                      placeholder={threadSummary?.summary}
                    />
                  </div>
                </div>
              </PopoverContent>
            </Popover>
            <TooltipContent side="right" className="flex items-center gap-4">
              {"Try AI"}
            </TooltipContent>
          </Tooltip>
          </li>
        </ul>
      </div>
    </div>
  )
}