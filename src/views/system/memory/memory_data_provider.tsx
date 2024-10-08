import { ReactNode, useEffect, useState } from "react";
import { MemoryDataContext } from "./memory_data_context";

export function MemoryUsageProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<Array<any>>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/memory/all");
        const result = await response.json();
        console.log(result)

        setData((oldData) => {
          if (oldData.length >= 10) {
            return [...oldData.slice(-9), result];
          }

          return [
            ...oldData,
            result
          ];
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
    <MemoryDataContext.Provider value={data}>
      {children}
    </MemoryDataContext.Provider>
  );
}
