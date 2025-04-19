import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

export interface SuggestedReply {
  response: string
  more_ideas: string[]
}

export interface ParsedSuggestedReplyResponse {
  intent_summary: string
  manual_facts: string[]
  matches_sent: any[]
  suggested_reply: SuggestedReply | null
}

interface RawSuggestedReplyResponse {
  intent_summary: string
  manual_facts: string[]
  matches_sent: any[]
  suggested_reply: string
}

const fetchSuggestedReply = async (text: string): Promise<RawSuggestedReplyResponse> => {
  const response = await axios.post('http://localhost:8000/emails/suggested_reply', 
    text,
  )
  return response.data
}

export const useSuggestedReply = (text: string | null) => {
  return useQuery<ParsedSuggestedReplyResponse>({
    queryKey: ['suggested-reply', text],
    queryFn: async () => {
      const rawData = await fetchSuggestedReply(text!)

      let parsed: SuggestedReply | null = null
      try {
        parsed = JSON.parse(rawData.suggested_reply)
      } catch (err) {
        console.error('Failed to parse suggested_reply:', err)
      }

      return {
        ...rawData,
        suggested_reply: parsed,
      }
    },
    enabled: !!text,
  })
}
