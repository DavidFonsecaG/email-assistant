import { useInfiniteQuery } from '@tanstack/react-query';
import axios from 'axios';

const fetchEmails = async ({ pageParam = 1 }) => {
  const response = await axios.get(`http://localhost:8000/emails?page=${pageParam}&pageSize=20&user_email=dfonseca@mccollege.edu&source=received`);
  return response.data;
};

const useEmails = () => {
  return useInfiniteQuery({
    queryKey: ['emails'],
    queryFn: fetchEmails,
    initialPageParam: 1,
    getNextPageParam: (lastPage, allPages) => {
      const totalFetched = allPages.flatMap(page => page.emails).length;
      return totalFetched < lastPage.total ? allPages.length + 1 : undefined;
    },
  });
};

export default useEmails;
