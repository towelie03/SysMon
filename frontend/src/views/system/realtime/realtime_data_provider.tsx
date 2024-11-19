import { ReactNode, useEffect, useState } from "react";
import { RealtimeDataContext } from "./realtime_data_context.ts";

// type RealtimeData = {
//   "throughput":
// }

export function RealtimeDataProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<Array<any>>([
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
  ]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/realtime");
        const result = await response.json();

        setData((oldData) => {
          if (oldData.length >= 10) {
            return [...oldData.slice(-9), result];
          }

          return [...oldData, result];
        });
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    // Fetch data every 2 seconds
    const intervalId = setInterval(fetchData, 2000);

    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  return (
    <RealtimeDataContext.Provider value={data}>
      {children}
    </RealtimeDataContext.Provider>
  );
}
