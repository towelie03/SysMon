import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ThemeContext } from "@/theme_provider";
import { useContext } from "react";

export function SettingsView() {
  const theme = useContext(ThemeContext)

  return (
    <div className="flex flex-col gap-8 w-full h-full">
      <div className="flex flex-col gap-4">
        <div className="text-4xl font-bold">Theme</div>
        <div>
        <Select onValueChange={(value) => {
            theme.setTheme(value)
        }}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder={theme.theme} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="Catpuccin">Catpuccin</SelectItem>
            <SelectItem value="DefaultGreen">Default Green</SelectItem>
            <SelectItem value="DarkRed">Dark Red</SelectItem>
            <SelectItem value="LightRed">Light Red</SelectItem>
          </SelectContent>
        </Select>
        </div>
      </div>
    </div>
  );
}
