import { format, isToday, isThisYear } from "date-fns"

export function formatDate(dateString: string): string {
    const date = new Date(dateString);
  
    if (isToday(date)) {
      return format(date, 'hh:mm a'); // e.g., 10:30 AM
    }
  
    if (isThisYear(date)) {
      return format(date, 'MMM d'); // e.g., Apr 11
    }
  
    return format(date, 'M/d/yy'); // e.g., 4/11/24
  }