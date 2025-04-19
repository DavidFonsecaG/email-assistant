import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

interface ThreadSummary {
  summary: string
}

const summarizeThreadById = async (threadId: string): Promise<ThreadSummary> => {
    const response = await axios.get(`http://localhost:8000/emails/thread/${threadId}/summary?user_email=dfonseca%40mccollege.edu`);
    return response.data;
};

export const useSummaryByThreadId = (threadId: string | null) => {
    return useQuery<ThreadSummary>({
      	queryKey: ['summary', threadId],
      	queryFn: () => summarizeThreadById(threadId!),
      	enabled: !!threadId,
    });
};
