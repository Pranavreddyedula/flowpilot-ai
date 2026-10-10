import { useEffect, useState } from 'react';

export default function App() {
  const [status, setStatus] = useState<{ status?: string; provider?: string; message?: string } | null>(null);
  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((response) => response.json())
      .then(setStatus)
      .catch(() => setStatus({ message: 'API unavailable' }));
  }, []);

  return (
    <main style={{ fontFamily: 'sans-serif', padding: 32 }}>
      <h1>FlowPilot AI</h1>
      <pre>{JSON.stringify(status, null, 2)}</pre>
    </main>
  );
}
