import { Button } from "@/components/ui/button"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Textarea } from "@/components/ui/textarea"


export function AiSidebar() {


  return (
    <div className="flex h-full w-[--sidebar-width] flex-col bg-sidebar text-sidebar-foreground !w-[calc(var(--sidebar-width-icon)_+_1px)] border-r">
      <div data-sidebar="header" className="flex flex-col gap-2 p-2">
        <ul data-sidebar="menu" className="flex w-full min-w-0 flex-col gap-1">
          <li data-sidebar="menu-item" className="group/menu-item relative">
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="default" className="px-3">AI</Button>
            </PopoverTrigger>
            <PopoverContent className="w-100">
              <div className="grid gap-4">
                <div className="space-y-2">
                  <h4 className="font-medium leading-none">Email Companion</h4>
                  <p className="text-sm text-muted-foreground">
                    Some info here.
                  </p>
                </div>
                <div className="grid gap-2">
                  <Textarea
                    className="p-4"
                    placeholder={`Ask something ${"here"}...`}
                  />
                </div>
              </div>
            </PopoverContent>
          </Popover>
          </li>
        </ul>
      </div>
    </div>
  )
}