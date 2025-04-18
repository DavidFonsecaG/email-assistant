import { useState } from "react"
import { Send, X } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"


interface CardsChatProps {
  summary: string | null
  setIsCollapsed: Function
}

export function CardsChat({ summary, setIsCollapsed }: CardsChatProps) {

  const [messages, setMessages] = useState([
    {
      role: "agent",
      content: "Hi, how can I help you today?",
    },
    {
      role: "user",
      content: "Hey, I'm having trouble with my account.",
    },
    {
      role: "agent",
      content: "What seems to be the problem?",
    },
    {
      role: "user",
      content: "I can't log in.",
    },
  ])
  const [input, setInput] = useState("")
  const inputLength = input.trim().length

  return (
    <>
      <div className="flex flex-col flex-grow h-full w-1/4 transition-all duration-1000 ease-in-out">

        <div className="flex items-center justify-between py-2 px-4">
          <div className="flex h-9 items-center">
            <h4 className="font-medium leading-none">AI Assistant</h4>
          </div>
          <Button variant="ghost" size="icon" onClick={() => {setIsCollapsed(true)}}>
            <X className="h-4 w-4"/>
            <span className="sr-only">Close</span>
          </Button>
        </div>
        <Separator />

        <div className="flex flex-col h-full bg-accent overflow-hidden">
          <div className="flex-grow space-y-4 p-4 overflow-auto">
            
            <div className="flex flex-col gap-2 rounded-lg px-3 py-2 text-sm ml-auto bg-popover">
              <h5 className="font-semibold">Summary</h5>
              {summary ? 
                <p className="">{summary}</p> 
                : (
                  <div className="space-y-2">
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-4 w-5/6" />
                    <Skeleton className="h-4 w-2/3" />
                  </div>
                )}
            </div>

            {messages.map((message, index) => (
              <div
                key={index}
                className={cn(
                  "flex w-max max-w-[75%] flex-col gap-2 rounded-lg px-3 py-2 text-sm",
                  message.role === "user"
                    ? "ml-auto bg-primary text-primary-foreground"
                    : "bg-muted"
                )}
              >
                {message.content}
              </div>
            ))}
          </div>

          <form
            onSubmit={(event) => {
              event.preventDefault()
              if (inputLength === 0) return
              setMessages([
                ...messages,
                {
                  role: "user",
                  content: input,
                },
              ])
              setInput("")
            }}
            className="flex w-full items-center p-4 space-x-2"
          >
            <Input
              id="message"
              placeholder="Type your message..."
              className="flex-1 bg-popover"
              autoComplete="off"
              value={input}
              onChange={(event) => setInput(event.target.value)}
            />
            <Button type="submit" size="icon" disabled={inputLength === 0}>
              <Send />
              <span className="sr-only">Send</span>
            </Button>
          </form>
        </div>
      </div>
    </>
  )
}