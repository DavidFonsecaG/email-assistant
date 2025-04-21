import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

interface ConversationSummary {
  summary: string;
}

const fetchSummaryByEmailId = async (emailId: string): Promise<ConversationSummary> => {
  const response = await axios.get(`http://localhost:8000/emails/${emailId}/sender-summary`);
  return response.data;
};

export const useSummaryByEmailId = (emailId: string | null) => {
  return useQuery<ConversationSummary>({
    queryKey: ['email-summary', emailId],
    queryFn: () => fetchSummaryByEmailId(emailId!),
    enabled: !!emailId,
  });
};
