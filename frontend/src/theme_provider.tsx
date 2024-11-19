import { createContext, ReactNode, useState } from "react";

export const ThemeContext = createContext<any>({theme: "Catpuccin"});

export function ThemeProvider({ children }: { children: ReactNode}) {
  const [theme, setTheme] = useState("Catpuccin");

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
