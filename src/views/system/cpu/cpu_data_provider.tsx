import { ReactNode, useEffect, useState } from "react";
import { CpuDataContext } from "./cpu_data_context";

export function CpuUsageProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<Array<any>>([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/cpu/usage");
        const result = await response.json();

        setData((oldData) => {
          if (oldData.length >= 10) {
            return [...oldData.slice(-9), { amt: result.cpu_usage }];
          }

          return [
            ...oldData,

            {
              amt: result.cpu_usage,
            },
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
    <CpuDataContext.Provider value={data}>{children}</CpuDataContext.Provider>
  );
}
