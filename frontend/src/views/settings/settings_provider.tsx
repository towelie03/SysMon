import { ThemeContext } from "@/theme_provider";
import { createContext, useContext } from "react";
import { ReactNode, useEffect, useState } from "react";

export const SettingsDataContext = createContext<any>({});

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<any>({
    cpu_threshold: 80,
    memory_threshold: 80,
    disk_threshold: 80,
    network_threshold: 1000000,
    gpu_threshold: 80,
    check_interval: 10,
    theme: "Catpuccin",
  });
  const theme = useContext(ThemeContext);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/settings");
        const result = await response.json();

        setData(result);

        theme.setTheme(result.theme);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <SettingsDataContext.Provider value={data}>
      {children}
    </SettingsDataContext.Provider>
  );
}
