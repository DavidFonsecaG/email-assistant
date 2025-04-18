import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { ThreadSummary } from '@/pages/Mail/data';

const fetchEmailById = async (threadId: string): Promise<ThreadSummary> => {
  const response = await axios.get(`http://localhost:8000/emails/thread/${threadId}/summary?user_email=dfonseca%40mccollege.edu`);
  return response.data;
};

export const useSummaryByThreadId = (threadId: string | null) => {
  return useQuery<ThreadSummary>({
    queryKey: ['summary', threadId],
    queryFn: () => fetchEmailById(threadId!),
    enabled: !!threadId,
  });
};
