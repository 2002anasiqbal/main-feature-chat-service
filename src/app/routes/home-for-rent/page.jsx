'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomeForRend() {
  const router = useRouter();

  useEffect(() => {
    router.push('/routes/travel/holiday-homes');
  }, [router]);

  return (
    <div>
      Redirecting...
    </div>
  );
}
