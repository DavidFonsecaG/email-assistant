import { useState } from "react"
import { Send, X } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"
import { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent } from "@/components/ui/card"

interface SuggestedReply {
  response: string
  more_ideas: string[]
}

interface CardsChatProps {
  summary: string | null
  suggested_reply: SuggestedReply | null
  setIsCollapsed: Function
}

export function CardsChat({ summary, suggested_reply, setIsCollapsed }: CardsChatProps) {

  const [messages, setMessages] = useState([
    {
      role: "agent",
      content: "",
    },
    // {
    //   role: "user",
    //   content: "Hey, I'm having trouble with my account.",
    // },
    // {
    //   role: "agent",
    //   content: "What seems to be the problem?",
    // },
    // {
    //   role: "user",
    //   content: "I can't log in.",
    // },
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

            <Card className="text-sm">
              <CardHeader className="flex-row space-x-2">
                <Avatar className="h-6 w-6">
                  <AvatarImage src="/avatar.png" alt={`avatar.png`} />
                  <AvatarFallback>AI</AvatarFallback>
                </Avatar>
                <span className="font-semibold">Summary</span>
              </CardHeader>
              <CardContent className="pl-10 text-xs">
                {summary ? 
                  <p className="font-normal leading-snug text-muted-foreground">"{summary}"</p> 
                : (
                  <div className="space-y-2">
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-4 w-5/6" />
                    <Skeleton className="h-4 w-2/3" />
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="text-sm">
              <CardHeader className="flex-row space-x-2">
                <Avatar className="h-6 w-6">
                  <AvatarImage src="/avatar.png" alt={`avatar.png`} />
                  <AvatarFallback>AI</AvatarFallback>
                </Avatar>
                <span className="font-semibold">Suggested Reply</span>
              </CardHeader>
              <CardContent className="pl-10 text-xs">
                {suggested_reply ? 
                  <p className="font-normal leading-snug text-muted-foreground whitespace-pre-line">"{suggested_reply.response}"</p> 
                : (
                  <div className="space-y-2">
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-4 w-5/6" />
                    <Skeleton className="h-4 w-2/3" />
                  </div>
                )}
              </CardContent>
              <CardFooter className="flex-col pl-10">
                {suggested_reply ?
                  <>
                    <div>
                      <Button
                        onClick={(e) => e.preventDefault()}
                        size="xs"
                        className="ml-auto text-xs font-normal"
                      >
                        Insert
                      </Button>
                    </div>
                    <div className="space-y-1 mt-2">
                      <span className="text-xs text-muted-foreground">More ideas:</span>
                      {suggested_reply?.more_ideas.map((idea, index) =>
                      <div>
                        <Button
                          key={index}
                          onClick={(e) => e.preventDefault()}
                          size="xs"
                          className="ml-auto text-xs font-normal"
                          variant={"outline"}
                        >
                          {idea}
                        </Button>
                      </div>
                      )}
                    </div>
                  </> 
                : (
                  <div className="space-y-2">
                    <Skeleton className="h-7 w-1/4" />
                  </div>
                )} 
              </CardFooter>
            </Card>

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