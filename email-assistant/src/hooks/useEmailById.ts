import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export interface FullMail {
	id: string;
	user_email: string;
	sender_name: string;
	sender_email: string;
	subject: string;
	body_preview: string;
	timestamp: string;
	is_read: boolean;
	labels: string[];
	body_original: string;
	body_cleaned: string;
	thread_id: string;
	has_attachments: boolean;
	recipient_emails: string[];
	recipient_names: string[];
	source: string;
	web_link: string;
};

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
