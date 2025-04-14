import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { FullMail } from '@/pages/Mail/data';

const fetchEmailById = async (id: string): Promise<FullMail> => {
  const response = await axios.get(`http://localhost:8000/emails/${id}`);
  return response.data;
};

export const useEmailById = (id: string | null) => {
  return useQuery({
    queryKey: ['email', id],
    queryFn: () => fetchEmailById(id!),
    enabled: !!id,
  });
};
